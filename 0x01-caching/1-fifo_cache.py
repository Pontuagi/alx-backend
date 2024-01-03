#!/usr/bin/python3

"""
FIFOCache module
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    A FIFOCache class that inherits from BaseCaching.
    It is a Caching sytem
    """
    def __init__(self):
        """
        Initialization
        """
        super().__init__()

    def put(self, key, item):
        """
        Add an item in cache
        """
        if key is None or item is None:
            return
        if len(self.cache_data) >= self.MAX_ITEMS:
            first_key = next(iter(self.cache_data))
            print(f"DISCARD: {first_key}")
            del self.cache_data[first_key]

        self.cache_data[key] = item

    def get(self, key):
        """
        Return the value of a key
        """
        if key is not None:
            return self.cache_data.get(key)
        return None
