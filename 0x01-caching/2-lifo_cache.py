#!/usr/bin/env python3
"""
Module to implement LIFO Caching
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache is a caching system that uses a Last-In-First-Out
    (LIFO) algorithm.
    It inherits from BaseCaching and has a maximum size defined by MAX_ITEMS.
    """

    def __init__(self):
        """Initialize the cache with parent init and set up
        for LIFO behavior."""
        super().__init__()
        self.last_key = None  # Track last key added to implement LIFO removal

    def put(self, key, item):
        """
        Add an item in the cache following LIFO replacement policy.
        Args:
            key - the key of the data to be added
            item - the value of the data to be added
        """
        if key is not None and item is not None:
            # Add or update the item in the cache
            self.cache_data[key] = item
            self.last_key = key  # Track the last inserted key

            # If we exceed MAX_ITEMS, discard the last item added (LIFO)
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                # Remove the last added item from cache
                del self.cache_data[self.last_key]
                print(f"DISCARD: {self.last_key}")
                # After removal, update `last_key` to None since was discarded
                self.last_key = None

    def get(self, key):
        """
        Retrieve an item from the cache by key.
        Args:
            key - key to the data to be retrieved
        Returns:
            Value of the item if found, None if key is None or doesn't exist.
        """
        return self.cache_data.get(key, None)
