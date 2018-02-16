class NaiveSearch(object):
    _data = None

    def __init__(self, input_set=[]):
        self._data = input_set.copy()

    def add(self, kv):
        self._data.append(kv)

    def search(self, key):
        for kv in self._data:
            if kv.key == key:
                return kv
