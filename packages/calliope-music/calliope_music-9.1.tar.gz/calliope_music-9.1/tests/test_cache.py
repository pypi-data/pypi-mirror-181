# Calliope
# Copyright (C) 2018  Sam Thursfield <sam@afuera.me.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import pytest

import calliope

import datetime
import threading


KINDS = [calliope.cache.SqliteCache]


test_counter = 1
@pytest.fixture
def cache(tmpdir, kind):
    global test_counter
    namespace = f'test-{test_counter}'
    test_counter += 1
    return kind(namespace, cachedir=tmpdir)


@pytest.mark.parametrize('kind', KINDS)
def test_dict(cache):
    '''Store and retrieve a dictionary value.'''
    key = 'foo'
    value = {'a': 5, 'b': 4}

    found_timestamp, returned_value = cache.lookup(key)
    assert found_timestamp == None
    assert returned_value == None

    cache.store(key, value)

    found_timestamp, returned_value = cache.lookup(key)

    assert found_timestamp
    assert returned_value == value


@pytest.mark.parametrize('kind', KINDS)
def test_null_value(cache):
    '''Store and retrieve a null value.'''
    key = 'foo'
    value = None

    found_timestamp, returned_value = cache.lookup(key)
    assert found_timestamp == None
    assert returned_value == None

    cache.store(key, value)

    found_timestamp, returned_value = cache.lookup(key)

    assert found_timestamp
    assert returned_value == value


def assert_timestamp_equal_without_milliseconds(a, b):
    fmt = 'YYYY-MM-DDTHH:MM:SS'
    assert a.strftime(fmt) == b.strftime(fmt)

@pytest.mark.parametrize('kind', KINDS)
def test_timestamps(cache):
    '''Timestamps are stored with values.'''

    key = 'timestamp-key'
    value = 'timestamp-value'

    then = datetime.datetime.now()
    cache.store(key, value)
    found_timestamp, returned_value = cache.lookup(key)
    assert then <= found_timestamp < datetime.datetime.now()

    cache.store(key, value, timestamp=then)
    found_timestamp, returned_value = cache.lookup(key)
    assert_timestamp_equal_without_milliseconds(found_timestamp, then)


@pytest.mark.parametrize('kind', KINDS)
def test_expiry(cache):
    '''The .wrap() method handles cache expiry.'''

    key = 'expiry-key'
    value = 'expiry-value'

    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)

    class Semaphore():
        def __init__(self):
            self.called = False
        def callback(self):
            self.called = True
            return value

    # Value never expires - callback should not be called.
    semaphore = Semaphore()
    cache.store(key, value, timestamp=one_week_ago)
    returned_value = cache.wrap(key, semaphore.callback, expiry=None)
    assert returned_value == value
    assert semaphore.called == False

    # Value expires after 1 year - callback should not be called.
    semaphore = Semaphore()
    cache.store(key, value, timestamp=one_week_ago)
    one_year_ish = datetime.timedelta(days=365)
    returned_value = cache.wrap(key, semaphore.callback, expiry=one_year_ish)
    assert returned_value == value
    assert semaphore.called == False

    # Value expires after 1 week - callback should be called.
    semaphore = Semaphore()
    cache.store(key, value, timestamp=one_week_ago)
    one_week = datetime.timedelta(days=7)
    returned_value = cache.wrap(key, semaphore.callback, expiry=one_week)
    assert returned_value == value
    assert semaphore.called == True

    # Value expires after 1 hour - callback should be called.
    semaphore = Semaphore()
    cache.store(key, value, timestamp=one_week_ago)
    one_hour = datetime.timedelta(hours=1)
    returned_value = cache.wrap(key, semaphore.callback, expiry=one_hour)
    assert returned_value == value
    assert semaphore.called == True


class Counter():
    '''Helper class used by benchmark tests.'''
    def __init__(self, limit=None):
        self.value = 0
        self.limit = limit

    def next(self):
        self.value += 1
        if self.limit is not None and self.value >= self.limit:
            self.value = 0

    def get(self):
        return self.value


@pytest.mark.parametrize('kind', KINDS)
@pytest.mark.benchmark(min_rounds=100)
def test_read_speed(cache, benchmark):
    # First, write 1000 values to the cache.
    for i in range(0, 1000):
        key = 'test:%i' % i
        test_data = 100*chr((i%26)+65)
        cache.store(key, test_data)

    def read_value(cache, counter):
        '''Test function: Read 1 value from the cache.'''
        counter.next()
        key = 'test:%i' % counter.get()
        found, value = cache.lookup(key)
        assert found
        assert len(value) == 100

    counter = Counter(limit=1000)
    benchmark(read_value, cache, counter)


@pytest.mark.parametrize('kind', KINDS)
@pytest.mark.benchmark(min_rounds=100)
def test_write_speed(cache, benchmark):
    def store_new_value(cache, counter):
        '''Test function: Write 1 value to the cache.'''
        counter.next()
        key = 'test:%i' % counter.get()
        test_data = 100*chr((counter.get()%26)+65)
        cache.store(key, test_data)

    counter = Counter()
    benchmark(store_new_value, cache, counter)


@pytest.mark.parametrize('kind', KINDS)
def test_concurrent_writes(kind, tmpdir):
    '''Test that two threads can write to the same cache file at once.'''

    class Thread1(threading.Thread):
        def run(self):
            cache = kind('benchmark', cachedir=tmpdir)
            for i in range(0, 1000):
                key = 'test:%i' % i
                test_data = 100*chr((i%26)+65)
                cache.store(key, test_data)

    class Thread2(threading.Thread):
        def run(self):
            cache = kind('benchmark', cachedir=tmpdir)
            for i in range(500, 1500):
                key = 'test:%i' % i
                test_data = 100*chr((i%26)+65)
                cache.store(key, test_data)

    t1 = Thread1()
    t2 = Thread2()
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    cache = kind('benchmark', cachedir=tmpdir)
    for i in range(0, 1500):
        found, value = cache.lookup('test:%i' % i)
        assert found, f"key 'test:{i}' was not found in the cache!"
        assert len(value) == 100
