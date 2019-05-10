#coding=utf-8

"""
    树的层次遍历：
        如需要按照层次输出一棵树的所有节点的组合（LeetCode 107）
        如求一棵树的最左节点（LeetCode 513）

    二叉树相关算法：
        https://segmentfault.com/a/1190000018265301?utm_source=tag-newest
"""

from queue import Queue, LifoQueue

class Node(object):
    def __init__(self, data=None):
        self.left_ = None
        self.right_ = None
        self.data_ = data


root = Node(8)
# build binary tree
def add(data):
    node = Node(data=data)
    qu = Queue()
    qu.put(root)
    while True:
        tmp_node = qu.get()
        if not tmp_node.left_:
            tmp_node.left_ = node
            return
        elif not tmp_node.right_:
            tmp_node.right_ = node
            return
        else:
            qu.put(tmp_node.left_)
            qu.put(tmp_node.right_)

# build binary search tree
def addBST(node, data):
    if data < node.data_:
        if node.left_:
            addBST(node.left_, data)
        else:
            node.left_ = Node(data=data)
    else:
        if node.right_:
            addBST(node.right_, data)
        else:
            node.right_ = Node(data)

# lookup BST
def lookupBST(node, data):
    if not node:
        return None
    elif node.data_ == data:
        return node
    elif data < node.data_:
        return lookupBST(node.left_, data)
    else:
        return lookupBST(node.right_, data)

######################### pre order
def preoder(root):
    if not isinstance(root, Node):
        return []
    preorder_res = []
    if root:
        preorder_res.append(root.data_)
        preorder_res += preoder(root.left_)
        preorder_res += preoder(root.right_)
    return preorder_res

def pre_list(node):
    res = []
    if not node:
        return []
    print("pre list=", node.data_)
    res.append(node.data_)
    res += pre_list(node.left_)
    res += pre_list(node.right_)
    return res

def pre_order_not_recursion(root):
    if not isinstance(root, Node):
        return None

    stack = [root]
    result = []
    while stack:
        node = stack.pop(-1)
        if node:
            result.append(node.data_)
            stack.append(node.right_)
            stack.append(node.left_)
    return result

def pre_list_not_recursion(node):
    qu = LifoQueue()
    qu.put(node)
    res = []
    while qu.qsize() > 0:
        tmp_node = qu.get()
        res.append(tmp_node.data_)
        if tmp_node.right_:
            qu.put(tmp_node.right_)
        if tmp_node.left_:
            qu.put(tmp_node.left_)
    return res


######################### pre order

######################### mid order
def mid_list(node):
    if not node:
        return []
    res = []
    res += mid_list(node.left_)
    res.append(node.data_)
    res += mid_list(node.right_)
    return res


def mid_list_not_recursion(node):
    qu = LifoQueue()
    qu.put(node.right_)
    qu.put(node)
    qu.put(node.left_)
    while qu.qsize() > 0:
        


def middle_order_bot_recursion(root):
    if not isinstance(root, Node):
        return []

    result = []
    stack = [root.right_, root.data_, root.left_]
    while stack:
        temp = stack.pop(-1)
        if temp:
            if isinstance(temp, Node):
                stack.append(temp.right_)
                stack.append(temp.data_)
                stack.append(temp.left_)
            else:
                result.append(temp)
    return result


######################### mid order

######################### last order
def last_list(node):
    if not node:
        return
    last_list(node.left_)
    last_list(node.right_)
    print("last list=", node.data_)


def last_list_not_recursion(node):
    pass


######################### last order

def list_tree_level(node):
    qu = Queue()
    qu.put(node)
    length = qu.qsize()
    while qu.qsize() > 0:
        length = qu.qsize()
        while length > 0:
            node = qu.get()
            print(node.data_)
            if node.left_:
                qu.put(node.left_)
            if node.right_:
                qu.put(node.right_)
            length -= 1
        print("====")

def list_tree_level2(node):
    qu = Queue()
    qu.put(node)
    while qu.qsize() > 0:
        qu.put("$")
        while True:
            tmp_node = qu.get()
            if tmp_node == "$":
                print("=======")
                break
            print(tmp_node.data_)
            if tmp_node.left_:
                qu.put(tmp_node.left_)
            if tmp_node.right_:
                qu.put(tmp_node.right_)


if __name__ == '__main__':
    add(10)
    add(3)
    add(5)
    add(15)
    add(12)
    pre_list(root)
    print("=="*64)

    root = Node(8)
    addBST(root, 10)
    addBST(root, 3)
    addBST(root, 5)
    addBST(root, 15)
    addBST(root, 12)
    res = pre_list(root)
    res2 = pre_order_not_recursion(root)
    res3 = pre_list_not_recursion(root)
    print("res=",res)
    print("res2=",res2)
    print("res3=",res3)
    print("=="*64)
    res = preoder(root)
    print("=="*64)
    print(res)
    print("=="*64)
    res = mid_list(root)
    res2 = middle_order_bot_recursion(root)
    print("mid res=",res)
    print("mid res2=",res2)
    print("=="*64)
    last_list(root)
    find_node = lookupBST(root, 15)
    print("find_node=",find_node)
    print("find_node=",find_node.data_)
    #list_tree_level(root)
    #list_tree_level2(root)
