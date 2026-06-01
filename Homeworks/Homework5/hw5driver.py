from ArraySet import ArraySet

with open("Homeworks/Homework5/maleNames2016.txt", "r") as file:
    malenames = ArraySet()
    for line in file:
        parts = line.split()
        malenames.add(parts[0])

with open("Homeworks/Homework5/femaleNames2016-1.txt", "r") as file:
    femalenames = ArraySet()
    for line in file:
        parts = line.split()
        femalenames.add(parts[0])

malenames.intersection(femalenames)
combined = malenames

print(f"The amount of names in both lists: {combined.get_size()}")
print(combined)
