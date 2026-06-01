"""
Filename: Percolation_donez.py
Author: James Donez
Course: COMP 1353
Assignment: Percolation Project

This program makes random forests and checks if a fire can spread. It uses
DFS, BFS, simulations for fire probability, and makes a graph.
"""

import os
import random

os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


class Cell:
    def __init__(self, row, col):
        self.__row = row
        self.__col = col

    def get_row(self):
        return self.__row

    def get_col(self):
        return self.__col


class Stack:
    def __init__(self):
        self.__stuff = []

    def push(self, value):
        self.__stuff.append(value)

    def pop(self):
        return self.__stuff.pop()

    def is_empty(self):
        return len(self.__stuff) == 0


class Queue:
    def __init__(self):
        self.__stuff = []

    def enqueue(self, value):
        self.__stuff.append(value)

    def dequeue(self):
        return self.__stuff.pop(0)

    def is_empty(self):
        return len(self.__stuff) == 0


class Forest:
    def __init__(self, width, height, d):
        self.__width = width
        self.__height = height
        self.__trees = []

        for r in range(height):
            row = []
            for c in range(width):
                if random.random() < d:
                    row.append(1)
                else:
                    row.append(0)
            self.__trees.append(row)

    def __str__(self):
        answer = ""
        for r in range(self.__height):
            for c in range(self.__width):
                answer += str(self.__trees[r][c]) + " "
            answer += "\n"
        return answer

    def set_trees(self, new_trees):
        self.__trees = new_trees

    def reset_fire(self):
        for r in range(self.__height):
            for c in range(self.__width):
                if self.__trees[r][c] == 2:
                    self.__trees[r][c] = 1

    def depth_first_search(self):
        self.reset_fire()
        spots = Stack()

        # Start trees in the top row on fire.
        for c in range(self.__width):
            if self.__trees[0][c] == 1:
                self.__trees[0][c] = 2
                spots.push(Cell(0, c))

        while not spots.is_empty():
            next_spot = spots.pop()
            r = next_spot.get_row()
            c = next_spot.get_col()

            if r == self.__height - 1:
                return True

            around = [[r - 1, c], [r + 1, c], [r, c - 1], [r, c + 1]]
            for place in around:
                new_r = place[0]
                new_c = place[1]
                if new_r >= 0 and new_r < self.__height:
                    if new_c >= 0 and new_c < self.__width:
                        if self.__trees[new_r][new_c] == 1:
                            self.__trees[new_r][new_c] = 2
                            spots.push(Cell(new_r, new_c))

        return False

    def breadth_first_search(self):
        self.reset_fire()
        spots = Queue()

        # Start trees in the top row on fire.
        for c in range(self.__width):
            if self.__trees[0][c] == 1:
                self.__trees[0][c] = 2
                spots.enqueue(Cell(0, c))

        while not spots.is_empty():
            next_spot = spots.dequeue()
            r = next_spot.get_row()
            c = next_spot.get_col()

            if r == self.__height - 1:
                return True

            around = [[r - 1, c], [r + 1, c], [r, c - 1], [r, c + 1]]
            for place in around:
                new_r = place[0]
                new_c = place[1]
                if new_r >= 0 and new_r < self.__height:
                    if new_c >= 0 and new_c < self.__width:
                        if self.__trees[new_r][new_c] == 1:
                            self.__trees[new_r][new_c] = 2
                            spots.enqueue(Cell(new_r, new_c))

        return False


class FireProbability:
    @staticmethod
    def probability_of_fire_spread_dfs(d):
        made_it = 0

        for num in range(1000):
            woods = Forest(20, 20, d)
            if woods.depth_first_search():
                made_it += 1

        return made_it / 1000

    @staticmethod
    def probability_Of_fire_spread_bfs(d):
        made_it = 0

        for num in range(1000):
            woods = Forest(20, 20, d)
            if woods.breadth_first_search():
                made_it += 1

        return made_it / 1000

    @staticmethod
    def highest_Density_dfs():
        low_density = 0.0
        high_density = 1.0
        density = 0.0

        for num in range(20):
            density = (high_density + low_density) / 2.0
            p = FireProbability.probability_of_fire_spread_dfs(density)

            if p < 0.5:
                low_density = density
            else:
                high_density = density

        return density

    @staticmethod
    def highest_Density_bfs():
        low_density = 0.0
        high_density = 1.0
        density = 0.0

        for num in range(20):
            density = (high_density + low_density) / 2.0
            p = FireProbability.probability_Of_fire_spread_bfs(density)

            if p < 0.5:
                low_density = density
            else:
                high_density = density

        return density


def make_graph():
    densities = []
    fire_probabilities = []

    for num in range(101):
        density = num / 100
        p = FireProbability.probability_of_fire_spread_dfs(density)
        densities.append(density)
        fire_probabilities.append(p)
        print("Density:", density, "Probability:", p)

    plt.plot(densities, fire_probabilities, marker="o", markersize=3)
    plt.title("Probability of Fire Spread Based on Forest Density")
    plt.xlabel("Forest Density")
    plt.ylabel("Probability of Fire Spreading")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True)
    plt.savefig("fire_spread_graph.png")
    plt.close()


if __name__ == "__main__":
    print("Critical density using DFS:", FireProbability.highest_Density_dfs())
    print("Critical density using BFS:", FireProbability.highest_Density_bfs())
    print("Making graph...")
    make_graph()
    print("The graph was saved as fire_spread_graph.png")
