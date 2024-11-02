#!/usr/bin/env python3
"""
Module implements LFU (Least Frequently Used) Cache Logic
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """This class defines LFUCache inheriting from BaseCaching"""

    def __init__(self):
        """Class Constructor"""
        super().__init__()
        self.freq_map = {}  # Map to track frequency of each key
        self.lfu_order = []  # List to track the order of keys by frequency
        self.min_freq = 0  # Track the minimum frequency

    def put(self, key, item):
        """
        This method allows adding a key-value pair to the cache.
        Args:
            key - the key of the data to be added
            item - the value of the data to be added
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Update existing item
            self.cache_data[key] = item
            self._update_frequency(key)
            return

        # If cache is full, evict least frequently used item
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            self._evict()

        # Add new item to cache
        self.cache_data[key] = item
        self.freq_map[key] = 1
        self.lfu_order.append(key)
        self.min_freq = 1  # Reset min frequency to 1

    def get(self, key):
        """
        This method retrieves an item from the cache by the key.
        Args:
            key - key to the data to be retrieved.
        Returns:
            Value of the item if found, None if key is None or doesn't exist.
        """
        if key is None or key not in self.cache_data:
            return None

        # Update the frequency of the key
        self._update_frequency(key)
        return self.cache_data[key]

    def _update_frequency(self, key):
        """Update the frequency of the given key."""
        freq = self.freq_map[key]
        self.freq_map[key] += 1
        new_freq = self.freq_map[key]

        # Update LFU order
        self.lfu_order.remove(key)
        self.lfu_order.append(key)

        # If was the only key with the minimum frequency, increment min_freq
        if freq == self.min_freq and not any(f == freq for f in self.freq_map.values()):
            self.min_freq += 1

    def _evict(self):
        """Evict the least frequently used item from the cache."""
        lfu_keys = [k for k, v in self.freq_map.items() if v == self.min_freq]

        # If there are multiple keys with the same frequency, evict the LRU
        key_to_evict = lfu_keys[0]  # Pick the first key to evict
        self.cache_data.pop(key_to_evict)
        self.freq_map.pop(key_to_evict)
        self.lfu_order.remove(key_to_evict)
        print(f"DISCARD: {key_to_evict}")
