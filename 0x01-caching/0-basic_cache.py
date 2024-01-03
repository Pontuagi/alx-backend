#!/usr/bin/env python3

"""
A BasicCache module that inherits from BaseCaching
"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache inherits from BaseCaching.
    A caching sytem with put and get methods.
    """

    def put(self, key, item):
        """
        Add an item in the Cache
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
        Get an item by key
        """
        if key is not None:
            return self.cache_data.get(key)
        return None
