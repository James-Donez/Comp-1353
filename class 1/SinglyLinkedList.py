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
