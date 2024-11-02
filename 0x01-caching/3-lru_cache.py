#!/usr/bin/env python3
"""
Module to implement LRU Caching
"""
from base_caching import BaseCaching
from collections import OrderedDict


class LRUCache(BaseCaching):
    """
    LRUCache is a caching system that uses a Least Recently Used
    (LRU) algorithm.
    It inherits from BaseCaching and has a maximum size defined by MAX_ITEMS.
    """

    def __init__(self):
        """Initialize the cache using OrderedDict to maintain LRU order."""
        super().__init__()
        self.cache_data = OrderedDict()  # OrderedDict to track access order

    def put(self, key, item):
        """
        Add an item in the cache following LRU replacement policy.
        Args:
            key - the key of the data to be added
            item - the value of the data to be added
        """
        if key is not None and item is not None:
            # If key already exists, delete it to update its position
            if key in self.cache_data:
                del self.cache_data[key]

            # Add the item to the cache, marking it as most recently used
            self.cache_data[key] = item

            # If we exceed MAX_ITEMS, remove the least recently used item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                # Pop the first item from OrderedDict (LRU behavior)
                lru_key, _ = self.cache_data.popitem(last=False)
                print(f"DISCARD: {lru_key}")

    def get(self, key):
        """
        Retrieve an item from the cache by key.
        Args:
            key - key to the data to be retrieved
        Returns:
            Value of the item if found, None if key is None or doesn't exist.
        """
        if key is None or key not in self.cache_data:
            return None

        # Move accessed item to the end (mark as most recently used)
        item = self.cache_data.pop(key)
        self.cache_data[key] = item
        return item
