from app import settings
from app.cache_model import Cacheout


class Node:
    # Head-> [prev,A,next] <-> [prev,B,next] <-> [prev,C,next] -> NULL
    # NULL <- prev
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None


class LRUCache:
    # first init - connect head and tail
    limit_cache_num = Cacheout.cache_ttl

    def __init__(self, func):
        self.func = func
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    # efficient way to use class use as a function
    def __call__(self, *args, **kwargs):
        # in cache? pull result
        if args in self.cache:
            self.cache_on_list(args)
            return self.cache[args]
        # if cache is full (limit_cache_num) - remove least recently used node + dict
        if self.limit_cache_num is not None:
            if len(self.cache) > self.limit_cache_num:
                node = self.head.next
                self._remove(node)
                del self.cache[node.key]
        # after all if not in cache, save dict and create new node
        result = self.func(*args, **kwargs)
        self.cache[args] = result
        node = Node(args, result)
        self._add(node)
        # self.print_cache()
        return result

    def __str__(self):
        # for testing - print double linked list [0,items,0]
        res = ""
        ptr = self.head
        while ptr:
            res += str(ptr.val) + ", "
            ptr = ptr.next
        res = res.strip(", ")
        if len(res):
            return "[" + res + "]"
        else:
            return "[]"

    def cache_on_list(self, args):
        current = self.head
        while True:
            # if exists remove old add new
            if current.key == args:
                node = current
                self._remove(node)
                self._add(node)
                break
            else:
                current = current.next

    def _remove(self, node):
        n = node.next
        p = node.prev
        p.next = n
        n.prev = p

    def _add(self, node):
        p = self.tail.prev
        p.next = node
        self.tail.prev = node
        node.prev = p
        node.next = self.tail

    def print_cache(self):
        print(self)
