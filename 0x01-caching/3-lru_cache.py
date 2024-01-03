#!/usr/bin/env python3

"""
LRU Caching module
"""

from base_caching import BaseCaching
from collections import OrderedDict


class LRUCache(BaseCaching):
    """
    LRUCache class that inherits from BaseCaching
    Implementa a least recently used (LRU) caching system
    """
    def __init__(self):
        """
        Initialization
        """
        super().__init__()
        self.order = OrderedDict()

    def put(self, key, item):
        """
        Add an item to the cache
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            del self.order[key]
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Cache is full, discard the least recently used item
            least_used = next(iter(self.order))
            print(f"DISCARD: {least_used}")
            del self.cache_data[least_used]
            del self.order[least_used]

        self.cache_data[key] = item
        self.order[key] = None

    def get(self, key):
        """
        Get item by key
        """
        if key in self.cache_data:
            # If key exists, move it to the end (most recently used)
            self.order.move_to_end(key)
            return self.cache_data[key]
        return None
