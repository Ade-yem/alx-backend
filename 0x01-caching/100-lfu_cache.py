#!/usr/bin/env python3
"""LFU Caching"""

BaseCaching = __import__("base_caching").BaseCaching


class LFUCache(BaseCaching):
    """LFU cache system"""

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.__keys = []
        self.__count = {}

    def put(self, key, item):
        """Add an item in the cache"""
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
                self.__count[key] += 1
                self.__keys.remove(key)
            else:
                if len(self.cache_data) >= self.MAX_ITEMS:
                    discard = self.__keys.pop(self.__keys.index(
                        self.get_key()))
                    del self.cache_data[discard]
                    del self.__count[discard]
                    print("DISCARD: {}".format(discard))
                self.__count[key] = 1
            self.__keys.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """Get an item by key"""
        if key and key in self.cache_data:
            self.__count[key] += 1
            self.__keys.remove(key)
            self.__keys.append(key)
            return self.cache_data[key]
        return None

    def get_key(self):
        """Get the key to remove"""
        min_value = min(self.__count.values())
        for key in self.__count:
            if self.__count[key] == min_value:
                return key
        return None
