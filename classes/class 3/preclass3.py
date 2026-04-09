
class Node:
    def __init__(self, v):
        self.value = v
        self.next = None
    
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

class CircularLinkedList: 
    def __init__(self):
        self.cursor = None        
        self.size = 0
		

    def removeAfterCursor(self):
        if self.cursor is None:
            raise ValueError("list is empty")	
        if self.cursor.next is self.cursor:
            self.cursor = None
        else:
            self.cursor.next = self.cursor.next.next
        self.size -= 1

    
    def __str__(self):
        if self.size == 0:
                return '[]'

        result = '[' + str(self.cursor) + " "
        temp = self.cursor.next
        while temp is not self.cursor:
            result += str(temp) + " "
            temp = temp.next
            
        return result +']'