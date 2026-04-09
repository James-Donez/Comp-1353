from DoublyLinkedList import DoublyLinkedList

def inclass_driver():
    ddl_list = DoublyLinkedList()

    ddl_list.add_last(1)
    ddl_list.add_last(2)
    ddl_list.add_last(3)
    ddl_list.add_between(2, 3, 300)
    ddl_list.add_first(400)
    ddl_list.add_between(400, 1, 90)
    ddl_list.add_first(500)

    print(ddl_list)

    print(ddl_list.removeFirst())
    print(ddl_list.removeLast())

    print(ddl_list)