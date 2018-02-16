

class BitMap(object):
    _data = []
    _bit_map = []
    _predicate = None

    def __init__(self, predicate):
        self._data = []
        self._bit_map = []
        self._predicate = predicate

    def add(self, kv):
        self._data.append(kv)
        self._bit_map.append(self._predicate(kv.key))

    def get_predicate_value(self):
        result = []
        for kv, predicate_value in zip(self._data, self._bit_map):
            if predicate_value:
                result.append(kv)
        return result