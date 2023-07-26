#!/usr/bin/env python3
"""Basic dictionary"""

BaseCaching = __import__("base_caching").BaseCaching


class BasicCache(BaseCaching):
    """caching system"""
    def __init__(self):
        """initialize"""
        super().__init__()

    def put(self, key, item):
        """add item to cache"""
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """get item from cache"""
        if key and key in self.cache_data:
            return self.cache_data[key]
        return None
