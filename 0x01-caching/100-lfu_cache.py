#!/usr/bin/env python3
"""LFU Caching"""

BaseCaching = __import__("base_caching").BaseCaching


class LFUCache(BaseCaching):
    """LFU cache system"""

    def __init__(self):
        """Initialize"""
        super().__init__()
        self.count = {}
    
    def put(self, key, item):
        """Add item to cache"""
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
                if key in self.count:
                    self.count[key] += 1
                else:
                    self.count[key] = 1
                return
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lfu = sorted(self.count.items(), key=lambda x:x[1])
                discard = lfu[0][0]
                self.cache_data.pop(discard)
                self.count.pop(discard)
                print("DISCARD: {}".format(discard))
            self.cache_data[key] = item
            # self.count[key] = 0

    def get(self, key):
        """Get item from cache"""
        if key in self.cache_data:
            if key in self.count:
                self.count[key] += 1
            else:
                self.count[key] = 1
            return self.cache_data[key]
        return None
    
my_cache = LFUCache()
my_cache.put("A", "Hello")
my_cache.put("B", "World")
my_cache.put("C", "Holberton")
my_cache.put("D", "School")
my_cache.print_cache()
print(my_cache.get("B"))
my_cache.put("E", "Battery")
my_cache.print_cache()
my_cache.put("C", "Street")
my_cache.print_cache()
print(my_cache.get("A"))
print(my_cache.get("B"))
print(my_cache.get("C"))
my_cache.put("F", "Mission")
my_cache.print_cache()
my_cache.put("G", "San Francisco")
my_cache.print_cache()
my_cache.put("H", "H")
my_cache.print_cache()
my_cache.put("I", "I")
my_cache.print_cache()
print(my_cache.get("I"))
print(my_cache.get("H"))
print(my_cache.get("I"))
print(my_cache.get("H"))
print(my_cache.get("I"))
print(my_cache.get("H"))
my_cache.put("J", "J")
my_cache.print_cache()
my_cache.put("K", "K")
my_cache.print_cache()
my_cache.put("L", "L")
my_cache.print_cache()
my_cache.put("M", "M")
my_cache.print_cache()