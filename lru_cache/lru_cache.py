#!/usr/bin/env python

"""
.. module:: lru_cache
   :platform: Unix, Linux
   :synopsis: A Least Recently Used cache

.. moduleauthor:: Alex Baldwin <http://www.abaldwin.com>

"""

import sys

MIN_PYTHON = (2, 7)
if sys.version_info <= MIN_PYTHON:
    sys.exit("This module works with Python %s.%s and newer." % MIN_PYTHON)

from collections import OrderedDict


class LruCache(OrderedDict):
    """Least Recently Used Cache
    """
    
    def __init__(self, *args, **kwargs):
        """This initializes a Least Recently Used cache
        
        Kwargs:
            max_size (int): LRU cache capacity
            
        Returns:
            LruCache instance
        """
        self._max_size = max(1, kwargs.pop('max_size', 100))
        try:
            self._parent = super()
        except TypeError:
            self._parent = super(self.__class__, self)
        return self._parent.__init__(*args, **kwargs)
    
    def pop_lru(self):
        """Remove the least recently used cache entry
        
        Returns:
            tuple: The dictionary key and value, in (key, value) format
        """
        return self.popitem(last=False)
    
    def max_size(self):
        """Return the cache capacity
        
        Returns:
            int: The cache capacity
        """
        return self._max_size
    
    def is_full(self):
        """Test if cache is full
        
        Returns:
            bool: True if the cache is full, False otherwise
        """
        return len(self) == self.max_size()
    
    def __setitem__(self, key, value):
        """Set a key:value, marking an existing key as recently used
        
        Args:
            key (hashable): The key used to look up the entry
            value (various): The entry's value
        """
        try:
            del self[key]
        except KeyError:
            if self.is_full():
                self.pop_lru()
        return self._parent.__setitem__(key, value)
            
    def get(self, key, default=None):
        """Get a key's value and mark the key as recently used
        
        Args:
            key (hashable): The key used to look up the entry
            
        Kwargs:
            default (various): The value returned if the entry is not found
            
        Returns:
            various: The entry's value
        """
        try:
            try:
                self.move_to_end(key)
            except AttributeError:
                # OrderedDict.move_to_end was added in Python 3.2
                value = self._parent.__getitem__(key)
                self.__setitem__(key, value)
            return self._parent.__getitem__(key)
        except KeyError:
            return default

if __name__ == "__main__":
    print("I am a Least Recently Used Cache written in Python")
