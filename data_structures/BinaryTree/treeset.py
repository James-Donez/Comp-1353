class TreeNode:
    def __init__(self, v):
        self.value = v
        self.left = None
        self.right = None
        self.parent = None

    def is_external(self):
        return self.left is None and self.right is None

    def is_internal(self):
        return not self.is_external()

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


class TreeSet:
    def __init__(self):
        self.root = None
        self.size = 0

    def get_size(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def _add_recursive(self, r, v):
        if r is None:
            self.size += 1
            return TreeNode(v)

        if v < r.value:
            r.left = self._add_recursive(r.left, v)
            r.left.parent = r

        elif v > r.value:
            r.right = self._add_recursive(r.right, v)
            r.right.parent = r

        return r

    def add(self, v) -> None:
        self.root = self._add_recursive(self.root, v)
        if self.root is not None:
            self.root.parent = None

    def _discard_recursive(self, r, v):
        if r is None:
            return None

        if v < r.value:
            r.left = self._discard_recursive(r.left, v)
            if r.left is not None:
                r.left.parent = r

        elif v > r.value:
            r.right = self._discard_recursive(r.right, v)
            if r.right is not None:
                r.right.parent = r

        else:
            # Case 1: leaf node
            if r.is_external():
                self.size -= 1
                return None

            # Case 2: one child
            if r.left is None:
                self.size -= 1
                r.right.parent = r.parent
                return r.right

            if r.right is None:
                self.size -= 1
                r.left.parent = r.parent
                return r.left

            # Case 3: two children
            pred = r.left
            while pred.right is not None:
                pred = pred.right

            r.value = pred.value
            r.left = self._discard_recursive(r.left, pred.value)

            if r.left is not None:
                r.left.parent = r

        return r

    def discard(self, v) -> None:
        self.root = self._discard_recursive(self.root, v)
        if self.root is not None:
            self.root.parent = None

    def _contains_recursive(self, r:TreeNode, v):
        if r is None:
            return False
        if r.is_external() and r.value != v:
            return False
        if r.value < v:
            return self._contains_recursive(r.right, v) #type: ignore
        elif r.value > v:
            return self._contains_recursive(r.left, v) #type: ignore
        
        return True
        

    def contains(self, v) -> bool:
        return self._contains_recursive(self.root, v) #type: ignore

    def union(self, other):
        pass

    def intersection(self, other):
        pass

    def _recursive_str(self, r, level):
        if r is None:
            return ""

        return (
            level * "  " + str(r) + "\n"
            + self._recursive_str(r.left, level + 1)
            + self._recursive_str(r.right, level + 1)
        )

    def __str__(self):
        return self._recursive_str(self.root, 0)
    

    def _sorted_recursive(self, r:TreeNode, sorted_values: list):
        if r is None:
            return
        self._sorted_recursive(r.left, sorted_values)
        sorted_values.append(r.value)
        self._sorted_recursive(r.right, sorted_values)
        

    def print_sorted(self):
        sorted_values = []
        self._sorted_recursive(self.root, sorted_values)
        return sorted_values
    
    def _min_recursive(self, r:TreeNode):
        if r is None:
            return None
        if r.left is not None:
            return self._min_recursive(r.left)
        return r.value

    def min(self):
        return self._min_recursive(self.root)
            
    def _max_recursive(self, r:TreeNode):
        if r is None:
            return None
        if r.right is not None:
            return self._max_recursive(r.right)
        return r.value

    def max(self):
        return self._max_recursive(self.root)
