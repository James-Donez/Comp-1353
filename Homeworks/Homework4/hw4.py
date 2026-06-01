from arraylist import ArrayList


array_list = ArrayList()

for number in range(1, 101):
    array_list.append(number)

total = 0
for number in array_list:
    total += number

expected_total = 100 * 101 // 2

print("ArrayList:", array_list)
print("Total:", total)
print("Expected total:", expected_total)
print("Correct:", total == expected_total)
