from arraylist import ArrayList
import time
import matplotlib.pyplot as plt


class ArrayListArithmetic(ArrayList):
    def expand_array(self):
        new_capacity = self.capacity + 1000
        new_array = [None] * new_capacity
        for i in range(self.size):
            new_array[i] = self.array[i]
        self.capacity = new_capacity
        self.array = new_array


def time_append(list_class, n):
    start = time.perf_counter()
    arr_list = list_class()
    for i in range(n):
        arr_list.append(i)
    stop = time.perf_counter()
    return stop - start


num_trial = (25000, 50000, 100000, 200000)
labels = {
    25000: "25k",
    50000: "50k",
    100000: "100k",
    200000: "200k",
}

geometric_times = []
arithmetic_times = []

print("n\tTime for Geometric Expansion\tTime for Arithmetic Expansion")
for n in num_trial:
    geometric_time = time_append(ArrayList, n)
    arithmetic_time = time_append(ArrayListArithmetic, n)

    geometric_times.append(geometric_time)
    arithmetic_times.append(arithmetic_time)

    print(f"{labels[n]}\t{geometric_time:.6f}\t\t\t{arithmetic_time:.6f}")


plt.plot(num_trial, geometric_times, marker='o', label='Geometric Expansion')
plt.plot(num_trial, arithmetic_times, marker='o', label='Arithmetic Expansion')
plt.xlabel('Number of items (n)')
plt.ylabel('Elapsed time (seconds)')
plt.title('Geometric vs Arithmetic Array Expansion')
plt.grid(True)
plt.legend()
plt.show()
