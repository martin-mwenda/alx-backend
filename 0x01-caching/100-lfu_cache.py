#!/usr/bin/env python3
"""
Module to implement LFU Caching
"""
from base_caching import BaseCaching
from collections import OrderedDict, defaultdict


class LFUCache(BaseCaching):
    """
    LFUCache is a caching system that uses a Least Frequently Used
    (LFU) algorithm.
    It discards the least frequently used item if the cache exceeds MAX_ITEMS.
    If multiple items have the same frequency, it discards the least
    recently used.
    """

    def __init__(self):
        """Initialize the cache and frequency tracking."""
        super().__init__()
        self.cache_data = OrderedDict()  # Store cache items
        self.usage_count = defaultdict(int)  # Track access frequency each key
        self.frequency_order = OrderedDict()

    def put(self, key, item):
        """
        Add an item in the cache following LFU replacement policy.
        Args:
            key - the key of the data to be added
            item - the value of the data to be added
        """
        if key is None or item is None:
            return

        # If key already exists, just update item and frequency
        if key in self.cache_data:
            self.cache_data[key] = item
            self._update_frequency(key)
            return

        # Add the new item
        self.cache_data[key] = item
        self.usage_count[key] = 1
        self.frequency_order[key] = None

        # Check if we need to discard an item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # Find the least frequently used keys
            min_freq = min(self.usage_count.values())
            lfu_keys = [
                    k for k in self.cache_data.keys()
                    if self.usage_count[k] == min_freq]

            # If there's a tie, discard the least recently used item amongthem
            if len(lfu_keys) > 1:
                # Using OrderedDict's ordering to determine least recentlyused
                discard_key = next(
                        k for k in self.frequency_order if k in lfu_keys)
            else:
                discard_key = lfu_keys[0]

            # Discard the selected key
            del self.cache_data[discard_key]
            del self.usage_count[discard_key]
            del self.frequency_order[discard_key]
            print(f"DISCARD: {discard_key}")

        # Mark the newly added item as the most recently used of its freq level
        self._update_frequency(key)

    def get(self, key):
        """
        Retrieve an item from the cache by key and update its frequency.
        Args:
            key - key to the data to be retrieved
        Returns:
            Value of the item if found, None if key is None or doesn't exist.
        """
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and return the item
        self._update_frequency(key)
        return self.cache_data[key]

    def _update_frequency(self, key):
        """
        Update the frequency and order of the given key to reflect
        recent access.
        """
        # Increase frequency count
        self.usage_count[key] += 1
        # Move key to the end of frequency_order to mark it most recently used
        if key in self.frequency_order:
            del self.frequency_order[key]
        self.frequency_order[key] = None
