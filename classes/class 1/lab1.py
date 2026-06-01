from SinglyLinkedList import SinglyLinkedList
import random



def homework_driver():
    random.seed(6)
    testing_list= SinglyLinkedList()
    for i in range(1,4):
        testing_list.add_first(i * random.randint(0,10))
        testing_list.add_last(i * random.randint(0,10))
        testing_list.add_first(i * random.randint(0,10))
        testing_list.add_last(i * random.randint(0,10))
    # print(TestingList)
    for _ in range(5):
        rand_index=random.randint(0,20)
        # print(f'rand_index is {rand_index}')
        try: testing_list.remove_at_index(rand_index)
        except IndexError as e:
            pass
            # print(e)
    print(testing_list)

#The following is the main code block:


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
    # sll2 = SinglyLinkedList()
    # for i in range(20):
    #     sll2.add_first(randint(1,10000))
    
    # print(sll2)

    # test=SinglyLinkedList()
    # print(test)
    # test.add_first(2)
    # test.add_last(3)
    # print(test)

    homework_driver()
    

if __name__ == "__main__":
    main()