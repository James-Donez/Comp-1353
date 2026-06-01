from hash_set import HashSet


def table_values(hash_set):
    values = []

    for bucket in hash_set.the_table:
        for value in bucket:
            values.append(value)

    return values


def assert_values(hash_set, expected):
    actual = set(table_values(hash_set))
    assert actual == expected, f"expected values {expected}, got {actual}"


def make_set(values):
    hash_set = HashSet()

    for value in values:
        hash_set.add(value)

    return hash_set


def test_init():
    hash_set = HashSet()

    assert len(hash_set.the_table) == 16, "new table should have 16 buckets"
    assert hash_set.size == 0, "new set should start empty"


def test_init_table():
    hash_set = make_set([1, 2, 3])
    hash_set._init_table(8)

    assert len(hash_set.the_table) == 8, "table should use the new capacity"
    assert hash_set.size == 0, "initializing a table should reset the size"
    assert_values(hash_set, set())


def test_hash_and_compress():
    hash_set = HashSet()
    index = hash_set._hash_and_compress(42)

    assert 0 <= index < len(hash_set.the_table), "hash index should be a table index"


def test_expand_table():
    hash_set = make_set([1, 2, 3])
    old_capacity = len(hash_set.the_table)

    hash_set._expand_table()

    assert len(hash_set.the_table) == old_capacity * 2, "expand should double capacity"
    assert_values(hash_set, {1, 2, 3})


def test_get_size():
    hash_set = make_set([4, 5, 6])

    assert hash_set.get_size() == 3, "get_size should return the number of values"


def test_add():
    hash_set = HashSet()

    hash_set.add(10)
    hash_set.add(20)
    hash_set.add(10)

    assert_values(hash_set, {10, 20})
    assert hash_set.size == 2, "adding a duplicate should not change size"


def test_discard():
    hash_set = make_set([10, 20])

    hash_set.discard(10)
    hash_set.discard(99)

    assert_values(hash_set, {20})
    assert hash_set.size == 1, "discard should only lower size when a value is removed"


def test_contains():
    hash_set = make_set([10, 20])

    assert hash_set.contains(10) is True, "contains should find stored values"
    assert hash_set.contains(99) is False, "contains should reject missing values"


def test_union():
    left = make_set([1, 2])
    right = make_set([2, 3])

    left.union(right)

    assert_values(left, {1, 2, 3})


def test_intersection():
    left = make_set([1, 2, 3])
    right = make_set([2, 3, 4])

    left.intersection(right)

    assert_values(left, {2, 3})


def test_difference():
    left = make_set([1, 2, 3])
    right = make_set([2, 4])

    left.difference(right)

    assert_values(left, {1, 3})


def test_iter():
    hash_set = make_set([1, 2, 3])

    assert set(iter(hash_set)) == {1, 2, 3}, "__iter__ should yield every value"


def test_str():
    hash_set = make_set([1, 2, 3])
    result = str(hash_set)

    assert result.startswith("{") and result.endswith("}"), "string should look like a set"
    assert "1" in result and "2" in result and "3" in result


def run_test(method_name, test):
    try:
        test()
        print(f"PASS {method_name}")
        return True
    except AssertionError as error:
        print(f"FAIL {method_name}: {error}")
    except Exception as error:
        print(f"FAIL {method_name}: {type(error).__name__}: {error}")

    return False


def main():
    tests = [
        ("__init__", test_init),
        ("_init_table", test_init_table),
        ("_hash_and_compress", test_hash_and_compress),
        ("_expand_table", test_expand_table),
        ("get_size", test_get_size),
        ("add", test_add),
        ("discard", test_discard),
        ("contains", test_contains),
        ("union", test_union),
        ("intersection", test_intersection),
        ("difference", test_difference),
        ("__iter__", test_iter),
        ("__str__", test_str),
    ]

    passed = 0

    for method_name, test in tests:
        if run_test(method_name, test):
            passed += 1

    percent_complete = passed / len(tests) * 100

    print()
    print(f"HashSet tests passed: {passed}/{len(tests)}")
    print(f"HashSet completion by tester: {percent_complete:.1f}%")


if __name__ == "__main__":
    main()
