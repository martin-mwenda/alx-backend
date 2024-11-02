#!/usr/bin/env python3
"""
Module to implement FIFO Caching
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache is a caching system that uses a First-In-First-Out
    (FIFO) algorithm.
    It inherits from BaseCaching and has a maximum size defined by MAX_ITEMS.
    """

    def __init__(self):
        """Initialize the cache with parent init and a list to track order."""
        super().__init__()
        self.order = []  # List to track the insertion order of keys

    def put(self, key, item):
        """
        Add an item in the cache following FIFO replacement policy.
        Args:
            key - the key of the data to be added
            item - the value of the data to be added
        """
        if key is not None and item is not None:
            # If key already exists, remove it to update order
            if key in self.cache_data:
                self.order.remove(key)

            # Add key to the order list
            self.order.append(key)
            self.cache_data[key] = item

            # Check if we exceed MAX_ITEMS, and apply FIFO removal if necessary
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                # FIFO - remove the oldest item
                first_key = self.order.pop(0)
                del self.cache_data[first_key]
                print(f"DISCARD: {first_key}")

    def get(self, key):
        """
        Retrieve an item from the cache by key.
        Args:
            key - key to the data to be retrieved
        Returns:
            Value of the item if found, None if key is None or doesn't exist.
        """
        return self.cache_data.get(key, None)
