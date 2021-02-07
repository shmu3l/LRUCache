import json
import os
from cacheout import Cache


class Cacheout:
    global_settings = json.load(open(os.path.join('./app', "static", "settings.json"), "r"))
    cache = Cache()
    cache_ttl = global_settings['CACHE_TTL']

    def set(self, key: str, val: dict):
        self.cache.set(key, val, ttl=self.cache_ttl)

    def get(self, key: str) -> dict:
        if key in self.cache:
            return self.cache.get(key)
        return self.global_settings["STATUSES"]["NOT_FOUND"]

    def get_global_settings(self):
        return self.global_settings