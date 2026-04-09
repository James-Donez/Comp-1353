from circularlinkedlist import CircularLinkedList, Node

def main():
    cll = CircularLinkedList()

    print(cll)   # []

    cll.add_after_cursor(6)

    print(cll)   # [6]

    cll.add_after_cursor(8)
    print(cll)   # [6 8]

    cll.add_after_cursor(10)
    print(cll)   # [6 10 8]

if __name__ == "__main__":
    main()
