#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

__all__ = [
    "ZenCacheService",
    "NONE",
    "NX",
    "XX",
    "GT",
    "LT",
]

import re
import time
import logging
import threading
from queue import Queue
from queue import Empty

from zenutils import serviceutils
from zenutils import errorutils
from zenutils import hashutils


_logger = logging.getLogger(__name__)

NONE = "NONE"
NX = "NX"
XX = "XX"
GT = "GT"
LT = "LT"


class ZenCacheService(serviceutils.ServiceBase):

    namespace = "zencache"

    def __init__(self, config=None, namespace=None):
        super().__init__(config, namespace)
        self._data = {}
        self._ttls = {}
        self._ttl_scanner_worker_singals = Queue()
        self._ttl_scanner_manager_signals = Queue()
        self._ttl_scanner_worker_interval = self.config.select("zencache.ttl-scanner-worker-interval", 60)
        self._ttl_scanner_manager_interval = self.config.select("zencache.ttl-scanner-manager-interval", 60)
        self._start_ttl_scanner()

    def _start_ttl_scanner(self):
        _logger.info("doing _start_ttl_scanner")
        self._ttls_scanner_worker_thread = threading.Thread(target=self._ttl_scanner_worker, daemon=True)
        self._ttls_scanner_worker_thread.start()
        self._ttls_scanner_manager_thread = threading.Thread(target=self._ttl_scanner_manager, daemon=True)
        self._ttls_scanner_manager_thread.start()
        _logger.info("_start_ttl_scanner done!")

    def _ttl_scanner_worker(self):
        while True:
            _logger.debug("_ttl_scanner_worker do scanning...")
            min_expires = None
            for key in list(self._ttls.keys()):
                expires = self._ttls.get(key)
                if not expires:
                    continue
                if expires < time.time():
                    if key in self._data:
                        del self._data[key]
                    if key in self._ttls:
                        del self._ttls[key]
                else:
                    if (min_expires is None) or (expires < min_expires):
                        min_expires = expires
            if min_expires:
                self._ttl_scanner_manager_signals.put(min_expires)
            try:
                self._ttl_scanner_worker_singals.get(timeout=self._ttl_scanner_worker_interval)
            except Empty:
                pass

    def _ttl_scanner_manager(self):
        next_work_timestamp = None
        while True:
            _logger.debug("_ttl_scanner_manager scanning...")
            if next_work_timestamp:
                if next_work_timestamp < time.time():
                    self._ttl_scanner_worker_singals.put(1)
                    next_work_timestamp = None
            else:
                self._ttl_scanner_worker_singals.put(1)
            if next_work_timestamp:
                sleepts = next_work_timestamp - time.time()
            else:
                sleepts = self._ttl_scanner_manager_interval
            if sleepts > self._ttl_scanner_manager_interval:
                sleepts = self._ttl_scanner_manager_interval
            if sleepts < 0:
                sleepts = 0.1
            try:
                new_work_timestamp = self._ttl_scanner_manager_signals.get(timeout=sleepts)
                if (next_work_timestamp is None) or (new_work_timestamp < next_work_timestamp):
                    next_work_timestamp = new_work_timestamp
            except Empty:
                pass

    def ping(self):
        return "pong"

    def flushall(self):
        self._data = {}
        self._ttls = {}
        return True

    def login(self, username, password, _protocol_instance):
        users = _protocol_instance.config.select("authentication.users", {})
        _logger.debug("zencache.login, _protocol_instance={protocol_instance}, users={users}...".format(
            protocol_instance=_protocol_instance,
            users=users,
        ))
        if not username in users:
            raise errorutils.UserPasswordError()
        configed_password = users[username]
        if hashutils.validate_password_hash(password, configed_password):
            _protocol_instance.authenticated = True
            return True
        else:
            return False

    def set(self, key, value):
        key = str(key)
        self._data[key] = value
        return True

    def get(self, key):
        key = str(key)
        return self._data.get(key, None)

    def delete(self, key):
        key = str(key)
        if key in self._data:
            del self._data[key]
        if key in self._ttls:
            del self._ttls[key]
        return True

    def setnx(self, key, value):
        key = str(key)
        if not key in self._data:
            self._data[key] = value
            return True
        else:
            return False

    def getset(self, key, value):
        key = str(key)
        old_value = self._data.get(key, None)
        self._data[key] = value
        return old_value

    def getdel(self, key):
        key = str(key)
        if key in self._data:
            old_value = self._data[key]
            del self._data[key]
            return old_value
        else:
            return None

    def getrange(self, key, start, end):
        key = str(key)
        if key in self._data:
            return self._data[start:end]
        else:
            return None

    def mset(self, data):
        for key, value in data.items():
            key = str(key)
            self._data[key] = value
        return True

    def mget(self, keys):
        data = {}
        for key in keys:
            key = str(key)
            data[key] = self._data.get(key)
        return data

    def msetnx(self, data):
        for key in data.keys():
            key = str(key)
            if key in self._data:
                return False
        for key, value in data.items():
            key = str(key)
            self._data[key] = value
        return True

    def strlen(self, key):
        key = str(key)
        if key in self._data:
            return len(self._data[key])
        else:
            return -1

    def append(self, key, value):
        key = str(key)
        if not key in self._data:
            self._data[key] = value
            return True
        else:
            if not isinstance(self._data[key], str):
                return False
            else:
                self._data[key].append(value)
                return True

    def incr(self, key):
        key = str(key)
        if not key in self._data:
            self._data[key] = 1
        else:
            self._data[key] += 1
        return self._data[key]

    def decr(self, key):
        key = str(key)
        if not key in self._data:
            self._data[key] = -1
        else:
            self._data[key] -= 1
        return self._data[key]

    def incrby(self, key, delta):
        key = str(key)
        if not key in self._data:
            self._data[key] = delta
        else:
            self._data[key] += delta
        return self._data[key]

    def decrby(self, key, delta):
        key = str(key)
        if not key in self._data:
            self._data[key] = -delta
        else:
            self._data[key] -= delta
        return self._data[key]

    def keys(self, search=None):
        if not search:
            keys = list(self._data.keys())
            keys.sort()
            return keys
        else:
            pattern = re.compile(search)
            keys = [key for key in self._data.keys() if pattern.match(key)]
            keys.sort()
            return keys

    def exists(self, key):
        key = str(key)
        if key in self._data:
            return True
        else:
            return False

    def rename(self, key, newkey):
        key = str(key)
        newkey = str(newkey)
        if key in self._data:
            self._data[newkey] = self._data[key]
            del self._data[key]
            return True
        else:
            return False

    def renamenx(self, key, newkey):
        key = str(key)
        newkey = str(newkey)
        if key in self._data:
            if not newkey in self._data:
                self._data[newkey] = self._data[key]
                del self._data[key]
                return True
            else:
                return False
        else:
            return False

    def copy(self, skey, dkey, replace=False):
        skey = str(skey)
        dkey = str(dkey)
        if skey in self._data:
            if not dkey in self._data:
                self._data[dkey] = self._data[skey]
                return True
            else:
                if replace:
                    self._data[dkey] = self._data[skey]
                    return True
                else:
                    return False
        else:
            return False

    def expire(self, key, seconds, option="NONE"):
        key = str(key)
        if not key in self._data:
            return False
        expires = time.time() + seconds
        return self.expireat(key, expires, option)

    def expireat(self, key, expires, option="NONE"):
        key = str(key)
        if not key in self._data:
            return False
        if option == "NONE":
            self._ttls[key] = expires
            self._ttl_scanner_manager_signals.put(expires)
            return True
        elif option == "NX":
            if not key in self._ttls:
                self._ttls[key] = expires
                self._ttl_scanner_manager_signals.put(expires)
                return True
        elif option == "XX":
            if key in self._ttls:
                self._ttls[key] = expires
                self._ttl_scanner_manager_signals.put(expires)
                return True
        elif option == "GT":
            if key in self._ttls:
                if expires > self._ttls[key]:
                    self._ttls[key] = expires
                    self._ttl_scanner_manager_signals.put(expires)
                    return True
        elif option == "LT":
            if key in self._ttls:
                if expires < self._ttls[key]:
                    self._ttls[key] = expires
                    self._ttl_scanner_manager_signals.put(expires)
                    return True
        return False

    def expiretime(self, key):
        key = str(key)
        if not key in self._data:
            return -2
        if not key in self._ttls:
            return -1
        return self._ttls[key]

    def ttl(self, key):
        key = str(key)
        if not key in self._data:
            return -2
        if not key in self._ttls:
            return -1
        nowtime = time.time()
        if nowtime > self._ttls[key]:
            return -2
        return self._ttls[key] - time.time()

    def lpush(self, key, value):
        key = str(key)
        if not key in self._data:
            self._data[key] = Queue()
        if not isinstance(self._data[key], Queue):
            raise errorutils.TypeError()
        self._data[key].put(value)
        return self._data[key].qsize()
    
    def rpop(self, key, timeout=None):
        key = str(key)
        if not key in self._data:
            self._data[key] = Queue()
        if not isinstance(self._data[key], Queue):
            raise errorutils.TypeError()
        try:
            return self._data[key].get(timeout=timeout)
        except Empty:
            return None

    def llen(self, key):
        key = str(key)
        if not key in self._data:
            self._data[key] = Queue()
        if not isinstance(self._data[key], Queue):
            raise errorutils.TypeError()
        return self._data[key].qsize()

    def rpoplpush(self, key1, key2, timeout=None):
        key1 = str(key1)
        key2 = str(key2)
        if not key1 in self._data:
            self._data[key1] = Queue()
        if not key2 in self._data:
            self._data[key2] = Queue()
        if not isinstance(self._data[key1], Queue):
            raise errorutils.TypeError()
        if not isinstance(self._data[key2], Queue):
            raise errorutils.TypeError()
        try:
            value = self._data[key1].get(timeout=timeout)
            self._data[key2].put(value)
            return value
        except Empty:
            return None
