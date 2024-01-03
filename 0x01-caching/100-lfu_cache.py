#!/usr/bin/env python3

"""
LFU Caching module
"""

from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """
    LFUCache class that inherits from BaseCaching
    Implements a Least Frequently Used (LFU) caching system
    """

    def __init__(self):
        """
        Initialization
        """
        super().__init__()
        self.frequency = defaultdict(int)
        self.order = defaultdict(OrderedDict)

    def put(self, key, item):
        """
        Add an item to cache using LFU algorithm
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequency[key] += 1
        else:
            if len(self.cache_data) >= self.MAX_ITEMS:
                self._discard_least_frequent()
            self.cache_data[key] = item
            self.frequency[key] = 1

        self._update_order(key)

    def get(self, key):
        """
        Get item by key
        """
        if key in self.cache_data:
            self.frequency[key] += 1
            self._update_order(key)
            return self.cache_data[key]
        return None

    def _discard_least_frequent(self):
        """
        Discard least frequent items using LFU algorithm (and LRU if necessary)
        """
        min_frequency = min(self.frequency.values())  # Find minimum frequency
        items_to_discard = [
            k for k,
            v in self.frequency.items() if v == min_frequency]

        if len(items_to_discard) > 1:
            # Use LRU if there's more than one item with the least frequency
            lru_keys = list(self.order[min_frequency].keys())
            lru_key = min(lru_keys, key=lambda k: self.frequency[k])
            items_to_discard = [lru_key]

        for key in items_to_discard:
            print(f"DISCARD: {key}")
            del self.cache_data[key]
            del self.frequency[key]
            del self.order[min_frequency][key]

    def _update_order(self, key):
        """
        Update order based on frequency for the key
        """
        frequency = self.frequency[key]
        if key in self.order[frequency]:
            del self.order[frequency][key]
        self.order[frequency][key] = None
