#!/usr/bin/env python3

"""
Most Recently Used Cache module
"""

from base_caching import BaseCaching
from collections import OrderedDict


class MRUCache(BaseCaching):
    """
    class MRUCache that inherits from BaseCaching and is a caching system
    """
    def __init__(self):
        """
        Initialization
        """
        super().__init__()
        self.order = OrderedDict()

    def put(self, key, item):
        """
        Add an item to cache
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            del self.order[key]
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            mru_key = list(self.order)[-1]
            print(f"DISCARD: {mru_key}")
            del self.cache_data[mru_key]
            del self.order[mru_key]

        self.cache_data[key] = item
        self.order[key] = None

    def get(self, key):
        """
        get Item by key
        """
        if key in self.cache_data:
            self.order.move_to_end(key)
            return self.cache_data[key]
        return None
