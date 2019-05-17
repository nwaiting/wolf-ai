#coding=utf-8

"""
    print all leaves
"""

class Node(object):
    def __init__(self, data=None):
        self.data_ = data
        self.left_ =None
        self.right_ = None

root = Node(10)
def add(node, v):
    if v < node.data_:
        if not node.left_:
            node.left_ = Node(v)
        else:
            add(node.left_, v)
    else:
        if not node.right_:
            node.right_ = Node(v)
        else:
            add(node.right_, v)

def show_leaves(node):
    if not node:
        return
    if not node.left_ and not node.right_:
        print(node.data_)
        return

    show_leaves(node.left_)
    show_leaves(node.right_)


if __name__ == '__main__':
    add(root, 5)
    add(root, 8)
    add(root, 3)
    add(root, 12)
    show_leaves(root)
