from aliterator import ALIterator
class ArrayList:
    def __init__(self):
        self.size = 0
        self.capacity = 1
        self.array = [None] * self.capacity

    def __str__(self):
        result = "["
        for i in range(self.size):
            result += str(self.array[i]) + " "
        result += "]"
        return result

    def get_size(self):
        return self.size

    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False

    def set(self, index, element):
        self.array[index] = element

    def get(self, index):
        return self.array[index]

    def expand_array(self):
        print("resizing the array")
        print(self.array)
        new_capacity = self.capacity * 2
        new_array = [None] * new_capacity
        for i in range(self.size):
            new_array[i] = self.array[i]
        self.capacity = new_capacity
        self.array = new_array


    def append(self, element):
        if self.size == self.capacity:
            self.expand_array()
        self.array[self.size] = element
        self.size += 1

    def remove(self, index):
        if index >= self.size:
            raise ValueError("Element Does Not Exist")
        else:
            self.array.remove(index)
            self.size -= 1

    
    # def add(self, index, element):
    #     if self.size == self.capacity:
    #         self.expand_array()
    #     while index >= self.capacity:
    #         self.expand_array()
    #     new_array = [None] * self.capacity
    #     for i in range(index):
    #         new_array[i] = self.array[i]
    #     new_array[index] = element

    #     if index < self.size:
    #         for i in range(index+1, self.size)

    def __iter__(self):
       return ALIterator(self)

