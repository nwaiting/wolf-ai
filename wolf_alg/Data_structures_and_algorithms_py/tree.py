#!/usr/bin/env python
# coding: utf-8

"""
    @file: tree.py
    @time: 2017/1/18 16:56
"""

"""
    树的遍历有很多实际应用，如找到匹配的字符串、文本分词和文件路径等
    树的遍历两个基本方法：
        深度优先遍历
            前序遍历
            中序遍历
            后序遍历
        广度优先遍历
            层次遍历

    二叉树相关算法：
        https://segmentfault.com/a/1190000018265301?utm_source=tag-newest
"""

class Node(object):
    def __init__(self, data=None):
        self.left_ = None
        self.right = None
        self.data = data

root = Node()


def list_pre(node):
    if node:
        print node.data
        list_pre(node.left_)
        list_pre(node.right)


def list_middle(node):
    if node:
        list_middle(node.left_)
        print node.data
        list_middle(node.right)


def list_last(node):
    if node:
        list_last(node.left_)
        list_last(node.right)
        print node.data


def add(root=None, data=None):
    if not root.data:
        root = Node(data)
    elif data < root.data:
        add(root.left_, data)
    else:
        add(root.right, data)

"""
    BST(binary search tree)
    (is order?)
"""
def isBST(root):
    tree_list = inOrder(root)
    for i in range(len(tree_list)-1):
        if tree_list[i] > tree_list[i+1]:
            return False
    return True

def inOrder(node):
    order_list = []
    if not node:
        return
    inOrder(node.left_)
    order_list.append(node.data)
    inOrder(node.right_)
    return order_list

if __name__ == "__main__":
    add(root, 10)
    add(root, 5)
    add(root, 4)
    add(root, 7)
    add(root, 12)

    list_pre(root)
