from Bitree import BinaryTree

class ExpressionTree(BinaryTree):
    def __str__(self)->str:
        """
        Returns the expression tree as a string.
        Returns:
            str: The full expression stored in the tree
        """
        return self._str_helper(self.root)
    
    def _str_helper(self,node)->str:
        """
        Recursively builds the string for the expression tree.
        Parameters:
            node: The current node in the expression tree
        Returns:
            str: The expression string from the current node
        """
        if node is None:
            return ""
        if node.left is None and node.right is None:
            return str(node.data)
        return f"({self._str_helper(node.left)}{node.data}{self._str_helper(node.right)})"
        
    def evaluate(self,node)->float:
        """
        Recursively evaluates the expression tree.
        Parameters:
            node: The current node in the expression tree
        Returns:
            float: The calculated value of the expression
        """
        if node.left is None and node.right is None:
            return float(node.data)
        
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if node.data == "+":
            return left + right
        if node.data == "-":
            return left - right
        if node.data == "*":
            return left * right
        if node.data == "/":
            return left / right

        raise ValueError(f"Unknown operator: {node.data}")