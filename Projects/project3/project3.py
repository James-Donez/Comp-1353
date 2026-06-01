"""
    Description of program: Tests three algorithms that determine whether a
    sorted list of integers contains a pair x and -x. The program also times
    the algorithms on worst-case input sizes and saves the results to a CSV.
    Filename: project3.py
    Author: James Donez
    Date: 4/26/26
    Course: COMP 1353
    Assignment: Project 3
    Collaborators: None
    Internet Source: None
"""

import random
import time
import os

os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def sequential_search(numbers):
    """
    Checks for a pair x and -x using a nested sequential search.

    Parameters:
        numbers (list): A sorted list of integers with no zeros

    Returns:
        bool: True if a pair x and -x exists, otherwise False
    """
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == 0:
                return True

    return False


def binary_search(numbers):
    """
    Checks for a pair x and -x using binary search for each number.

    Parameters:
        numbers (list): A sorted list of integers with no zeros

    Returns:
        bool: True if a pair x and -x exists, otherwise False
    """
    for i in range(len(numbers)):
        target = numbers[i] * -1
        start = 0
        end = len(numbers) - 1

        while start <= end:
            mid = (start + end) // 2

            if numbers[mid] == target and mid != i:
                return True
            elif numbers[mid] < target:
                start = mid + 1
            else:
                end = mid - 1

    return False


def two_index_search(numbers):
    """
    Checks for a pair x and -x using indices at both ends of the list.

    Parameters:
        numbers (list): A sorted list of integers with no zeros

    Returns:
        bool: True if a pair x and -x exists, otherwise False
    """
    i = 0
    j = len(numbers) - 1

    while i < j:
        total = numbers[i] + numbers[j]

        if total == 0:
            return True
        elif total < 0:
            i += 1
        else:
            j -= 1

    return False


def make_worst_case_list(n):
    """
    Creates a sorted list with no zeros and no pair x and -x.

    Parameters:
        n (int): The number of integers to put in the list

    Returns:
        list: A sorted worst-case list for the three algorithms
    """
    magnitudes = random.sample(range(1, n * 10), n)
    numbers = []

    for i in range(n):
        if i % 2 == 0:
            numbers.append(magnitudes[i])
        else:
            numbers.append(magnitudes[i] * -1)

    numbers.sort()
    return numbers


def time_algorithm(function, numbers):
    """
    Times how long an algorithm takes to run on a list.

    Parameters:
        function (function): The algorithm function being timed
        numbers (list): The list of integers to search

    Returns:
        tuple: The boolean result and the elapsed time in seconds
    """
    start = time.perf_counter()
    result = function(numbers)
    end = time.perf_counter()

    return result, end - start


def test_algorithms():
    """
    Runs small predetermined tests to verify all three algorithms.
    """
    true_list = [-25] + list(range(1, 50))
    true_list.sort()

    false_list = make_worst_case_list(50)

    print("Predetermined tests")
    print("Algorithm, True List, False List")
    print("Sequential,", sequential_search(true_list), ",", sequential_search(false_list))
    print("Binary,", binary_search(true_list), ",", binary_search(false_list))
    print("Two Index,", two_index_search(true_list), ",", two_index_search(false_list))
    print()


def print_big_oh_analysis():
    """
    Prints the worst-case Big-Oh analysis for the three algorithms.
    """
    print("Big-Oh worst-case analysis")
    print("Sequential Search: O(n^2)")
    print("Binary Search: O(n log n)")
    print("Two Index Search: O(n)")
    print()


if __name__ == "__main__":
    test_algorithms()
    print_big_oh_analysis()

    input_sizes = [5000, 10000, 20000, 40000, 80000]
    timing_rows = []

    print("Worst-case timing table")
    print("n,Sequential,Binary,Two Index")

    for n in input_sizes:
        numbers = make_worst_case_list(n)

        sequential_result, sequential_time = time_algorithm(sequential_search, numbers)
        binary_result, binary_time = time_algorithm(binary_search, numbers)
        two_index_result, two_index_time = time_algorithm(two_index_search, numbers)

        print(n, sequential_time, binary_time, two_index_time, sep=",")
        timing_rows.append((n, sequential_time, binary_time, two_index_time))

        if sequential_result or binary_result or two_index_result:
            print("Error: this list was supposed to be a worst-case false list.")

    with open("project3_timing.csv", "w") as file:
        file.write("n,Sequential,Binary,Two Index\n")
        for row in timing_rows:
            file.write(
                str(row[0]) + ","
                + str(row[1]) + ","
                + str(row[2]) + ","
                + str(row[3]) + "\n"
            )

    sizes = []
    sequential_times = []
    binary_times = []
    two_index_times = []

    for row in timing_rows:
        sizes.append(row[0])
        sequential_times.append(row[1])
        binary_times.append(row[2])
        two_index_times.append(row[3])

    plt.plot(sizes, sequential_times, marker="o", label="Sequential")
    plt.plot(sizes, binary_times, marker="o", label="Binary")
    plt.plot(sizes, two_index_times, marker="o", label="Two Index")
    plt.title("Project 3 Worst-Case Timing Results")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Time (seconds, log scale)")
    plt.yscale("log")
    plt.legend()
    plt.grid(True)
    plt.savefig("project3_timing_graph.png")
    plt.close()

    plt.plot(sizes, binary_times, marker="o", label="Binary")
    plt.plot(sizes, two_index_times, marker="o", label="Two Index")
    plt.title("Project 3 Binary and Two Index Timing Results")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)
    plt.savefig("project3_timing_graph_zoom.png")
    plt.close()
