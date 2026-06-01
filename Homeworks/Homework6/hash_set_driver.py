from hash_set import HashSet

with open("Homeworks/Homework5/maleNames2016.txt", "r") as file:
    male_names = HashSet()
    for line in file:
        parts = line.split()
        male_names.add(parts[0])

with open("Homeworks/Homework5/femaleNames2016-1.txt", "r") as file:
    female_names = HashSet()
    for line in file:
        parts = line.split()
        female_names.add(parts[0])

male_names.intersection(female_names)

print(male_names.size)

print(male_names)

