from Bitree import BinaryTree


def test_heights():
    empty = BinaryTree()
    assert empty.tree_height() == -1

    single = BinaryTree()
    single_root = single.add_root(10)
    assert single_root.node_height() == 0
    assert single.tree_height() == 0

    balanced = BinaryTree()
    root = balanced.add_root(1)
    left = balanced.add_left(root, 2)
    right = balanced.add_right(root, 3)
    balanced.add_left(left, 4)
    balanced.add_right(left, 5)
    balanced.add_left(right, 6)
    balanced.add_right(right, 7)
    assert left.node_height() == 1
    assert right.node_height() == 1
    assert root.node_height() == 2
    assert balanced.tree_height() == 2

    uneven = BinaryTree()
    root = uneven.add_root(20)
    child = uneven.add_right(root, 30)
    grandchild = uneven.add_right(child, 40)
    leaf = uneven.add_left(grandchild, 35)
    assert leaf.node_height() == 0
    assert child.node_height() == 2
    assert root.node_height() == 3
    assert uneven.tree_height() == 3


test_heights()
print("All height tests passed.")
