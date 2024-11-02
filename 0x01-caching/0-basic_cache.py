#!/usr/bin/env python3
"""
Module to implement Basic Caching
"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache is a caching system that inherits from BaseCaching.
    This caching system has no limit on the number of items it can store.
    """

    def put(self, key, item):
        """
        Add an item in the cache.
        If key or item is None, do nothing.
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
        Get an item by key from the cache.
        Return None if key is None or if key doesn't exist in cache.
        """
        return self.cache_data.get(key, None)
