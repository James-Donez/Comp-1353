from hash_map import HashMap

groups = HashMap()

with open("classes/class12/Dictionary.txt", "r") as file:
    for line in file:
        word = line.strip().lower()
        key = "".join(sorted(word))

        if groups.get(key) is None:
            groups.put(key, [])

        groups.get(key).append(word)

listen_key = "".join(sorted("weakliness"))
listen_anagrams = sorted(groups.get(listen_key))

print(", ".join(listen_anagrams))

largest_group = []

for anagram_list in groups.values():
    if len(anagram_list) > len(largest_group):
        largest_group = anagram_list

print("Largest number of anagrams:", len(largest_group))
print("Words:", sorted(largest_group))