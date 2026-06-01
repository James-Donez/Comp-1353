class TreeNode:
    def __init__(self, data, parent = None) -> None:
        self.data = data
        self.right, self.left = None, None
        self.parent = parent

    def node_height(self):
        if self.left is None and self.right is None:
            return 0

        left_height = -1 if self.left is None else self.left.node_height()
        right_height = -1 if self.right is None else self.right.node_height()
        return 1 + max(left_height, right_height)

class BinaryTree:
    def __init__(self, root = None) -> None:
        if root is not None:
            self.root = TreeNode(root)
        else:
            self.root = None

    def insert(self, data):
        node = TreeNode(data)
        if self.root is None:
            self.root = node
            return
        current = self.root

        while True:
            if data <= current.data:
                if current.left is None:
                    current.left = node #type: ignore
                    node.parent = current
                    return
                current = current.left
            elif data > current.data:
                if current.right is None:
                    current.right = node #type: ignore
                    node.parent = current
                    return
                current = current.right
        
    def find_node(self, value):
        if self.root is None:
            return     
        
        current = self.root
        while True:
            if value <= current.data: #type: ignore
                if value == current.data: #type: ignore
                    return current
                current = current.left #type: ignore
            else:
                if value == current.data: #type: ignore
                    return current
                current = current.right #type: ignore

            

    def ancestors(self, node):

        num = []
        curnode = self.find_node(node)

        if curnode.parent is None: #type: ignore
            return curnode.data #type: ignore

        while True:
            num.append(curnode.data) #type: ignore
            if curnode.parent is None: #type: ignore
                result = " ".join(str(item) for item in num)
                return result
            curnode = curnode.parent #type: ignore

    def node_depth(self, node: TreeNode):
        if node is None:
            return -1
        curnode = node
        i=0

        while curnode.parent is not None:
            i += 1
            curnode = curnode.parent
        
        return i

    def tree_height(self):
        if self.root is None:
            return -1

        return self.root.node_height()
    
    def add_root(self, data):
        self.root = TreeNode(data)
        return self.root

    # Add left child
    def add_left(self, node, data):
        node.left = TreeNode(data, parent=node)
        return node.left

    # Add right child
    def add_right(self, node, data):
        node.right = TreeNode(data, parent=node)
        return node.right

            
        
