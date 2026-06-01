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
           
def _main():
    tree = ExpressionTree()

    r = tree.add_root("-")
    rl = tree.add_left(r, "+")
    rll = tree.add_left(rl, "+")
    rlll = tree.add_left(rll, "*")
    rllll = tree.add_left(rlll, "13")
    rlllr = tree.add_right(rlll, "12")
    rllr = tree.add_right(rll, "11")
    rlr = tree.add_right(rl, "+")
    rlrl = tree.add_left(rlr, "-")
    rlrll = tree.add_left(rlrl, "9")
    rlrlr = tree.add_right(rlrl, "5")
    rlrr = tree.add_right(rlr, "2")
    rr = tree.add_right(r, "+")
    rrl = tree.add_left(rr, "*")
    rrll = tree.add_left(rrl, "3")
    rrlr = tree.add_right(rrl, "-")
    rrlrl = tree.add_left(rrlr, "+")
    rrlrll = tree.add_left(rrlrl, "3")
    rrlrlr = tree.add_right(rrlrl, "9")
    rrlrr = tree.add_right(rrlr, "+")
    rrlrrr = tree.add_right(rrlrr, "7")
    rrlrrl = tree.add_left(rrlrr, "3")
    rrr = tree.add_right(rr, "6")

    print(tree, end='')
    print('=',tree.evaluate(tree.root))


if __name__ == '__main__':
    _main()
