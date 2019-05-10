#coding=utf-8

from copy import copy

"""
    https://blog.csdn.net/u011452172/article/details/78127836
"""

class Node(object):
    def __init__(self, data=None):
        self.next_ = None
        self.data_ = data

head = Node(888)

# func1，time O(n) space O(n)
# 数组的索引逆序进行反转
def list_reverse1(head):
    res = []
    tmp_node = head
    while tmp_node:
        res.append(tmp_node)
        tmp_node = tmp_node.next_

    print("reverse1 ",end=' ')
    for i in res[::-1]:
        print(i.data_, end=' ')
    print('')

# func2 time O(n) space O(1)
# 逐个链接点进行反转
def list_reverse2(node):
    new_head = copy(node)
    new_head.next_ = None
    while node.next_:
        tmp_head = new_head
        new_head = copy(node.next_)
        new_head.next_ = tmp_head
        node = node.next_

    print("reverse2 ", end=' ')
    while new_head:
        print(new_head.data_, end=' ')
        new_head = new_head.next_
    print('')


def list_reverse22(node):
    #先将原链表的第一个节点变成了新链表的最后一个节点，同时将原链表的第二个节点保存在cur中
    pre = node
    cur = node.next_
    pre.next_ = None
    #从原链表的第二个节点开始遍历到最后一个节点，将所有节点翻转一遍
    while cur:
        tmp = cur.next_
        cur.next_ = pre
        pre = cur
        cur = tmp
    return pre

"""
    !!!
"""
def list_reverse2222(node):
    if not node or not node.next_:
        return node
    p1 = node
    p2 = node.next_
    while p2:
        tmp = p2.next_
        p2.next_ = p1
        p1 = p2
        p2 = tmp
    node.next_ = None
    return p1

def list_reverse222(node):
    cur = node
    tmp = None
    new_head = None
    while cur:
        tmp = cur.next_
        cur.next_ = new_head
        new_head = cur
        cur = tmp
    print('reverse222 ', end=' ')
    while new_head:
        print(new_head.data_, end=' ')
        new_head = new_head.next_
    print('')

# func3 time O(n) space O(1)
# 第2个节点到第N个节点，依次逐节点插入到第1个节点(head节点)之后，最后将第一个节点挪到新表的表尾
def list_reverse3(node):
    current_node = node.next_
    while current_node:
        tmp_node = copy(current_node)
        tmp_node.next_ = node.next_
        node.next_ = tmp_node
        if current_node.next_:
            current_node = current_node.next_
        else:
            break
    new_head = copy(node.next_)
    current_node.next_ = node
    node.next_ = None
    print("reverse3 ", end='')
    while new_head:
        print(new_head.data_, end=' ')
        new_head = new_head.next_
    print('')

def add(node, data):
    if not node.next_:
        node.next_ = Node(data=data)
        return node.next_

def show(node):
    print("show ", end=' ')
    while node:
        print(node.data_, end=' ')
        node = node.next_
    print('')

if __name__ == '__main__':
    node = add(head, 8)
    node = add(node, 5)
    node = add(node, 7)
    node = add(node, 3)
    node = add(node, 10)
    node = add(node, 15)

    #show(head)
    #list_reverse1(copy(head))

    #show(head)
    #list_reverse2(copy(head))

    show(head)
    res = list_reverse22(copy(head))

    #show(head)
    #res = list_reverse2222(copy(head))

    while res:
        print(res.data_, end=' ')
        res = res.next_
    print('')

    #show(head)
    #list_reverse222(copy(head))

    #show(head)
    #list_reverse3(head)
