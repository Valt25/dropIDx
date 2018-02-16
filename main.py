from time import time
from hash_index import create_hash_table
from btree_index import create_tree
from utils import KeyValue
import random
from utils.test_performace import test_by_index, test_by_size, compare_methods
from utils.test_filter_performance import compare_methods as compare_filters
from naive_search import NaiveSearch
from naive_filter import NaiveFilter
from bitmap_index.BitMap import BitMap


def create_test_set(N=10000):
    result = []
    for i in range(0, N):
        kv = KeyValue(i, random.randint(0, N))
        result.append(kv)
    return result


def odd_predicate(obj):
    return hash(obj) >> 10 > 15

test_set = create_test_set(100000)


naive_search = NaiveSearch()
hash_map = create_hash_table(10)
print('First method is hash map index. And the second one is naive search')
compare_methods(hash_map, naive_search, test_set)
print()

naive_search = NaiveSearch()
btree = create_tree(10)
print('The first method is Btree index. And the second one is naive search')
compare_methods(btree, naive_search, test_set)

print()
hash_map = create_hash_table(10)
btree = create_tree(10)
print('The first method is Btree index. And the second one is hash map index')
compare_methods(btree, hash_map, test_set)

print()
# btree = create_tree(3)
#
#
# res = test_by_size(test_set, 100, btree)
#
# for i in range(0, len(res)):
#     print('%d %f' % (i, res[i]))
naive_search = NaiveFilter(odd_predicate)
bit_map = BitMap(odd_predicate)
print('The first method is bit map index. And the second one is naive filter')
compare_filters(bit_map, naive_search, test_set)


# for t in test_set:
#     btree.add(t)
#
# for t in test_set:
#     btree.search(t.key)



# naive_search = NaiveSearch()
#
# compare_methods(btree, naive_search, test_set)

