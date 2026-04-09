# within a singly linked list. Other languages offer ways to
# ensure this. You will learn about that in OOP.
# The next instance variable refers to the next Node in the list,
# when next is None, then this node is the end of the list
class Node:
    def __init__(self, v, n = None):
        self.value = v
        self.next = n

    def __str__(self):
        return str(self.value)  
        # or return f"{self.value}"  
    
    # python has a flaw, that __str__ won't be called when you ask to output
    # a python list, instead __repr__ is called. We'll put this in here in
    # case we ever have a list of Node objects
    def __repr__(self):
        return self.__str__()

    # Two nodes are equal if their values are equal
    def __eq__(self, other):
        return self.value == other.value

# Note that we use CamelCase for class names in python
class SinglyLinkedList:

    def __init__(self):
        self.head = None
        self.size = 0

    def add_first(self, n):
        self.head = Node(n, self.head)
        self.size += 1

    def min(self):
        if self.head is None:
            return None
        
        temp = self.head.value
        current = self.head.next

        while current != None:
            if current < temp:
                temp = current.value
            current = current.next
        
        return temp
    
    def rotate(self, n):
        if n >= 0:
            raise ValueError("ndex out of bounds exception")
        else:
            for i in range(n):
                save = self.head
                self.head = self.head.next
                current = self.head
                while not current.next is None:
                    current = current.next
                save.next = None
                current.next = save


