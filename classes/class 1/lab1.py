from SinglyLinkedList import SinglyLinkedList
from random import randint
def main():
    # sll = SinglyLinkedList()
    # random.seed(8092024)
    # v1 = random.randint(1,1000)
    # sll.add_first(v1+10)
    # print("TEST 1")
    # print(sll.min())        # test1, sll with a single element
    # for i in range(5):
    #     sll.add_first(v1+i)
    # print("TEST 2")
    # print(sll.min())        # test2, sll where min is at the end
    # for i in range(5):
    #     sll.add_first(v1-i)
    # print("TEST 3")
    # print(sll.min())        # test3, sll where min is at the beginning
    sll2 = SinglyLinkedList()
    for i in range(20):
        sll2.add_first(randint(1,10000))
    
    sll2.rotate(5)
    print(sll2)

if __name__ == "__main__":
    main()