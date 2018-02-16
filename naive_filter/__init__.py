class NaiveFilter(object):
    _data = None
    _predicate = None

    def __init__(self, predicate, input_set=[]):
        self._data = input_set.copy()
        self._predicate = predicate

    def add(self, kv):
        self._data.append(kv)

    def get_predicate_value(self):
        result = []
        for kv in self._data:
            if self._predicate(kv.key):
                result.append(kv)
        return result
