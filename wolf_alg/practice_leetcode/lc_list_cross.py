#coding=utf-8

"""
    list is cross
        则先让较长的链表向后移动(len1-len2)个长度。然后开始从当前位置同时遍历两个链表，当遍历到的链表的节点相同时，则这个节点就是第一个相交的节点。
"""

class Node(object):
    def __init__(self, data=None, next=None):
        self.next_ = next
        self.data_ = data

def list_is_cross(node1, node2):
    len1 = 0
    len2 = 0
    p1 = node1
    p2 = node2
    while p1:
        len1 += 1
        p1 = p1.next_

    while p2:
        len2 += 1
        p2 = p2.next_

    if len1 > len2:
        delta = len1 - len2
        p1 = node1
        p2 = node2
    else:
        delta = len2 - len1
        p1 = node2
        p2 = node1

    while delta > 0:
        p1 = p1.next_
        delta -= 1

    while p1 != p2:
        p1 = p1.next_
        p2 = p2.next_
    return p1 != None


if __name__ == '__main__':
    main()
