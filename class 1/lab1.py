from SinglyLinkedList import SinglyLinkedList
import random

def main():
    sll = SinglyLinkedList()
    random.seed(8092024)
    v1 = random.randint(1,1000)
    sll.add_first(v1+10)
    print(sll.min())        # test1, sll with a single element
    for i in range(5):
        sll.add_first(v1+i)
    print(sll.min())        # test2, sll where min is at the end
    for i in range(5):
        sll.add_first(v1-i)
    print(sll.min())        # test3, sll where min is at the beginning
    sll2 = SinglyLinkedList()
    for i in range(100):
        sll2.add_first(random.randint(1,10000))
    print(sll2.min())       # test4, sll where min is at a random location
    
if __name__ == "__main__":
    main()