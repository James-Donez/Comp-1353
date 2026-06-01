from random import choice, randint

import numpy as np

from DLL.DoublyLinkedList import DoublyLinkedList


class Item:
    def __init__(self, k, v):
        self.key = k
        self.value = v

    def __str__(self):
        return f"{self.key}: {self.value}"

    def __repr__(self):
        return str(self)

    def set_value(self, new_value):
        old_value = self.value
        self.value = new_value
        return old_value


class HashMap:
    PRIMES = (
        25165843,
        50331653,
        100663319,
        201326611,
        402653189,
        805306457,
        1610612741,
    )

    def __init__(self):
        self._init_table(16)

    def _init_table(self, new_capacity):
        self.the_table = np.empty(new_capacity, dtype=DoublyLinkedList)
        self.prime = choice(HashMap.PRIMES)
        self.a = randint(1, self.prime - 1)
        self.b = randint(0, self.prime - 1)
        self.size = 0

        # Create all buckets.
        for i in range(len(self.the_table)):
            self.the_table[i] = DoublyLinkedList()

    def _expand_table(self):
        old_items = self.items()
        old_cap = len(self.the_table)

        self._init_table(old_cap * 2)

        for item in old_items:
            self.put(item.key, item.value)

    def _hash_and_compress(self, k):
        return (hash(k) * self.a + self.b) % self.prime % len(self.the_table)

    def get(self, k):
        # Get the bucket where the key could exist.
        index = self._hash_and_compress(k)
        bucket = self.the_table[index]

        for item in bucket:
            if item.key == k:
                return item.value

        return None

    def put(self, k, v):
        index = self._hash_and_compress(k)
        bucket = self.the_table[index]

        for item in bucket:
            if item.key == k:
                # Replace the value and return the old value.
                return item.set_value(v)

        new_item = Item(k, v)
        bucket.add_first(new_item)
        self.size += 1

        if self.size / len(self.the_table) > 0.75:
            self._expand_table()

        return None

    def remove(self, k):
        index = self._hash_and_compress(k)
        bucket = self.the_table[index]

        current = bucket.header.next

        while current != bucket.tailer and current.data.key != k:
            current = current.next

        if current != bucket.tailer:
            removed_item = bucket.remove_between(current.prev, current.next)
            self.size -= 1
            return removed_item.value

        return None

    # Iterable methods
    def keys(self):
        the_keys = []

        for bucket in self.the_table:
            for item in bucket:
                the_keys.append(item.key)

        return the_keys

    def values(self):
        return [item.value for bucket in self.the_table for item in bucket]

    def items(self):
        return [item for bucket in self.the_table for item in bucket]

    # Size methods
    def get_size(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def __iter__(self):
        return iter(self.keys())

    def __str__(self):
        return str(self.items())

    def output_table_info(self):
        max_bucket_size = 0

        for i in range(len(self.the_table)):
            print(f"{i}: {self.the_table[i]}")
            if self.the_table[i].size > max_bucket_size:
                max_bucket_size = self.the_table[i].size

        print("Size of largest bucket: ", max_bucket_size)
        print("Table size: ", self.size)
        print("Load factor: ", self.size / len(self.the_table))


def main():
    HashMap()


if __name__ == "__main__":
    main()
