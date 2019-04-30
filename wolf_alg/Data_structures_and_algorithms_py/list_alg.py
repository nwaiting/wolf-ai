#coding=utf-8

import random
import time

class ATest(object):
    def __init__(self, data=None, index=0):
        self.next_ = None
        self.data_ = data
        self.index_ = index

def main():
    random.seed(time.time())
    first_obj = ATest(round(random.random(), 2), 0)
    next_obj = first_obj
    for i in range(1,10):
        tmp_obj = ATest(round(random.random(), 2), i)
        next_obj.next_ = tmp_obj
        next_obj = tmp_obj

    p_list = first_obj
    while p_list:
        print("{0} {1}".format(p_list.index_, p_list.data_))
        p_list = p_list.next_

def is_cycle(node):
    first_node = second_node = node
    while first_node and second_node and second_node.next_:
        first_node = first_node.next_
        second_node = second_node.next_.next_
        if first_node == second_node:
            return True
    return False

def find_loop_start_node(node):
    one_step_node = two_step_node = node
    while one_step_node and two_step_node and two_step_node.next_:
        one_step_node = one_step_node.next_
        two_step_node = two_step_node.next_.next_
        if one_step_node == two_step_node:
            # find has cycle
            break

    if one_step_node == None or two_step_node == None or two_step_node.next_ == None:
        return None

    first_node = node
    second_node = one_step_node
    while first_node and second_node:
        first_node = first_node.next_
        second_node = second_node.next_
        if first_node == second_node:
            return first_node

    return None

def cycle_list_generator():
    head = ATest(round(random.random(), 2))
    tmp_node = head
    for i in range(1,6):
        tmp_node.next_ = ATest(round(random.random(), 2), i)
        tmp_node = tmp_node.next_
    tmp_node.next_ = head.next_.next_.next_
    return head

def show_list(node):
    while node:
        print("{0}-{1}-{2}".format(node.index_,node.data_,node))
        node = node.next_

if __name__ == '__main__':
    #main()
    head = cycle_list_generator()
    #show_list(head)
    print(is_cycle(head))
    find_node = find_loop_start_node(head)
    print(find_node.index_)
