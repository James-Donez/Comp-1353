"""
    Description of program: Checks whether parentheses, brackets, and braces
    are balanced in a given line of text by using a stack built from a doubly
    linked list
    Filename: homework3.py
    Author: James Donez
    Date: 4/19/26
    Course: COMP 1353
    Assignment: Homework 3
    Collaborators: None
    Internet Source: None
"""


class Node:
    """
    Stores one value in the doubly linked list.
    """

    def __init__(self, data=None):
        """
        Creates a node with optional data and links on both sides.

        Parameters:
            data: The value stored in the node
        """
        self.data = data
        self.prev = None
        self.next = None

    def __str__(self) -> str:
        """
        Returns the node data as a string.
        """
        return str(self.data)

    def __repr__(self) -> str:
        """
        Returns the printable representation of the node.
        """
        return self.__str__()


class DoublyLinkedList:
    """
    Stores values in a list with links in both directions.
    """

    def __init__(self):
        """
        Creates an empty doubly linked list with header and tailer sentinels.
        """
        self.header = Node()
        self.tailer = Node()
        self.header.next = self.tailer
        self.tailer.prev = self.header
        self.size = 0

    def __str__(self) -> str:
        """
        Returns the list contents in bracket form.
        """
        values = []
        current = self.header.next

        while current is not self.tailer:
            values.append(str(current.data))
            current = current.next

        return "[" + ", ".join(values) + "]"

    def __repr__(self) -> str:
        """
        Returns the printable representation of the list.
        """
        return self.__str__()

    def add_last(self, value):
        """
        Adds a new value to the back of the list.

        Parameters:
            value: The value to add
        """
        new_node = Node(value)
        previous = self.tailer.prev
        new_node.prev = previous
        new_node.next = self.tailer
        previous.next = new_node
        self.tailer.prev = new_node
        self.size += 1

    def remove_last(self):
        """
        Removes and returns the last value in the list.

        Returns:
            The value that was removed from the back of the list
        """
        if self.is_empty():
            raise IndexError("List is empty")

        value = self.tailer.prev.data
        self.tailer.prev.prev.next = self.tailer
        self.tailer.prev = self.tailer.prev.prev
        self.size -= 1
        return value

    def is_empty(self):
        """
        Returns whether the list contains no values.

        Returns:
            bool: True if the list is empty, otherwise False
        """
        return self.size == 0


class Stack:
    """
    Stores values in last-in, first-out order.
    """

    def __init__(self):
        """
        Creates an empty stack backed by a doubly linked list.
        """
        self.list = DoublyLinkedList()

    def push(self, value):
        """
        Adds a value to the top of the stack.

        Parameters:
            value: The value to push onto the stack
        """
        self.list.add_last(value)

    def pop(self):
        """
        Removes and returns the top value from the stack.

        Returns:
            The value removed from the top of the stack
        """
        return self.list.remove_last()

    def is_empty(self):
        """
        Returns whether the stack has no values.

        Returns:
            bool: True if the stack is empty, otherwise False
        """
        return self.list.is_empty()


def is_balanced(line: str):
    """
    Checks whether brackets in a line are balanced and properly nested.

    Parameters:
        line (str): The line of text to examine

    Returns:
        bool: True if the brackets are balanced, otherwise False
    """
    stack = Stack()
    openers = ["(", "[", "{"]
    closers = [")", "]", "}"]

    for char in line:
        if char in openers:
            stack.push(char)
        elif char in closers:
            if stack.is_empty():
                return False
            closer_index = closers.index(char)
            if stack.pop() != openers[closer_index]:
                return False

    return stack.is_empty()


if __name__ == "__main__":
    """
    Runs sample test cases for the balanced-brackets function.
    """
    true_cases = [
        "({}){}{[()()](())}",
        "(\"I know\", she said (though she said it uncertainly))",
        "x*{3+5*[2+4(x-2)]-6}",
        "primes = [num for num in range(min,max) if 0 not in [num%i for i in range(2,int(num/2)+1)]]",
    ]

    false_cases = [
        "{(})",
        ")What? (I don't know)",
        "{x+3](2-x]+4}",
        "public static void main(String[] args) {",
    ]

    print("Expected True:")
    for case in true_cases:
        print(is_balanced(case), "-", case)

    print("\nExpected False:")
    for case in false_cases:
        print(is_balanced(case), "-", case)
