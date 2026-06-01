from hash_map import HashMap

def main():
    map = HashMap()
    with open("classes/class11/baby_names2016.txt", "r") as a_file:
        for line in a_file:
            data = line.strip().split(" ")
            if map.get(data[0]) is None:
                map.put(data[0], data[1])
            else:
                map.put(data[0], data[1] + map.get(data[0]))

    map.output_table_info()


if __name__ == "__main__":
    main()