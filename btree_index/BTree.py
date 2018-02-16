from utils import KeyValue


class BNode(object):
    _values = None
    _children = None
    _tree_factor = 0
    _data = None
    _parent = None

    def __init__(self, tree_factor, values=[], children=[], data=[], parent = None):
        self._values = values
        self._children = children
        self._tree_factor = tree_factor
        self._data = data
        self._parent = None

    def find(self, key):
        if len(self._children) != 0:
            if len(self._values) != 0:
                child_to_search = 0
                while child_to_search < len(self._values) and key >= self._values[child_to_search]:
                    if self._values[child_to_search] == key:
                        return KeyValue(self._values[child_to_search], self._data[child_to_search])
                    child_to_search += 1
                return self._children[child_to_search].find(key)
            else:
                return None
        else:
            for f_key, value in zip(self._values, self._data):
                if f_key == key:
                    return KeyValue(f_key, value)
            return None

    def add(self, kv):
        if len(self._children) == 0:
            if not self._update(kv):
                if len(self._values) == 2 * self._tree_factor - 1:
                    to_parent, left, right = self._split()
                    self._parent.add_sub_tree(to_parent, left, right)
                    if kv.key > to_parent.key:
                        right.add(kv)
                    else:
                        left.add(kv)
                else:
                    index_to_add = self._get_index_to_insert(kv)
                    self._values.insert(index_to_add, kv.key)
                    self._data.insert(index_to_add, kv.value)
        else:
            assert self._update(kv)

    def add_sub_tree(self, to_parent, left, right):
        if len(self._values) == 2*self._tree_factor - 1:
            new_to_parent, new_left, new_right = self._split()
            self._parent.add_sub_tree(new_to_parent, new_left, new_right)
            if to_parent.key > new_to_parent.key:
                new_right.add_sub_tree(to_parent, left, right)
            else:
                new_left.add_sub_tree(to_parent, left, right)
        else:
            index_to_add = self._get_index_to_insert(to_parent)
            self._values.insert(index_to_add, to_parent.key)
            self._data.insert(index_to_add, to_parent.value)
            del self._children[index_to_add]
            self._children.insert(index_to_add, right)
            self._children.insert(index_to_add, left)
            self._set_parent()

    def _get_index_to_insert(self, to_parent):
        index_to_add = 0
        while index_to_add < len(self._values) and to_parent.key > self._values[index_to_add]:
            index_to_add += 1
        return index_to_add

    def _split(self):
        median_index = len(self._values) // 2
        left_values = self._values[0:median_index]
        left_data = self._data[0:median_index]
        left_children = self._children[0:median_index+1]
        right_values = self._values[median_index+1:]
        right_data = self._data[median_index+1:]
        right_children = self._children[median_index+1:]
        left = BNode(self._tree_factor, left_values, left_children, left_data, self._parent)
        right = BNode(self._tree_factor, right_values, right_children, right_data, self._parent)
        to_parent = KeyValue(self._values[median_index], self._data[median_index])
        return to_parent, left, right

    def _set_parent(self):
        for child in self._children:
            child._parent = self

    def _update(self, kv):
        for i in range(0, len(self._values)):
            if self._values[i] == kv.key:
                self._data[i] = kv.value
                return True

    def find_node(self, key):
        if len(self._children) != 0:
            if len(self._values) != 0:
                child_to_search = 0
                while child_to_search < len(self._values) and key >= self._values[child_to_search]:
                    if self._values[child_to_search] == key:
                        return self
                    child_to_search += 1
                return self._children[child_to_search].find_node(key)
            else:
                print('fail')
                return None
        else:
            return self


# class LeafNode(BNode):
#     def find(self, key):
#
#
#     def find_node(self, key):
#         return self
#
#     def add(self, kv):
#         if not self._update(kv):
#             if len(self._values) == 2 * self._tree_factor - 1:
#                 to_parent, left, right = self._split()
#                 self._parent.add_sub_tree(to_parent, left, right)
#                 if kv.key > to_parent.key:
#                     right.add(kv)
#                 else:
#                     left.add(kv)
#             else:
#                 index_to_add = self._get_index_to_insert()
#                 self._values.insert(index_to_add, kv.key)
#                 self._data.insert(index_to_add, kv.value)
#
#     def _split(self):
#         median_index = len(self._values)//2
#         left_values = self._values[0:median_index]
#         left_data = self._data[0:median_index]
#         right_values = self._values[median_index+1:]
#         right_data = self._data[median_index+1:]
#         left = LeafNode(self._tree_factor, left_values, [], left_data, self._parent)
#         right = LeafNode(self._tree_factor, right_values, [], right_data, self._parent)
#         to_parent = KeyValue(self._values[median_index], self._data[median_index])
#         return to_parent, left, right
#

class RootNode(BNode):
    _tree = None

    def set_tree(self, tree):
        self._tree = tree

    def add(self, kv):
        if len(self._children) == 0:
            if not self._update(kv):
                if len(self._values) == 2 * self._tree_factor - 1:
                    new_to_parent, new_left, new_right = self._split()
                    new_root = RootNode(self._tree_factor, [new_to_parent.key], [new_left, new_right],
                                        [new_to_parent.value])
                    new_root._set_parent()
                    new_root.set_tree(self._tree)
                    self._tree.set_root(new_root)

                    if kv.key > new_to_parent.key:
                        new_right.add(kv)
                    else:
                        new_left.add(kv)
                else:
                    index_to_add = self._get_index_to_insert(kv)
                    self._values.insert(index_to_add, kv.key)
                    self._data.insert(index_to_add, kv.value)
        else:
            assert self._update(kv)

    def add_sub_tree(self, to_parent, left, right):
        if len(self._values) == 2*self._tree_factor - 1:
            new_to_parent, new_left, new_right = self._split()
            new_root = RootNode(self._tree_factor, [new_to_parent.key], [new_left, new_right], [new_to_parent.value])
            new_left._parent = new_root
            new_right._parent = new_root
            new_root.set_tree(self._tree)
            self._tree.set_root(new_root)

            if to_parent.key > new_to_parent.key:
                new_right.add_sub_tree(to_parent, left, right)
            else:
                new_left.add_sub_tree(to_parent, left, right)
        else:
            index_to_add = self._get_index_to_insert(to_parent)
            self._values.insert(index_to_add, to_parent.key)
            self._data.insert(index_to_add, to_parent.value)
            del self._children[index_to_add]
            self._children.insert(index_to_add, right)
            self._children.insert(index_to_add, left)
            self._set_parent()


    def find_node(self, key):
        if len(self._children) != 0:
            return super(RootNode, self).find_node(key)
        else:
            return self


class BTree(object):
    _root = None
    size = 0

    def __init__(self, tree_factor):
        self._root = RootNode(tree_factor)
        self._root.set_tree(self)

    def set_root(self, new_root):
        self._root = new_root

    def search(self, key):
        return self._root.find(key)

    def add(self, kv):
        node = self._root.find_node(kv.key)
        node.add(kv)
        self.size += 1
