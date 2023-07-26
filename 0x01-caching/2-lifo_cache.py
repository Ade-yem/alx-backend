#!/usr/bin/env python3
"""LIFO Caching"""

BaseCaching = __import__("base_caching").BaseCaching


class LIFOCache(BaseCaching):
    """LIFO cache system"""
    def __init__(self):
        """Initialize"""
        super().__init__()

    def put(self, key, item):
        """Add item to cache"""
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
                return
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discard = list(self.cache_data.keys())[-1]
                self.cache_data.pop(discard)
                print("DISCARD: {}".format(discard))
            self.cache_data[key] = item

    def get(self, key):
        """Get item from cache"""
        if key and key in self.cache_data:
            return self.cache_data[key]
        return None
