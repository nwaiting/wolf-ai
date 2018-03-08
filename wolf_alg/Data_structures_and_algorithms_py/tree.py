#!/usr/bin/env python
# coding: utf-8

"""
@file: tree.py
@time: 2017/1/18 16:56
"""


class Node(object):
    def __init__(self, data=None):
        self.left = None
        self.right = None
        self.data = data

root = Node()


def list_pre(node):
    if node:
        print node.data
        list_pre(node.left)
        list_pre(node.right)


def list_middle(node):
    if node:
        list_middle(node.left)
        print node.data
        list_middle(node.right)


def list_last(node):
    if node:
        list_last(node.left)
        list_last(node.right)
        print node.data


def add(root=None, data=None):
    if not root.data:
        root = Node(data)
    elif data < root.data:
        add(root.left, data)
    else:
        add(root.right, data)

if __name__ == "__main__":
    add(root, 10)
    add(root, 5)
    add(root, 4)
    add(root, 7)
    add(root, 12)

    list_pre(root)
