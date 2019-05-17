#coding=utf-8

"""
    binary tree and BST ancestor
    https://blog.csdn.net/u012292754/article/details/87474802
"""

class Node(object):
    def __init__(self, data=None):
        self.left_ = None
        self.right_ = None
        self.data_ = data

"""
    binary search tree
"""
def lowestCommonAncestor_searchTree(root, node1, node2):
    root_data = root.data_
    node1_data = node1.data_
    node2_data = node2.data_
    if node1_data > root_data and node2_data > root_data:
        return lowestCommonAncestor_searchTree(root.right_, node1, node2)
    elif node1_data < root_data and node2_data < root_data:
        return lowestCommonAncestor_searchTree(root.left_, node1, node2)
    else:
        return root

"""
    binary tree
"""
def lowestCommonAncestor_binaryTree(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowestCommonAncestor_binaryTree(root.left_, p, q)
    right = lowestCommonAncestor_binaryTree(root.right_, p, q)
    if left and right:
        return root
    return left ? left:right


if __name__ == '__main__':
    main()
