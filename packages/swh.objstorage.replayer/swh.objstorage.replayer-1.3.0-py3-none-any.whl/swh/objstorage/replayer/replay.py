# Copyright (C) 2019-2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait as futures_wait
import logging
from time import time
from traceback import format_tb
from typing import Callable, Dict, List, Optional

from humanize import naturaldelta, naturalsize
import msgpack
from sentry_sdk import capture_exception, push_scope

try:
    from systemd.daemon import notify
except ImportError:
    notify = None

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)
from tenacity.retry import retry_base

from swh.core.statsd import statsd
from swh.model.hashutil import hash_to_hex
from swh.model.model import SHA1_SIZE
from swh.objstorage.constants import ID_HASH_ALGO
from swh.objstorage.exc import ObjNotFoundError
from swh.objstorage.objstorage import ObjStorage

logger = logging.getLogger(__name__)
REPORTER = None

CONTENT_OPERATIONS_METRIC = "swh_content_replayer_operations_total"
CONTENT_RETRY_METRIC = "swh_content_replayer_retries_total"
CONTENT_BYTES_METRIC = "swh_content_replayer_bytes"
CONTENT_DURATION_METRIC = "swh_content_replayer_duration_seconds"


def is_hash_in_bytearray(hash_, array, nb_hashes, hash_size=SHA1_SIZE):
    """
    Checks if the given hash is in the provided `array`. The array must be
    a *sorted* list of sha1 hashes, and contain `nb_hashes` hashes
    (so its size must by `nb_hashes*hash_size` bytes).

    Args:
        hash_ (bytes): the hash to look for
        array (bytes): a sorted concatenated array of hashes (may be of
            any type supporting slice indexing, eg. :class:`mmap.mmap`)
        nb_hashes (int): number of hashes in the array
        hash_size (int): size of a hash (defaults to 20, for SHA1)

    Example:

    >>> import os
    >>> hash1 = os.urandom(20)
    >>> hash2 = os.urandom(20)
    >>> hash3 = os.urandom(20)
    >>> array = b''.join(sorted([hash1, hash2]))
    >>> is_hash_in_bytearray(hash1, array, 2)
    True
    >>> is_hash_in_bytearray(hash2, array, 2)
    True
    >>> is_hash_in_bytearray(hash3, array, 2)
    False
    """
    if len(hash_) != hash_size:
        raise ValueError("hash_ does not match the provided hash_size.")

    def get_hash(position):
        return array[position * hash_size : (position + 1) * hash_size]

    # Regular dichotomy:
    left = 0
    right = nb_hashes
    while left < right - 1:
        middle = int((right + left) / 2)
        pivot = get_hash(middle)
        if pivot == hash_:
            return True
        elif pivot < hash_:
            left = middle
        else:
            right = middle
    return get_hash(left) == hash_


class ReplayError(Exception):
    """An error occurred during the replay of an object"""

    def __init__(self, *, obj_id, exc):
        self.obj_id = hash_to_hex(obj_id)
        self.exc = exc

    def __str__(self):
        return "ReplayError(%s, %r, %s)" % (
            self.obj_id,
            self.exc,
            format_tb(self.exc.__traceback__),
        )


def log_replay_retry(retry_state, sleep=None, last_result=None):
    """Log a retry of the content replayer"""
    exc = retry_state.outcome.exception()
    operation = retry_state.fn.__name__
    logger.debug(
        "Retry operation %(operation)s on %(obj_id)s: %(exc)s",
        {"operation": operation, "obj_id": exc.obj_id, "exc": str(exc.exc)},
    )


def log_replay_error(retry_state):
    """Log a replay error to sentry"""
    exc = retry_state.outcome.exception()

    with push_scope() as scope:
        scope.set_tag("operation", retry_state.fn.__name__)
        scope.set_extra("obj_id", exc.obj_id)
        capture_exception(exc.exc)

    error_context = {
        "obj_id": exc.obj_id,
        "operation": retry_state.fn.__name__,
        "exc": str(exc),
        "retries": retry_state.attempt_number,
    }

    logger.error(
        "Failed operation %(operation)s on %(obj_id)s after %(retries)s"
        " retries; last exception: %(exc)s",
        error_context,
    )

    # if we have a global error (redis) reporter
    if REPORTER is not None:
        oid = f"blob:{exc.obj_id}"
        msg = msgpack.dumps(error_context)
        REPORTER(oid, msg)

    raise exc


CONTENT_REPLAY_RETRIES = 3


class retry_log_if_success(retry_base):
    """Log in statsd the number of attempts required to succeed"""

    def __call__(self, retry_state):
        if not retry_state.outcome.failed:
            statsd.increment(
                CONTENT_RETRY_METRIC,
                tags={
                    "operation": retry_state.fn.__name__,
                    "attempt": str(retry_state.attempt_number),
                },
            )
        return False


content_replay_retry = retry(
    retry=retry_if_exception_type(ReplayError) | retry_log_if_success(),
    stop=stop_after_attempt(CONTENT_REPLAY_RETRIES),
    wait=wait_random_exponential(multiplier=1, max=60),
    before_sleep=log_replay_retry,
    retry_error_callback=log_replay_error,
)


@content_replay_retry
def get_object(objstorage, obj_id):
    try:
        with statsd.timed(CONTENT_DURATION_METRIC, tags={"request": "get"}):
            obj = objstorage.get(obj_id)
            logger.debug("retrieved %(obj_id)s", {"obj_id": hash_to_hex(obj_id)})
        return obj
    except ObjNotFoundError:
        logger.error(
            "Failed to retrieve %(obj_id)s: object not found",
            {"obj_id": hash_to_hex(obj_id)},
        )
        raise
    except Exception as exc:
        raise ReplayError(obj_id=obj_id, exc=exc) from None


@content_replay_retry
def put_object(objstorage, obj_id, obj):
    try:
        logger.debug("putting %(obj_id)s", {"obj_id": hash_to_hex(obj_id)})
        with statsd.timed(CONTENT_DURATION_METRIC, tags={"request": "put"}):
            logger.debug("storing %(obj_id)s", {"obj_id": hash_to_hex(obj_id)})
            objstorage.add(obj, obj_id, check_presence=False)
            logger.debug("stored %(obj_id)s", {"obj_id": hash_to_hex(obj_id)})
    except Exception as exc:
        logger.error(
            "putting %(obj_id)s failed: %(exc)r",
            {"obj_id": hash_to_hex(obj_id), "exc": exc},
        )
        raise ReplayError(obj_id=obj_id, exc=exc) from None


def copy_object(obj_id, src, dst):
    obj = get_object(src, obj_id)
    if obj is not None:
        put_object(dst, obj_id, obj)
        statsd.increment(CONTENT_BYTES_METRIC, len(obj))
        return len(obj)
    return 0


@content_replay_retry
def obj_in_objstorage(obj_id, dst):
    """Check if an object is already in an objstorage, tenaciously"""
    try:
        return obj_id in dst
    except Exception as exc:
        raise ReplayError(obj_id=obj_id, exc=exc) from None


def process_replay_objects_content(
    all_objects: Dict[str, List[dict]],
    *,
    src: ObjStorage,
    dst: ObjStorage,
    exclude_fn: Optional[Callable[[dict], bool]] = None,
    check_dst: bool = True,
    concurrency: int = 16,
):
    """
    Takes a list of records from Kafka (see
    :py:func:`swh.journal.client.JournalClient.process`) and copies them
    from the `src` objstorage to the `dst` objstorage, if:

    * `obj['status']` is `'visible'`
    * `exclude_fn(obj)` is `False` (if `exclude_fn` is provided)
    * `obj['sha1'] not in dst` (if `check_dst` is True)

    Args:
        all_objects: Objects passed by the Kafka client. Most importantly,
            `all_objects['content'][*]['sha1']` is the sha1 hash of each
            content.
        src: An object storage (see :py:func:`swh.objstorage.get_objstorage`)
        dst: An object storage (see :py:func:`swh.objstorage.get_objstorage`)
        exclude_fn: Determines whether an object should be copied.
        check_dst: Determines whether we should check the destination
            objstorage before copying.

    Example:

    >>> import hashlib
    >>> from swh.objstorage.factory import get_objstorage
    >>> src = get_objstorage('memory')
    >>> dst = get_objstorage('memory')
    >>> cnt1 = b'foo bar'
    >>> cnt2 = b'baz qux'
    >>> id1 = hashlib.sha1(cnt1).digest()
    >>> id2 = hashlib.sha1(cnt2).digest()
    >>> src.add(b'foo bar', obj_id=id1)
    >>> src.add(b'baz qux', obj_id=id2)
    >>> kafka_partitions = {
    ...     'content': [
    ...         {
    ...             'sha1': id1,
    ...             'status': 'visible',
    ...         },
    ...         {
    ...             'sha1': id2,
    ...             'status': 'visible',
    ...         },
    ...     ]
    ... }
    >>> process_replay_objects_content(
    ...     kafka_partitions, src=src, dst=dst,
    ...     exclude_fn=lambda obj: obj['sha1'] == id1)
    >>> id1 in dst
    False
    >>> id2 in dst
    True
    """

    def _copy_object(obj):
        obj_id = obj[ID_HASH_ALGO]
        logger.debug("Starting copy object %s", hash_to_hex(obj_id))
        if obj["status"] != "visible":
            logger.debug("skipped %s (status=%s)", hash_to_hex(obj_id), obj["status"])
            statsd.increment(
                CONTENT_OPERATIONS_METRIC,
                tags={"decision": "skipped", "status": obj["status"]},
            )
            return "skipped", None
        elif exclude_fn and exclude_fn(obj):
            logger.debug("skipped %s (manually excluded)", hash_to_hex(obj_id))
            statsd.increment(CONTENT_OPERATIONS_METRIC, tags={"decision": "excluded"})
            return "excluded", None
        elif check_dst and obj_in_objstorage(obj_id, dst):
            logger.debug("skipped %s (in dst)", hash_to_hex(obj_id))
            statsd.increment(CONTENT_OPERATIONS_METRIC, tags={"decision": "in_dst"})
            return "in_dst", None
        else:
            try:
                copied_bytes = copy_object(obj_id, src, dst)
            except ObjNotFoundError:
                logger.debug("not found %s", hash_to_hex(obj_id))
                statsd.increment(
                    CONTENT_OPERATIONS_METRIC, tags={"decision": "not_in_src"}
                )
                return "not_found", None
            except Exception as exc:
                logger.info("failed %s (%r)", hash_to_hex(obj_id), exc)
                statsd.increment(CONTENT_OPERATIONS_METRIC, tags={"decision": "failed"})
                return "failed", None
            else:
                if copied_bytes is None:
                    logger.debug("failed %s (None)", hash_to_hex(obj_id))
                    statsd.increment(
                        CONTENT_OPERATIONS_METRIC, tags={"decision": "failed"}
                    )
                    return "failed", None
                else:
                    logger.debug("copied %s (%d)", hash_to_hex(obj_id), copied_bytes)
                    statsd.increment(
                        CONTENT_OPERATIONS_METRIC, tags={"decision": "copied"}
                    )
                    return "copied", copied_bytes
        logger.debug("failed %s (XXX)", hash_to_hex(obj_id))
        return "failed", None

    vol = 0
    stats = dict.fromkeys(
        ["skipped", "excluded", "not_found", "failed", "copied", "in_dst"], 0
    )
    t0 = time()

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = []
        for (object_type, objects) in all_objects.items():
            if object_type != "content":
                logger.warning(
                    "Received a series of %s, this should not happen", object_type
                )
                continue
            for obj in objects:
                futures.append(pool.submit(_copy_object, obj=obj))
        logger.debug("Waiting for futures (%d)", len(futures))
        futures_wait(futures)
    logger.debug("Checking futures results")
    for f in futures:
        exc = f.exception()
        if exc:
            # XXX this should not happen, so it is probably wrong...
            raise exc
        else:
            state, nbytes = f.result()
            if nbytes is not None:
                vol += nbytes
            stats[state] += 1

    dt = time() - t0
    logger.info(
        "processed %s content objects (%s) in %s "
        "(%.1f obj/sec, %s/sec) "
        "- %d copied - %d in dst - %d skipped "
        "- %d excluded - %d not found - %d failed",
        len(futures),
        naturalsize(vol),
        naturaldelta(dt),
        len(futures) / dt,
        naturalsize(vol / dt),
        stats["copied"],
        stats["in_dst"],
        stats["skipped"],
        stats["excluded"],
        stats["not_found"],
        stats["failed"],
    )

    if notify:
        notify("WATCHDOG=1")
