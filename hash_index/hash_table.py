from time import time

INIT_BUCKET_SIZE = 10


class Bucket(object):
    _data = None

    def __init__(self):
        self._data = []

    def add_kv(self, kv):
        for entry in self._data:
            if entry.key == kv.key:
                entry.value = kv.value
                return False
        self._data.append(kv)
        return True

    def delete_kv(self, kv):
        for entry in self._data:
            if entry.key == kv.key:
                self._data.remove(entry)
                return

    def search(self, key):
        start = time()
        for entry in self._data:
            if entry.key == key:
                end = time() - start
                return entry
        end = time() - start
        return False

    def items(self):
        return self._data.copy()


class HashTable(object):
    _loadFactor = 1
    _buckets = []
    _size = 0

    def __init__(self, loadfactor=1):
        self._init_buckets(INIT_BUCKET_SIZE)
        self._loadFactor = loadfactor

    def add(self, kv):
        key_hash = hash(kv.key) % len(self._buckets)
        self._buckets[key_hash].add_kv(kv)
        self._size += 1
        if self._get_load_factor() > self._loadFactor:
            self._rebuild_table()

    def delete(self, kv):
        key_hash = hash(kv.key) % len(self._buckets)
        self._buckets[key_hash - 1].delete_kv(kv)
        self._size -= 1

    def search(self, key):
        start = time()
        key_hash = hash(key) % len(self._buckets)
        kv = self._buckets[key_hash].search(key)
        end = time() - start
        return kv

    def _get_load_factor(self):
        return float(self._size) / float(len(self._buckets))

    def _rebuild_table(self):
        old_buckets = self._buckets
        self._init_buckets(int(len(old_buckets)*1.75))
        for old_bucket in old_buckets:
            for item in old_bucket.items():
                self.add(item)

    def _init_buckets(self, init_size):
        for i in range(0, init_size):
            self._buckets.append(Bucket())
    