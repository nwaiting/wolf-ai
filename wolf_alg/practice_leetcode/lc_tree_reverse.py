#coding=utf-8


"""
    reverse binary tree
"""

class Node(object):
    def __init__(self,data=None,left=None,right=None):
        self.data_ = data
        self.left_ = left
        self.right_ = right

def tree_binary(node):
    if not node:
        return node
    node.left_,node.right_ = node.right_,node.left_
    tree_binary(node.left_)
    tree_binary(node.right_)
    return node

def show(node):
    if not node:
        return
    show(node.left_)
    print(node.data_, end=' ')
    show(node.right_)


if __name__ == '__main__':
    head = Node(100,left=Node(10, left=Node(1)), right=Node(1000, right=Node(1000)))
    show(head)
    print()
    tree_binary(head)
    show(head)
    print()
