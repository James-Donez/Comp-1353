from random import randint, choice

class HashSet:

    PRIMES = (
        25165843,
        50331653,
        100663319,
        201326611,
        402653189,
        805306457,
        1610612741,
    )

    def __init__(self) -> None:
        self._init_table(16)

    def _init_table(self, cap):
        self.the_table = []
        self.prime = choice(HashSet.PRIMES)
        self.a = randint(1, self.prime - 1)
        self.b = randint(0, self.prime - 1)

        for i in range(cap):
            self.the_table.append([])

        self.size = 0

    def _hash_and_compress(self, value):
        return ((hash(value) * self.a + self.b) % self.prime) % len(self.the_table)
    
    def _expand_table(self):
        old_values = []

        for bucket in self.the_table:
            for value in bucket:
                old_values.append(value)

        old_cap = len(self.the_table)

        self._init_table(old_cap * 2)

        for value in old_values:
            self.add(value)

    def get_size(self):
        i = 0
        for bucket in self.the_table:
            for value in bucket:
                i += 1
        return i
    
    def add(self, value):
        index = self._hash_and_compress(value)
        bucket = self.the_table[index]

        if value not in bucket:
            bucket.append(value)
            self.size += 1
        
        if self.size / len(self.the_table) > 0.75:
            self._expand_table()
    
    def discard(self, value):
        index = self._hash_and_compress(value)
        bucket = self.the_table[index]

        if value in bucket:
            bucket.remove(value)
            self.size -= 1
    
    def contains(self, value):
        index = self._hash_and_compress(value)
        bucket = self.the_table[index]

        return value in bucket

    def union(self, other):
        if self.size <= 0 or other.size <= 0:
            raise IndexError
        
        for thing in other:
            if self.contains(thing):
                pass
            else:
                self.add(thing)
        

    def intersection(self, other):
        if self.size <= 0 or other.size <= 0:
            raise IndexError
        
        temp = []
        for thing in self:
            temp.append(thing)

        for val in temp:
            if not other.contains(val):
                self.discard(val)
        return

    def difference(self, other):
        if self.size <= 0 or other.size <= 0:
            raise IndexError
        
        temp = []
        for thing in self:
            temp.append(thing)

        for val in temp:
            if other.contains(val):
                self.discard(val)
        return

    def __iter__(self):
        values = []

        for bucket in self.the_table:
            for value in bucket:
                values.append(value)

        return iter(values)

    def __str__(self) -> str:
        values = []

        for bucket in self.the_table:
            for value in bucket:
                values.append(str(value))

        return "{" + ", ".join(values) + "}"

