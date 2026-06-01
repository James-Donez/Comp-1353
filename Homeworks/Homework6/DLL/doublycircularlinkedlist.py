class Node:
    """
    Represents one node in a doubly circular linked list.
    """

    def __init__(self, data=None):
        """
        Creates a new node with optional data.

        Parameters:
            data: The value stored in the node
        """
        self.data = data
        self.prev = None
        self.next = None

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return isinstance(other, Node) and self.data == other.data


class DoublyCircularLinkedList:
    """
    A doubly circular linked list that stores a cursor reference.
    """

    def __init__(self):
        """
        Creates an empty doubly circular linked list.
        """
        self.cursor = None
        self.size = 0

    def add_after_cursor(self, value):
        """
        Adds a new node after the cursor.

        Parameters:
            value: The value to store in the new node
        """
        new_node = Node(value)

        if self.is_empty():
            new_node.next = new_node
            new_node.prev = new_node
            self.cursor = new_node
        else:
            after = self.cursor.next
            new_node.prev = self.cursor
            new_node.next = after
            self.cursor.next = new_node
            after.prev = new_node

        self.size += 1

    def delete_cursor(self):
        """
        Removes the cursor node and returns its value.

        Returns:
            The value stored in the removed node
        """
        if self.is_empty():
            raise IndexError("Cannot delete from an empty list.")

        removed_value = self.cursor.data

        if self.size == 1:
            self.cursor = None
        else:
            before = self.cursor.prev
            after = self.cursor.next
            before.next = after
            after.prev = before
            self.cursor = after

        self.size -= 1
        return removed_value

    def advance_cursor(self, n: int):
        """
        Moves the cursor forward n positions.

        Parameters:
            n (int): Number of positions to move forward
        """
        if self.is_empty() or n < 0:
            return

        for _ in range(n):
            self.cursor = self.cursor.next

    def get_value(self):
        """
        Returns the value at the cursor.

        Returns:
            The value stored at the cursor
        """
        if self.is_empty():
            raise IndexError("Cannot get a value from an empty list.")

        return self.cursor.data

    def is_empty(self):
        """
        Returns whether the list is empty.

        Returns:
            bool: True if the list is empty, otherwise False
        """
        return self.size == 0

    def get_size(self):
        """
        Returns the number of nodes in the list.

        Returns:
            int: The number of nodes in the list
        """
        return self.size
