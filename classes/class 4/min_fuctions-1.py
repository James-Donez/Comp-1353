import random


def min1(input_list: list[int])->int:
    min = input_list[0]
    for value in input_list:
        if min > value :
            min = value
    return min

def min2(input_list: list[int])->int:
    # performs bubble sort on the input
    n = len(input_list)
    for i in range(n):
        for j in range(1, n-i):
            if input_list[j - 1] > input_list[j]:
            # swap elements
                temp = input_list[j - 1]
                input_list[j - 1] = input_list[j]
                input_list[j] = temp
    return input_list[0]

def main():
    size = 5000
    list1 = []
    for i in range(size):
        list1.append(random.randint(0,1000))
        

if __name__ == "__main__":
    main()