#!/usr/bin/env python3
"""LRU Caching"""

BaseCaching = __import__("base_caching").BaseCaching


class LRUCache(BaseCaching):
    """LRU cache system"""
    def __init__(self):
        """Initialize"""
        super().__init__()
        self.lru = []

    def put(self, key, item):
        """Add item to cache"""
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
                return
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discard = self.lru[0]
                self.cache_data.pop(discard)
                self.lru.pop(0)
                print("DISCARD: {}".format(discard))
            self.cache_data[key] = item
            if key in self.lru:
                self.lru.pop(self.lru.index(key))
            self.lru.append(key)

    def get(self, key):
        """Get item from cache"""
        if key in self.cache_data:
            self.lru.pop(self.lru.index(key))
            self.lru.append(key)
            return self.cache_data[key]
        return None
