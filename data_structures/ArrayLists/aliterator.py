class ALIterator:
    def __init__(self, array_list) -> None:
        self.index = 0
        self.list = array_list

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == self.list.size:
            raise StopIteration

        value = self.list.get(self.index)
        self.index += 1
        return value