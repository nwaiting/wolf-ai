#coding=utf-8

"""
    find the kth node
"""

class Node(object):
    def __init__(self, data=None, next=None):
        self.data_ = data
        self.next_ = next

def find_kth(node, k):
    p1 = node
    p2 = node
    while k > 0 and p2:
        p2 = p2.next_
        k -= 1

    if k <= 0:
        return None

    while p2:
        p1 = p1.next_
        p2 = p2.next_
    return p1



if __name__ == '__main__':
    main()
