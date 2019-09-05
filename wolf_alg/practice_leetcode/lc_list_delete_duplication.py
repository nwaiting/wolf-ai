#coding=utf-8

"""
    sort list delete dumplication
"""

class Node(object):
    def __init__(self, data=None, next=None):
        self.next_ = next
        self.data_ = data

def show(node):
    while node:
        print(node.data_,)
        node = node.next_
    print()

def delete_dumplication(head):
    if not head and not head.next_:
        return head
    p1 = head
    p2 = head.next_
    while p2:
        while p2 and p1.data_ == p2.data_:
            p2 = p2.next_
        p1.next_ = p2
        p1 = p2
        if not p2:
            break
        p2 = p2.next_
    return head



if __name__ == '__main__':
    head = Node(1, Node(1, Node(3, Node(8, Node(8, Node(11, Node(11)))))))
    show(head)
    delete_dumplication(head)
    show(head)
