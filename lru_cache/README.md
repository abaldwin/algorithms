# Introduction

Least Recently Used cache

It's useful to have an in-memory cache that has size limits, with the least-recently used items removed first.

This module creates a Least Recently Used cache using Python's [collections.OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict). 

# Examples

To add items to the cache, use standard dict methods:

```python
from lru_cache import LruCache

cache = LruCache(max_size=3)   # The default size is 100 items

cache.max_size()    # => 3
cache.is_full()     # => False

cache[1] = 'val 1'
cache[2] = 'val 2'
print(cache)   # => LruCache([(1, 'val 1'), (2, 'val 2')])

cache.update({3: 'val 3'})
print(cache)   # => LruCache([(1, 'val 1'), (2, 'val 2'), (3, 'val 3')])

cache.is_full()     # => True

```

Updating existing keys marks them as recently used:

```python
cache[1] = 'new val'
print(cache)     # LruCache([(2, 'val 2'), (3, 'val 3'), (1, 'new val')])

cache.update({3: 'new 3', 2: 'new 2'}) # A Python dictionary is unordered
print(cache)     # LruCache([(1, 'new val'), (2, 'new 2'), (3, 'new 3')])
```


Adding new keys to a full cache removes the least recently used entries to make space:

```python
cache.is_full()     # => True
cache[4] = 'val 4'
cache[5] = 'val 5'
print(cache)    # => LruCache([(3, 'new 3'), (4, 'val 4'), (5, 'val 5')])
```


Using the get function marks an entry as recently used:

```python
cache.get(3)  # => 'new val'
print(cache)    # => LruCache([(4, 'val 4'), (5, 'val 5'), (3, 'new 3')])

cache.get(55, 'DEFAULT') # => 'DEFAULT'
```


Using dict[key] notation or the parent's get function does not mark entry as recently used:

```python
cache[5]      # => 'val 5'
print(cache)    # => LruCache([(4, 'val 4'), (5, 'val 5'), (3, 'new 3')])

cache._parent.get(4)   # => 'val 4'
print(cache)    # => LruCache([(4, 'val 4'), (5, 'val 5'), (3, 'new 3')])
```


To get the least recently used item:

```python
cache.pop_lru()  # => (4, 'val 4')
print(cache)     # => LruCache([(5, 'val 5'), (3, 'new 3')])
```


To test the module:

```python
python tests_lru_cache.py
```