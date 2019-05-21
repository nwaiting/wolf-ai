#coding=utf-8


"""
    find mid node
"""


class Node(object):
    def __init__(self,data=None,next=None):
        self.data_ = data
        self.next_ = next

def find_mid(head):
    if not head:
        return None
    p1 = head.next_
    p2 = head.next_.next_
    while p2:
        p1 = p1.next_
        p2 = p2.next_.next_
    return p1





if __name__ == '__main__':
    main()
