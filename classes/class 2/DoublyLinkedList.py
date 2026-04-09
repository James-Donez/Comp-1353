
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
	# check if either node1 or node2 is None. Raise a ValueError if so.
    if node1 is None or node2 is None:
        raise ValueError("A given node is None")
	# Check that node1 and node 2 has exactly 1 node between them, 
    # raise a ValueError if not
    if node1.next.next != node2 or node2.prev.prev != node1:
        raise ValueError("The distance between is not 1 Node")
	# Everything is in order, so delete the node between node1 and node2, 
    # returning the value that was stored in it
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



