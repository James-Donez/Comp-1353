"""
Testing code for project2.py.
"""

import random

from project2 import Forest


def test_random_forests():
    print("Testing random forests")

    random.seed(1353)
    lots_of_trees = Forest(20, 20, 0.75)
    dfs_answer = lots_of_trees.depth_first_search()
    bfs_answer = lots_of_trees.breadth_first_search()
    print("Density 0.75 DFS spreads:", dfs_answer)
    print("Density 0.75 BFS spreads:", bfs_answer)
    assert dfs_answer is True
    assert bfs_answer is True

    random.seed(1353)
    not_many_trees = Forest(20, 20, 0.30)
    dfs_answer = not_many_trees.depth_first_search()
    bfs_answer = not_many_trees.breadth_first_search()
    print("Density 0.30 DFS spreads:", dfs_answer)
    print("Density 0.30 BFS spreads:", bfs_answer)
    assert dfs_answer is False
    assert bfs_answer is False
    print()


def test_all_trees_and_no_trees():
    print("Testing forests with all trees or no trees")

    all_trees = Forest(5, 5, 1.0)
    print("All trees DFS spreads:", all_trees.depth_first_search())
    print("All trees BFS spreads:", all_trees.breadth_first_search())
    assert all_trees.depth_first_search() is True
    assert all_trees.breadth_first_search() is True

    no_trees = Forest(5, 5, 0.0)
    print("No trees DFS spreads:", no_trees.depth_first_search())
    print("No trees BFS spreads:", no_trees.breadth_first_search())
    assert no_trees.depth_first_search() is False
    assert no_trees.breadth_first_search() is False
    print()


def test_ones_i_made():
    print("Testing forests I made myself")

    has_path = Forest(4, 4, 0.0)
    has_path.trees = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
    ]
    print("Forest with a path DFS spreads:", has_path.depth_first_search())
    print("Forest with a path BFS spreads:", has_path.breadth_first_search())
    assert has_path.depth_first_search() is True
    assert has_path.breadth_first_search() is True

    no_path = Forest(4, 4, 0.0)
    no_path.trees = [
        [1, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
    ]
    print("Forest without a path DFS spreads:", no_path.depth_first_search())
    print("Forest without a path BFS spreads:", no_path.breadth_first_search())
    assert no_path.depth_first_search() is False
    assert no_path.breadth_first_search() is False
    print()


def test_one_row_forest():
    print("Testing a forest that has one row")

    one_tree = Forest(3, 1, 0.0)
    one_tree.trees = [[0, 1, 0]]
    assert one_tree.depth_first_search() is True
    assert one_tree.breadth_first_search() is True
    print("One-row forest with a tree spreads: True")

    one_empty_row = Forest(3, 1, 0.0)
    assert one_empty_row.depth_first_search() is False
    assert one_empty_row.breadth_first_search() is False
    print("One-row empty forest spreads: False")
    print()


if __name__ == "__main__":
    test_random_forests()
    test_all_trees_and_no_trees()
    test_ones_i_made()
    test_one_row_forest()
    print("All tests passed.")
