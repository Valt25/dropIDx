import random
from time import time


def test_by_index(data_set, index, method, N_TESTS=1000):
    total_time = 0
    kv = data_set[index]
    for i in range(0, N_TESTS):
        start = time()
        found = method(key=kv.key)
        end = time()
        assert found.value == kv.value
        total_time += (end - start)
    return total_time/N_TESTS


def test_by_size(data_set, step, index_object, N_TESTS=100):
    res = []
    for i in range(0, len(data_set), step):
        total_time = 0

        for k in range(0, step):
            index_object.add(data_set[i+k])
        for k in range(0, N_TESTS):
            index = random.randint(0, i)
            kv = data_set[index]
            start = time()
            found = index_object.search(kv.key)
            end = time()
            assert found.value == kv.value
            total_time += (end - start)
        res.append(total_time / N_TESTS)
        print(i)
    return res


def compare_methods(meth1, meth2, dataset, N_TESTS=1000):
    for d in dataset:
        meth1.add(d)
        meth2.add(d)
    total_time_first = 0

    for i in range(0, N_TESTS):
        index = random.randint(0, len(dataset)-1)
        kv = dataset[index]
        start = time()
        found_value = meth1.search(kv.key)
        end = time()
        assert found_value.value == kv.value
        total_time_first += (end - start)
    total_time_second = 0
    for i in range(0, N_TESTS):
        index = random.randint(0, len(dataset) - 1)
        kv = dataset[index]
        start = time()
        found_value = meth2.search(kv.key)
        end = time()
        assert found_value.value == kv.value
        total_time_second += (end - start)

    print('First algorithm works for %f' % total_time_first)
    print('Second algorithm works for %f' % total_time_second)
    print(total_time_first < total_time_second)
    return total_time_first < total_time_second

