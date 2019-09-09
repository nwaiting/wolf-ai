#coding=utf-8


"""
    code：
        https://blog.csdn.net/liugg2016/article/details/82085799
    分析：
        https://blog.csdn.net/sinat_35261315/article/details/79205157
"""

class Node(object):
    def __init__(self, data=None, next=None):
        self.data_ = data
        self.next_ = next

def detectCycle(head):
    if not head.next_ or not head.next_.next_:
        return 0

    p1 = head.next_
    p2 = head.next_.next_
    while p2 and p2.next_ and p2.next_.next_:
        p1 = p1.next_
        p2 = p2.next_.next_
        if p1 == p2:
            return 1
    return 0

def detect_cycle(node):
    if not node:
        return False
    p1 = p2 = node
    while p2 and p2.next_:
        p1 = p1.next_
        p2 = p2.next_.next_
        if p1 == p2:
            return True
    return False

def findCycleHead(head):
    if not head:
        return None
    p1 = p2 = head
    flag = False
    while p2 and p2.next_:
        p1 = p1.next_
        p2 = p2.next_.next_
        if p1 == p2:
            flag = True
            break
    if flag:
        p3 = head
        p4 = p1
        while p3 and p4:
            if p3== p4:
                return p3
            p3 = p3.next_
            p4 = p4.next_
    return None


if __name__ == '__main__':
    node = Node(1,Node(2,Node(3,Node(4,Node(5,Node(6,Node(7)))))))
    node2 = node.next_.next_.next_
    node.next_.next_.next_.next_.next_.next_.next_ = node2
    print(detectCycle(node))
    print(findCycleHead(node).data_)
