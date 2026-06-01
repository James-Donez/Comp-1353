class DLLIterator():
    def __init__(self, start_node, end_node):
        self.current = start_node
        self.end = end_node

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current == self.end:
            raise StopIteration
        
        value = self.current.data
        self.current = self.current.next
        return value