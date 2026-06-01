from .DoublyLinkedList import DoublyLinkedList


class Stack:
    def __init__(self):
        self.list = DoublyLinkedList()

    def push(self, value):
        self.list.add_last(value)

    def pop(self):
        value = self.list.remove_last()
        return value

    def is_empty(self):
        return self.list.is_empty()
