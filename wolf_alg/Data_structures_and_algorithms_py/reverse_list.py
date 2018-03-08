#!/usr/bin/env python
# coding: utf-8

"""
@file: reverse_list.py
@time: 2017/2/16 14:01
"""

global_value = 0


class Node:
    def __init__(self, node=None):
        global global_value
        self.value = global_value
        self.next = node
        global_value += 2


def add_list(head, node):
    last = head.next
    if not last:
        head.next = node
        return
    else:
        while last.next:
            last = last.next

        last.next = node


def print_list(head):
    first = head.next
    while first:
        print " ", first.value
        first = first.next


def reverse_list(head):
    first = None
    if head.next:
        first = head.next

    while first:
        temp = first.next
        if temp:
            if temp.next:
                first.next = temp.next
            else:
                first.next = None
                temp.next = head.next
                head.next = temp
                break
            temp.next = head.next
            head.next = temp
        else:
            break

if __name__ == "__main__":
    head = Node()
    add_list(head, Node())
    add_list(head, Node())
    add_list(head, Node())
    add_list(head, Node())
    add_list(head, Node())
    print_list(head)
    print "reverse"
    reverse_list(head)
    print_list(head)
