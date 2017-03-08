#!/usr/bin/env python

"""
.. module:: tests_lru_cache
   :platform: Unix, Linux
   :synopsis: Tests a Least Recently Used cache

.. moduleauthor:: Alex Baldwin <http://www.abaldwin.com>

"""

import sys

MIN_PYTHON = (2, 7)
if sys.version_info <= MIN_PYTHON:
    sys.exit("This module works with Python %s.%s and newer." % MIN_PYTHON)

from collections import OrderedDict
import sys
import unittest

from lru_cache import LruCache


class TestLruCache(unittest.TestCase):
    """This class tests that the Least Recently Used cache works as specified
    """

    def setUp(self):
        self.c = LruCache();
        try:
            MAX_SIZE = 100
            self.c.update([(i, str(i)) for i in range(MAX_SIZE)])
        except:
            print("Test LRU cache could not created or populated")
            raise

    def tearDown(self):
        pass

    def test_cache_can_be_created(self):
        """LRU cache was created and inherits properly
        """
        self.assertIsInstance(self.c, LruCache)
        self.assertIsInstance(self.c, OrderedDict)
        
    def test_max_size(self):
        """A maximum size can be set on the cache
        """
        self.assertEqual(self.c.max_size(), 100)
        
        self.c = LruCache(max_size=230);
        self.assertEqual(self.c.max_size(), 230)
        
    def test_max_size_cannot_be_less_than_one(self):
        """A cache capacity must be greater than zero
        """
        new_cache = LruCache(max_size=0)
        self.assertEqual(new_cache.max_size(), 1)
        
        new_cache = LruCache(max_size=-1)
        self.assertEqual(new_cache.max_size(), 1)
        
    def test_pop_lru(self):
        """Least recently used entries are pruned
        """
        self.assertEqual(self.c.pop_lru(), (0, '0'))
        self.assertEqual(self.c.pop_lru(), (1, '1'))
        
    def test_is_full(self):
        """Test the cache capacity monitor
        """
        self.assertTrue(self.c.is_full())
        self.c.pop_lru()
        self.assertFalse(self.c.is_full())
        
    def test_updating_existing_key_with_nonfull_cache_marks_key_as_recently_used(self):
        """Updating a key in a non-full cache marks the key as recently used
        
        Updating an existing key in cache should mark the key as recently used
        and otherwise leave the cache untouched
        
        """
        NUM_ENTRIES = 38
        MAX_SIZE = 50
        
        self.c = LruCache([(i, str(i)) for i in range(NUM_ENTRIES)], max_size=MAX_SIZE)
        self.assertFalse(self.c.is_full())
        
        self.c[0] = 'new value'
        self.assertEqual(self.c.popitem(), (0, 'new value'))
        self.assertEqual(self.c.popitem(), (NUM_ENTRIES-1, str(NUM_ENTRIES-1)))
        self.assertEqual(self.c.popitem(last=False), (1, '1'))
        
    def test_updating_existing_key_with_full_cache_marks_key_as_recently_used(self):
        """Updating a key in a full cache marks the key as recently used
        
        Updating an existing key in cache should mark the key as recently used
        and otherwise leave the cache untouched
        
        """
        self.assertTrue(self.c.is_full())
        idx_last_entry = self.c.max_size()-1
        self.c[0] = 'new value'
        self.assertEqual(self.c.popitem(), (0, 'new value'))
        self.assertEqual(self.c.popitem(), (idx_last_entry, str(idx_last_entry)))
        self.assertEqual(self.c.popitem(last=False), (1, '1'))
        
    def test_adding_a_new_key_to_full_cache_removes_least_recently_used_key(self):
        """Adding a new key to a full cache removes the least recently used key
        """
        self.assertTrue(self.c.is_full())
        self.assertTrue(0 in self.c)
        
        self.c["new key"] = "new value"
        self.assertFalse(0 in self.c)
    
    def test_adding_multiple_new_keys_removes_least_recently_used_keys(self):
        """Adding multiple new keys to a full cache removes the least recently used keys
        """
        self.assertTrue(self.c.is_full())
        self.c.update([(4444, '4444'),
                       (5555, '5555'),
                       (6666, '6666'),
                       (7777, '7777')
                       ])
        for n in range(0, 4):
            self.assertFalse(n in self.c)
    
    def test_get_function_marks_key_as_recently_used(self):
        """Returns the entry's value and marks the entry as recently used
        """
        self.assertEqual(self.c.popitem(last=False), (0, '0'))
        self.c.get(1)
        self.assertEqual(self.c.popitem(), (1, '1'))
        self.assertEqual(self.c.popitem(last=False), (2, '2'))
 
if __name__ == '__main__':
    unittest.main()