#!/usr/bin/env python3
"""
Module to implement Basic Caching using LIFO (Last In First Out) Stack Logic
"""
from base_caching import BaseCaching
from collections import OrderedDict


class LIFOCache(BaseCaching):
    """
    This is a class that inherits from the BaseCaching parent class
    It implements LIFO Stack system for caching
    """
    def __init__(self):
        """Constructor of FIFOCache"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        This is a method that allows adding of key value pair to the cache
        Args:
            key - the key of the data to be added
            item - the value of the data to be added
        """
        if key is not None or item is not None:
            if key not in self.cache_data:
                if (len(self.cache_data) + 1) > BaseCaching.MAX_ITEMS:
                    last_data_key, _ = self.cache_data.popitem(True)
                    print(f"DISCARD: {last_data_key}")
        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=True)

        return

    def get(self, key):
        """
        This is a method that retrieves an item from the cache by the key.
        Args:
            key - key to the data to be retrieved.
        """
        return self.cache_data.get(key, None)
