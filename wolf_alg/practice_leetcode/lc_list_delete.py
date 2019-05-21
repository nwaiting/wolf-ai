#coding=utf-8


"""
    delete node O(1)
    param:
        head
        node
"""

class Node(object):
    def __init__(self, data=None,next=None):
        self.next_ = next
        self.data_ = data

def delete_node(head, node):
    if not node:
        return
    next_node = node.next_
    node.data_ = next_node.data_
    node.next_ = next_node.next_
    del next_node

def delete_node(node):
    node.next_.pre_ = node.pre_
    node.pre_.next_ = node.next_
    del node

if __name__ == '__main__':
    main()
