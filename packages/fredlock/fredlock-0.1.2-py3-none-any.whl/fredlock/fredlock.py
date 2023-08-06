"""
Lock implementation
"""
import logging
import time
from functools import lru_cache

from redis import Redis
import pottery
from pottery import Redlock
# from pottery.exception import ReleaseUnlockedLock

from .config import Config
from .executor import execute

log = logging.getLogger(__name__)


def acq_params(timeout):
    """
        Computes lock acquire parameters (timeout, blocking)
        based on timeout
    """
    if timeout < 0:
        return dict(blocking=True, timeout=-1)
    if timeout == 0:
        return dict(blocking=False)
    return dict(blocking=True, timeout=timeout)


class FRedLock:
    """ FredLock application"""

    def __init__(self, config: Config):
        """ Initialize """
        self.conf = config

    @property
    @lru_cache(maxsize=1)
    def lock_name(self):
        """ Get lock name"""
        return self.conf.lock_name

    @property
    @lru_cache(maxsize=1)
    def redis(self):
        """ Get Redis client """
        kwargs = self.conf.redis_config
        url = kwargs.pop('url')
        if url:
            log.debug("Creating Redis from url : %s", kwargs)
            return Redis.from_url(url, **kwargs)
        log.debug("Creating Redis : %s", kwargs)
        return Redis(**kwargs)

    @property
    @lru_cache(maxsize=1)
    def lock(self):
        """ Get lock"""
        auto_release_time = self.conf.auto_release_time
        if auto_release_time <= 0:
            auto_release_time = 3600

        if self.conf.old_pottery:
            auto_release_time = int(auto_release_time * 1000)

        log.debug("Redlock(key='%s', masters=%s, auto_release_time=%s)",
                  self.lock_name, {self.redis}, auto_release_time)

        return Redlock(key=self.lock_name,
                       masters={self.redis},
                       auto_release_time=auto_release_time)

    def run(self):
        """ Run command """
        conf = self.conf
        lock = self.lock

        log.info("Preparing to acquire lock '%s'", conf.name)
        log.debug("Current Lock Status: %s", self.lock.locked())

        lock_args = acq_params(conf.wait_timeout)
        log.debug("Lock Acquire Arguments: %s", lock_args)

        if lock.acquire(**lock_args):
            try:
                log.debug("Lock acquired!")

                if conf.delay_after_acquire > 0:
                    log.info("Delaying %s seconds before running command",
                             conf.delay_after_acquire)
                    time.sleep(conf.delay_after_acquire)

                log.info("Executing command: %s", " ".join(conf.command))
                retcode = execute(*conf.command)
                log.info("Finished Executing command.")

                if conf.delay_before_release > 0:
                    log.info("Delaying %s seconds before releasing lock",
                             conf.delay_before_release)
                    time.sleep(conf.delay_before_release)
                return retcode
            finally:
                try:
                    lock.release()
                except pottery.exceptions.ReleaseUnlockedLock as ex:
                    log.debug("Exception: %s: %s", ex.__class__.__name__, ex)
                    log.warning("Warning, lock '%s' was already released. "
                                "Your command took longer than max allowed time",
                                conf.name)
        log.warning("Failed to get lock, command not executed!")
        return -2

    def check(self, locked="Locked", available="Available") -> float:
        """ Check if the lock is locked or not """
        remains = self.lock.locked()
        if remains:
            log.info("%s: %s", locked, remains)
        else:
            log.info("%s", available)
        return remains
