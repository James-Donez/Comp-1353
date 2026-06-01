from DoublyLinkedList import DoublyLinkedList

def dll_tester():
    # create a DoublyLinkedList
    test_list = DoublyLinkedList()
    
    #testing list creation
    assert test_list.get_size()==0,   'list should be empty to start!'
    
    #testing add_first
    test_list.add_first(1)
    assert test_list.first() == 1, 'add_first needs adjustment!'
    assert test_list.last() == 1, 'add_first needs adjustment!'
    assert test_list.get_size() == 1 ,    'add_first needs adjustment!'
    test_list.add_first(2)
    assert test_list.first() == 2, 'add_first needs adjustment!'
    assert test_list.last() == 1, 'add_first needs adjustment!'
    assert test_list.get_size() == 2, 'add_first needs adjustment!'
    
    #testing add_last
    test_list.add_last(3)
    assert test_list.first() == 2,'add_last needs adjustment!'
    assert test_list.last() == 3, 'add_last needs adjustment!'
    assert test_list.get_size() == 3, 'add_last needs adjustment!'

    #test remove_first
    assert test_list.remove_first() == 2, 'remove_first needs adjustment!'
    assert test_list.first() == 1, 'remove_first needs adjustment!'
    assert test_list.last() == 3, 'remove_first needs adjustment!'
    assert test_list.get_size() == 2, 'remove_first needs adjustment!'

    #test remove_last
    assert test_list.remove_last() == 3, 'remove_last needs adjustment!'
    assert test_list.first() == 1, 'remove_last needs adjustment!'
    assert test_list.last() == 1, 'remove_last needs adjustment!'
    assert test_list.get_size() == 1, 'remove_last needs adjustment!'

    while not test_list.is_empty():
        test_list.remove_first()

    assert test_list.get_size() == 0, 'list should be empty after removing all values'    

    for i in range(10):
        test_list.add_last(i+1)
    #test get method
    assert test_list.get(0) == 1, 'get(0) should return the element at first index'
    assert test_list.get(5) == 6, 'get(1) should return the element at index 1'
    assert test_list.get(9) == 10, 'get(9) should return the element at last index'

    print('All tests passed!')



dll_tester()