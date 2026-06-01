from doublycircularlinkedlist import DoublyCircularLinkedList

import random
def homework_driver():
    random.seed(1)
    test_list = DoublyCircularLinkedList()

    for i in range(10):
        test_list.add_after_cursor(i)
    while not test_list.is_empty():
        n = random.randint(0,9)
        test_list.advance_cursor(n)
        print(test_list.delete_cursor(), end='')
    print()
homework_driver()