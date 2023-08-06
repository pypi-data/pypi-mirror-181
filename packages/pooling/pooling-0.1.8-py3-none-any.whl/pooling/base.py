#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

__all__ = [
    "Counter",
    "Session",
    "PoolBase",
    "Pool",
]

import time
from threading import Lock
try:
    from queue import Queue
    from queue import Empty
except ImportError:
    from Queue import Queue
    from Queue import Empty

import wrapt

SESSION_USAGE_COUNT_PROPERY = "_pooling_usage_count"
SESSION_MARK_FOR_DESTORY_PROPERTY = "_pooling_mark_for_destory"


class Counter(object):

    def __init__(self, init_value=0):
        self.value = init_value
        self.lock = Lock()
    
    def incr(self):
        with self.lock as locked:
            if locked:
                self.value += 1
                return self.value

    def decr(self):
        with self.lock as locked:
            if locked:
                self.value -= 1
                return self.value


class Session(wrapt.ObjectProxy):

    def __init__(self, real_session, pool):
        wrapt.ObjectProxy.__init__(self, real_session)
        self._pooling_real_session = real_session
        self._pooling_pool = pool
        self._pooling_pool_version = pool.version.value
        self._pooling_mark_for_destory_flag = False
        self._pooling_incr_usage_count() # 使用的次数，而非引用的次数，所以是累加的。

    def __del__(self):
        self.__pooling_del__()

    def __pooling_del__(self):
        if self._pooling_real_session:
            if self._pooling_pool_version != self._pooling_pool.version.value or self._pooling_mark_for_destory_flag or self._pooling_is_connection_closed():
                self._pooling_pool.destory_session(self._pooling_real_session)
            else:
                self._pooling_pool.return_session(self._pooling_real_session)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.__pooling_del__()

    def _pooling_incr_usage_count(self):
        if hasattr(self._pooling_real_session, "__dict__"): # 如果self._pooling_real_session对象经过代理包装过的话，getattr会失效。只能直接操作__dict__属性。
            if not SESSION_USAGE_COUNT_PROPERY in self._pooling_real_session.__dict__:
                self._pooling_real_session.__dict__[SESSION_USAGE_COUNT_PROPERY] = 0
            self._pooling_real_session.__dict__[SESSION_USAGE_COUNT_PROPERY] += 1
        else:
            setattr(self._pooling_real_session, SESSION_USAGE_COUNT_PROPERY, getattr(self._pooling_real_session, SESSION_USAGE_COUNT_PROPERY, 0) + 1)

    def _pooling_get_usage_count(self):
        if hasattr(self._pooling_real_session, "__dict__"): # 如果self._pooling_real_session对象经过代理包装过的话，getattr会失效。只能直接操作__dict__属性。
            return self._pooling_real_session.__dict__.get(SESSION_USAGE_COUNT_PROPERY, 0)
        else:
            return getattr(self._pooling_real_session, SESSION_USAGE_COUNT_PROPERY, 0)

    def _pooling_mark_for_destory(self):
        self._pooling_mark_for_destory_flag = True

    def _pooling_destory_session(self):
        self._pooling_mark_for_destory_flag = True
        self._pooling_pool.destory_session(self._pooling_real_session)
        self._pooling_real_session = None

    def _pooling_return_session(self):
        self._pooling_pool.return_session(self._pooling_real_session)
        self._pooling_real_session = None

    def _pooling_is_connection_closed(self):
        return getattr(self._pooling_real_session, "_connection_closed", False)

class PoolBase(object):

    def __init__(self, pool_size, args=None, kwargs=None):
        """
        pool_size: The max number of the real session will be created.
        args: args used to make a new real session.
        kwargs: kwargs used to make a new real session.
        """
        self.pool_size = pool_size
        self.create_args = tuple(args or [])
        self.create_kwargs = kwargs or {}
        self.real_sessions = Queue()
        self.counter = Counter()
        self.make_session_lock = Lock()
        self.version = Counter(1)

    def do_session_create(self, *create_args, **create_kwargs):
        raise NotImplementedError()

    def do_session_destory(self, real_session):
        pass

    def create_session(self):
        real_session = self.do_session_create(*self.create_args, **self.create_kwargs)
        session = Session(real_session, self)
        self.counter.incr()
        return session

    def return_session(self, real_session):
        self.real_sessions.put(real_session)

    def destory_session(self, real_session):
        self.do_session_destory(real_session)
        self.counter.decr()

    def get_session(self, timeout=None):
        stime = time.time()
        # try to get session from the queue without waiting
        try:
            real_session = self.real_sessions.get_nowait()
            session = Session(real_session, self)
            return session
        except Empty:
            pass
        # the queue is empty, try to create a new session
        # don't block for ever, add timeout and check the state
        c = 0
        if self.counter.value < self.pool_size:
            while True:
                if timeout:
                    if time.time() - stime > timeout:
                        break
                flag = self.make_session_lock.acquire(False)
                if flag:
                    try:
                        if self.counter.value < self.pool_size:
                            session = self.create_session()
                            return session
                        else:
                            break
                    finally:
                        self.make_session_lock.release()
                c += 1
                if c > 100:
                    c = 0
                time.sleep(0.1 * c)
        # wait for session from the queue
        if timeout:
            get_real_session_timeout = timeout - (time.time() - stime)
            if get_real_session_timeout <= 0:
                get_real_session_timeout = 0.1
        else:
            get_real_session_timeout = None
        real_session = self.real_sessions.get(timeout=get_real_session_timeout)
        session = Session(real_session, self)
        return session

    def destory_all_sessions(self):
        # destory all sessions in the queue
        # incr pool version so that old sessions will be deleted while returning to the queue
        self.version.incr()
        while True:
            try:
                session = self.real_sessions.get_nowait()
            except Empty:
                break
            self.destory_session(session)


class Pool(PoolBase):
    
    def __init__(self, pool_size, create_factory, destory_factory=None):
        PoolBase.__init__(self, pool_size)
        self.create_factory = create_factory
        self.destory_factory = destory_factory

    def do_session_create(self, *create_args, **create_kwargs):
        return self.create_factory(*create_args, **create_kwargs)
    
    def do_session_destory(self, real_session):
        if self.destory_factory:
            self.destory_factory(real_session)
