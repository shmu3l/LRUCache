import json
import logging
import os
import concurrent.futures
import pickle
import urllib.request
import urllib.error
import redis
from rq import Queue
from urllib.parse import urlparse

from app.LRUCache import LRUCache
from app.cache_model import Cacheout


r = redis.Redis()
q = Queue(connection=r)
global_cache = Cacheout()
g_settings = global_cache.get_global_settings()
MAX_THREADS = g_settings["MAX_THREADS"]


def background_processing():
    # limit the amount of threads
    threads = min(MAX_THREADS, len(global_cache.cache))
    print(threads)
    for key in global_cache.cache:
        item = global_cache.cache.get(key)
        item.url_status = "RUNNING"
        global_cache.cache.set(item.uid, item)
    return True
    # I/O functionality use multithreading to get url status
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(check_url_status, global_cache.cache)



# @LRUCache
def check_url_status(uid):
    try:
        data_item = global_cache.cache.get(uid)
        if not urlparse(data_item.url_string).scheme:
            data_item.url_string = 'http://' + data_item.url_string
            conn = urllib.request.urlopen(data_item.url_string)
    except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        data_item.url_status = "ERROR"
        global_cache.cache.set(data_item.uid, data_item)
        return data_item
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        data_item.url_status = "INVALID_URL"
        global_cache.cache.set(data_item.uid, data_item)
        return data_item
    else:
        # 200
        data_item.url_status = "COMPLETE"
        global_cache.cache.set(data_item.uid, data_item)
        return data_item


# TODO: Offline save to pkl
# def save_obj(cache_list):
#     with open(global_settings['CACHE_FILE_NAME'] + '.pkl', 'wb') as f:
#         pickle.dump(cache_list, f, protocol=2)
#
#
# def load_obj():
#     try:
#         with open(global_settings['CACHE_FILE_NAME'] + '.pkl', 'rb') as f:
#             obj = pickle.load(f)
#             return obj
#     except (OSError, IOError) as e:
#         return False
