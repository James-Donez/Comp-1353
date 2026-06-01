class iterationSSL():
    def __init__(self, start_node):
        self.current = start_node

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration

        value = self.current.value
        self.current = self.current.next
        return value