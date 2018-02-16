from .hash_table import HashTable


def create_hash_table(loadfactor=1):
    return HashTable(loadfactor)