from dlliterator import DLLIterator
class Node:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None
    
    def __str__(self) -> str:
        return str(self.data)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        return self.data == other.data

class DoublyLinkedList:
    def __init__(self):
        self.header = Node()  # sentinel node at the beginning
        self.tailer = Node()  # sentinel node at the end
        self.header.next = self.tailer
        self.tailer.prev = self.header
        self.size = 0

   
    def __str__(self) -> str:
        values = []
        current = self.header.next

        while current != self.tailer:
            values.append(str(current.data))
            current = current.next

        return "[" + ", ".join(values) + "]"

    def __repr__(self) -> str:
        return self.__str__()
    

    def remove_between(self, node1, node2):

        if node1 is None or node2 is None:
            raise ValueError("A given node is None")

        if node1.next.next != node2 or node2.prev.prev != node1:
            raise ValueError("The distance between is not 1 Node")

        value = node1.next.data

        node1.next = node2
        node2.prev = node1

        self.size -= 1

        return value

    def add_first(self, v):
        new = Node(v)
        after = self.header.next
        new.prev = self.header
        new.next = after
        self.header.next = new
        after.prev = new
        self.size += 1

    def add_last(self, v):
        new = Node(v)
        prev = self.tailer.prev
        new.next = self.tailer
        new.prev = prev
        self.tailer.prev = new
        prev.next = new
        self.size += 1

    def search(self, value):
        current = self.header.next
        index = 0

        while current is not self.tailer:
            if current.data == value:
                return index

            current = current.next
            index += 1

        return -1
    
    def get_size(self):
        return self.size

    def first(self):
        return self.header.next.data
    
    def last(self):
        return self.tailer.prev.data
    
    def remove_first(self):
        value = self.header.next.data
        self.header.next.next.prev = self.header
        self.header.next = self.header.next.next

        self.size -= 1

        return value
    
    def remove_last(self):
        value = self.tailer.prev.data
        self.tailer.prev.prev.next = self.tailer
        self.tailer.prev = self.tailer.prev.prev

        self.size -= 1

        return value
    
    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False
        
    def get(self,index: int):
        current = self.header.next
        for i in range(index):
            current = current.next
        return current.data
    
    def remove_first(self):
        if self.is_empty():
            raise IndexError("List is empty")
        value = self.header.next.data
        self.header.next.next.prev = self.header
        self.header.next = self.header.next.next
        self.size -= 1
        return value
    
    def remove_last(self):
        if self.is_empty():
            raise IndexError("List is empty")
        value = self.tailer.prev.data
        self.tailer.prev.prev.next = self.tailer
        self.tailer.prev = self.tailer.prev.prev
        self.size -= 1
        return value
    
    def __iter__(self):
        return DLLIterator(self.header.next, self.tailer)
    
