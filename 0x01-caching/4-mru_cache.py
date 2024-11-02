#!/usr/bin/env python3
"""
Module implements Basic Caching using MRU (Most Recently Used) Cache Logic
"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """This class defines MRUCache inheriting from BaseCaching"""

    def __init__(self):
        """Class Constructor"""
        super().__init__()
        self.order = []  # List to maintain the order of keys (mru)

    def put(self, key, item):
        """
        This method allows adding a key-value pair to the cache.
        Args:
            key - the key of the data to be added
            item - the value of the data to be added
        """
        if key is None or item is None:
            return  # Do nothing if key or item is None

        if key in self.cache_data:
            # If the key already exists, remove it to update its order
            self.order.remove(key)
        else:
            # If the cache is full, evict the most recently used item
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                mru_key = self.order.pop()  # Remove the last item (mru)
                self.cache_data.pop(mru_key)
                print(f"DISCARD: {mru_key}")

        # Add the new key-value pair to the cache
        self.cache_data[key] = item
        self.order.append(key)  # Track the order of keys

    def get(self, key):
        """
        This method retrieves an item from the cache by the key.
        Args:
            key - key to the data to be retrieved.
        Returns:
            Value of the item if found, None if key is None or doesn't exist.
        """
        if key is None or key not in self.cache_data:
            return None  # Return None if key is invalid

        # Update the order to reflect that this key has been accessed
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]  # Return the cached value
