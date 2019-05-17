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


def findCycleHead(head):
    pass












if __name__ == '__main__':
    node = Node(1,Node(2,Node(3,Node(4))))
    node2 = node.next_
    node.next_.next_.next_.next_ = node2
    print(detectCycle(node))
