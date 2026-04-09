class Node:
    def __init__(self, v):
        self.value = v
        self.next = None
        self.prev = None
    
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

class CircularLinkedList: 
    def __init__(self):
        self.cursor = None       
        self.size = 0

    def add_after_cursor(self, v):
        new_node = Node(v)

        if self.cursor is None:
            new_node.next = new_node
            new_node.prev = new_node
            self.cursor = new_node
        else:
            new_node.next = self.cursor.next
            new_node.prev = self.cursor
            self.cursor.next.prev = new_node
            self.cursor.next = new_node

        self.size += 1


    def __str__(self) -> str:
        if self.size == 0:
            return "[]"

        values = [str(self.cursor.value)]
        current = self.cursor.next

        while current is not self.cursor:
            values.append(str(current.value))
            current = current.next

        return "[" + ", ".join(values) + "]"


cll = CircularLinkedList()
cll.add_after_cursor(6)
cll.add_after_cursor(4)


print(cll)