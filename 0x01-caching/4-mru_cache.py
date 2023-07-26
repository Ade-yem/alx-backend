#!/usr/bin/env python3
"""MRU Caching"""

BaseCaching = __import__("base_caching").BaseCaching


class MRUCache(BaseCaching):
    """MRU cache system"""
    def __init__(self):
        """Initialize"""
        super().__init__()
        self.mru = []

    def put(self, key, item):
        """Add item to cache"""
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
                self.mru.pop(self.mru.index(key))
                self.mru.append(key)
                return
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discard = self.mru[-1]
                self.cache_data.pop(discard)
                self.mru.pop(-1)
                print("DISCARD: {}".format(discard))
            self.cache_data[key] = item
            self.mru.append(key)

    def get(self, key):
        """Get item from cache"""
        if key in self.cache_data:
            self.mru.pop(self.mru.index(key))
            self.mru.append(key)
            return self.cache_data[key]
        return None
