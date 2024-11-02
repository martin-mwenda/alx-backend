#!/usr/bin/env python3
"""
Module implements LFU (Least Frequently Used) Cache Logic
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """This is a class that defines LFUCache inheriting from BaseCache"""

    def __init__(self):
        """Class Constructor"""
        super().__init__()
        self.frequency = {}  # Track frequency of keys
        self.order = {}  # Track the order of keys for LRU management
        self.min_freq = 0  # Track the minimum frequency in use

    def put(self, key, item):
        """
        This is a method that allows adding a key-value pair to the cache
        Args:
            key - the key of the data to be added
            item - the value of the data to be added
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item  # Update existing item
            self._update_frequency(key)
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Evict the least frequently used item
            self._evict()

        self.cache_data[key] = item
        self.frequency[key] = 1
        self.order[key] = len(self.cache_data)  # Use insertion index as order
        self.min_freq = min(self.min_freq, self.frequency[key])

    def get(self, key):
        """
        This is a method that retrieves an item from the cache by the key.
        Args:
            key - key to the data to be retrieved.
        Returns:
            Value of the item if found, None if key is None or doesn't exist.
        """
        if key is None or key not in self.cache_data:
            return None

        # Update frequency of the key
        self._update_frequency(key)
        return self.cache_data[key]

    def _update_frequency(self, key):
        """Update the frequency and order of the given key."""
        freq = self.frequency[key]
        self.frequency[key] += 1
        new_freq = self.frequency[key]

        # If this was the only key with the min frequency, update min_freq
        if (freq == self.min_freq and
                not any(f == freq for f in self.frequency.values())):
            self.min_freq += 1

        # Update the order to reflect the most recently used
        self.order[key] = len(self.cache_data)  # Update order to the latest

    def _evict(self):
        """Evict the least frequently used item from the cache."""
        lfu_keys = [k for k, v in self.frequency.items() if v == self.min_freq]

        # If there are multiple LFU keys, use LRU to determine which to evict
        key_to_evict = min(lfu_keys, key=lambda k: self.order[k])

        # Remove the item from cache
        del self.cache_data[key_to_evict]
        del self.frequency[key_to_evict]
        del self.order[key_to_evict]
        print(f"DISCARD: {key_to_evict}")
