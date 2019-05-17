#coding=utf-8

"""
    https://blog.csdn.net/huaweidong2011/article/details/82875485
    A有左右两个孩子（当然孩子可以是空），以每个孩子为起点，向下延伸，可以得到很多条单向的路径，这其中当然有一个最大路径。
        我们将以左孩子为起点的最大路径的值记为left_val，将以右孩子为起点的最大路径的值记为right_val，显然以A为最高点的最大路径只可能有以下四种情况：
        1. 若left_val < 0, 且right_val < 0, 那最大路径为A节点本身：maxPathSum(A) = A.val
        2. 若left_val > 0, 且right_val < 0, 那最大路径为A节点和以A的左孩子为起点的最大路径：maxPathSum(A) = A.val + left_val
        3. 若left_val < 0, 且right_val > 0, 那最大路径为A节点和以A的右孩子为起点的最大路径：maxPathSum(A) = A.val + right_val
        4. 若left_val > 0, 且right_val > 0, 那最大路径为A节点和以A的左、右孩子为起点的最大路径三者的联合：maxPathSum(A) = A.val + left_val + right_val
"""

class Node(object):
    def __init__(self, data=None):
        self.data_ = data
        self.left_ = None
        self.right_ = None


class Solution:
    def maxPathSum(self, root):
        self.result = root.data_
        self.helper(root)
        return self.result

    def helper(self, node):
        if not node:
            return 0
        left = self.helper(node.left_)
        right = self.helper(node.right_)
        # 返回最大的和
        self.result = max(self.result, max(left,0)+max(right,0)+node.data_)
        # 返回最大的单条路径和
        return max(node.data_, node.data_+left, node.data_+right)



if __name__ == '__main__':
    main()
