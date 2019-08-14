#coding=utf-8

import Queue

class Node(object):
    def __init__(self,left=None,right=None,data=None):
        self.left_ = left
        self.right_ = right
        self.data_ = data

def travel_level(root):
    if not root:
        return root
    q = Queue.Queue()
    q.put(root)
    while not q.empty():
        node = q.get()
        if node.left_:
            q.put(node.left_)
        if node.right_:
            q.put(node.right_)
        print(node.data_,)



if __name__ == '__main__':
    root = Node(Node(Node(data=20),None,50),Node(data=70),100)
    travel_level(root)
