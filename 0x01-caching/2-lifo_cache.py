#!/usr/bin/env python3

"""
LIFOCache module
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    A class LIFOCache that inherits from BaseCaching
    implements a LIFO caching system
    """
    def __init__(self):
        """
        Initializing
        """
        super().__init__()

    def put(self, key, item):
        """
        Insert an item to cache
        """
        if key is None or item is None:
            return
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key = list(self.cache_data.keys())[-1]
            print(f"DISCARD: {last_key}")
            del self.cache_data[last_key]

        self.cache_data[key] = item

    def get(self, key):
        """
        Get an item by key
        """
        if key is None:
            return None
        return self.cache_data.get(key)
