class Item:
    def __init__(self, k=None, v=None):
        self.key = k
        self.value = v

    def __str__(self):
        return "(" + str(self.key) + ", " + str(self.value) + ")"

    def __repr__(self):
        return self.__str__()


class ArrayMap:
    def __init__(self):
        # initialize underlying storage (list)
        self.the_table = []

    def get_size(self) -> int:
        return len(self.the_table)

    def is_empty(self) -> bool:
       return self.get_size() == 0

    def get(self, k):
        # return value associated with key k
        # return None if not found
        for item in self.the_table:
            if item.key == k:
                return item.value

    def put(self, k, v):
        # if key exists → update value and return old value
        # else → insert new key-value pair and return None
        for item in self.the_table:
            if item.key == k:
                old_value = item.value
                item.value = v
                return old_value

        self.the_table.append(Item(k, v))
        return None

    def remove(self, k):
        # remove item with key k
        # return its value, or None if not found
        for item in self.the_table:
            if item.key == k:
                old_value = item.value
                self.the_table.remove(item)
                return old_value
        return None

    def keys(self):
        # return iterable of all keys
        result = []

        for item in self.the_table:
            result.append(item.key)

        return result

    def values(self):
        result = []

        for values in self.the_table:
            result.append(values.value)

        return result

    def entries(self):
        return list(self.the_table)

    def __iter__(self):
        # allow iteration over keys
        return iter(self.keys())
