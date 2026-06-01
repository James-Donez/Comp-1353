from ssliterator import iterationSSL

class Node:
    def __init__(self, v, n = None):
        self.value = v
        self.next = n

    def __str__(self):
        return str(self.value)  

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if other == None:
            return False
        return self.value == other.value

class SinglyLinkedList:

    def __init__(self):
        self.head = None
        self.size = 0

    def get_size(self):
        return self.size
    
    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False

    def __str__(self):
        result = "["
        current = self.head
        while current is not None:
            result += str(current.value)
            current = current.next
            if current is not None:
                result += " "
        return result + "]"

    def add_first(self, n):
        self.head = Node(n, self.head)
        self.size += 1

    def add_last(self, n):
        if self.head is None:
            self.head = Node(n)
            self.size += 1
            return
        new_node = Node(n)
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node
        self.size += 1

    def remove_first(self):
        if self.head is None:
            raise IndexError("Index Error")
        value = self.head.value
        self.head = self.head.next
        self.size -= 1
        return value
    
    def remove_last(self):
        if self.head is None:
            raise IndexError("Index Error")
        current = self.head
        if current.next is None:
            value = current.value
            self.head = None
            self.size -= 1
            return value
        while current.next.next is not None:
            current = current.next
        value = current.next.value
        current.next = None
        self.size -= 1
        return value

    def get(self, index:int):
        if self.head is None:
            return None
        if index >= self.size:
            raise IndexError("Index Error")
        if index < 0:
            raise IndexError("Index Error")
        current = self.head
        for i in range(index):
            current = current.next
        return current.value

    def remove_at_index(self, index: int):
        if self.head is None:
            return None
        if index >= self.size:
            raise IndexError("Index Error")
        if index < 0:
            raise IndexError("Index Error")
        current = self.head
        prev = self.head
        if index == 0:
            value = self.head.value
            self.head = self.head.next
        for i in range(index):
            prev = current
            current = current.next
            value = current.value
        prev.next = current.next
        self.size -= 1
        return value

    def __iter__(self):
        return iterationSSL(self.head)
    
sll_list = SinglyLinkedList()
sll_list.add_first(1)
sll_list.add_first(2)
sll_list.add_first(3)
sll_list.add_first(4)
sll_list.add_first(5)

for value in sll_list:
    print(value)
