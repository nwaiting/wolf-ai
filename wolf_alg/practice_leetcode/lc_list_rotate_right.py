#coding=utf-8

"""
    向右旋转 K 个位置
"""

class Node(object):
    def __init__(self, data=None, next=None):
        self.data_ = data
        self.next_ = next

def show(head):
    while head:
        print(head.data_, end=' ')
        head = head.next_
    print()

def rotate_right_kth(head, k):
    if not head and head.next_:
        return head

    p1 = head
    p2 = head.next_
    while p2 and k > 0:
        p2 = p2.next_
        k -= 1
    if not p2:
        return head

    while p2:
        p1 = p1.next_
        if not p2.next_:
            break
        p2 = p2.next_

    tmp = p1.next_
    p1.next_ = None
    p2.next_ = head
    return tmp







if __name__ == '__main__':
    head = Node(1,Node(2, Node(3, Node(4, Node(5, Node(6, Node(7)))))))
    show(head)
    new_head = rotate_right_kth(head, 3)
    show(new_head)
