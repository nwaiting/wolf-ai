#coding=utf-8

"""
    第一类：
        给定 nums = [2, 7, 11, 15], target = 9
        因为 nums[0] + nums[1] = 2 + 7 = 9
        所以返回 [0, 1]
"""
import time

def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i]+nums[j]==target:
                return (i,j)

def twoSum2(nums, target):
    d = {}
    for i in range(len(nums)):
        findv = target - nums[i]
        if findv in d:
            return (i,d[findv])
        else:
            d[nums[i]] = i

"""
    第二类：
        输入：(2 -> 4 -> 3) + (5 -> 6 -> 4)
        输出：7 -> 0 -> 8
        原因：342 + 465 = 807
"""

class Node(object):
    def __init__(self, data=None, next=None):
        self.data_ = data
        self.next_ = next

def addTwoNumbers(l1, l2):
    result_node = Node()
    tmp_node = result_node
    carry = 0
    while l1 or l2 or carry:
        if l1:
            carry += l1.data_
            l1 = l1.next_
        if l2:
            carry += l2.data_
            l2 = l2.next_
        node = Node(carry%10)
        carry = int(carry/10)
        node.next_ = result_node.next_
        result_node.next_ = node
    return result_node.next_

def addTwoNumbers2(l1,l2):
    res_node = Node()
    carry = 0
    p1 = res_node
    while carry or l1 or l2:
        if l1:
            carry += l1.data_
            l1 = l1.next_
        if l2:
            carry += l2.data_
            l2 = l2.next_
        node = Node(carry%10)
        carry = carry//10

        p1.next_ = node
        p1 = node
    return res_node.next_

if __name__ == '__main__':
    nums = [1,3,6,8,12,15,17,20,123,2,34,345,36,2342,3345]
    begin1 = time.time()
    print(twoSum(nums, 381))
    begin2 = time.time()
    print(twoSum2(nums, 381))
    end = time.time()
    print("first={},second={}".format(begin2-begin1, end-begin2))


    fnode = Node(4, Node(5, Node(6, Node(7))))
    snode = Node(7, Node(8, Node(9)))
    res = addTwoNumbers(fnode, snode)
    print("7654+987=",end='')
    while res:
        print(res.data_, end='')
        res=res.next_
    print()
    res2 = addTwoNumbers2(fnode,snode)
    print("456+7899=",end='')
    while res2:
        print(res2.data_, end='')
        res2=res2.next_
    print()
