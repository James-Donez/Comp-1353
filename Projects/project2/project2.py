"""
Filename: project2.py
Author: James Donez
Course: COMP 1353
Assignment: Project 2

This program makes random forests and checks if a fire can get from the
top row to the bottom row. It uses a stack for DFS and a queue for BFS.
"""

import random


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col


class Stack:
    def __init__(self):
        self.stuff = []

    def push(self, value):
        self.stuff.append(value)

    def pop(self):
        return self.stuff.pop()

    def is_empty(self):
        return len(self.stuff) == 0


class Queue:
    def __init__(self):
        self.stuff = []

    def enqueue(self, value):
        self.stuff.append(value)

    def dequeue(self):
        return self.stuff.pop(0)

    def is_empty(self):
        return len(self.stuff) == 0


class Forest:
    def __init__(self, width, height, d):
        self.width = width
        self.height = height
        self.trees = []

        for r in range(height):
            line = []
            for c in range(width):
                chance = random.random()
                if chance < d:
                    line.append(1)
                else:
                    line.append(0)
            self.trees.append(line)

    def __str__(self):
        words = ""
        for r in range(self.height):
            for c in range(self.width):
                words += str(self.trees[r][c]) + " "
            words += "\n"
        return words

    def reset_fire(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.trees[r][c] == 2:
                    self.trees[r][c] = 1

    def depth_first_search(self):
        self.reset_fire()
        spots = Stack()

        # Start the fire in the first row.
        for c in range(self.width):
            if self.trees[0][c] == 1:
                self.trees[0][c] = 2
                spots.push(Cell(0, c))

        while not spots.is_empty():
            next_spot = spots.pop()
            r = next_spot.row
            c = next_spot.col

            if r == self.height - 1:
                return True

            around = [[r - 1, c], [r + 1, c], [r, c - 1], [r, c + 1]]
            for new_place in around:
                new_r = new_place[0]
                new_c = new_place[1]
                if new_r >= 0 and new_r < self.height:
                    if new_c >= 0 and new_c < self.width:
                        if self.trees[new_r][new_c] == 1:
                            self.trees[new_r][new_c] = 2
                            spots.push(Cell(new_r, new_c))

        return False

    def breadth_first_search(self):
        self.reset_fire()
        spots = Queue()

        # Start the fire in the first row.
        for c in range(self.width):
            if self.trees[0][c] == 1:
                self.trees[0][c] = 2
                spots.enqueue(Cell(0, c))

        while not spots.is_empty():
            next_spot = spots.dequeue()
            r = next_spot.row
            c = next_spot.col

            if r == self.height - 1:
                return True

            around = [[r - 1, c], [r + 1, c], [r, c - 1], [r, c + 1]]
            for new_place in around:
                new_r = new_place[0]
                new_c = new_place[1]
                if new_r >= 0 and new_r < self.height:
                    if new_c >= 0 and new_c < self.width:
                        if self.trees[new_r][new_c] == 1:
                            self.trees[new_r][new_c] = 2
                            spots.enqueue(Cell(new_r, new_c))

        return False
