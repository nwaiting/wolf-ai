#coding=utf-8

"""
    lru:
        time O(1)
"""

class Node(object):
    def __init__(self, key=None, value=None, next=None, pre=None):
        self.key_ = key
        self.value_ = value
        self.next_ = next
        self.pre_ = pre

class LRUCache(object):
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.cap_ = capacity
        self.key_set_ = dict()
        self.head_ = Node()
        self.tail_ = Node()
        self.head_.next_ = self.tail_
        self.tail_.pre_ = self.head_
        self.tmp_node_ = None

    def remove_node(self):
        if not self.tmp_node_:
            return
        self.tmp_node_.pre_.next_ = self.tmp_node_.next_
        self.tmp_node_.next_.pre_ = self.tmp_node_.pre_

    def add_node(self):
        if self.tmp_node_:
            self.head_.next_.pre_ = self.tmp_node_
            self.tmp_node_.next_ = self.head_.next_
            self.tmp_node_.pre_ = self.head_
            self.head_.next_ = self.tmp_node_

    def show(self):
        p = self.head_.next_
        while p != self.tail_:
            print("{}-{}".format(p.key_,p.value_), end=' ')
            p = p.next_
        print()

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        key_node = None
        if key in self.key_set_:
            key_node = self.key_set_[key]
            self.tmp_node_ = key_node
        if key_node and key_node.pre_ != self.head_:
            self.remove_node()
            self.add_node()
        return key_node.value_ if key_node else None


    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        if key in self.key_set_:
            key_node = self.key_set_[key]
            key_node.value_ = value
            self.tmp_node_ = key_node
            self.remove_node()
        else:
            self.tmp_node_ = Node(key=key, value=value)
            self.key_set_[key] = self.tmp_node_
        self.add_node()
        while len(self.key_set_) > self.cap_:
            self.tmp_node_ = self.tail_.pre_
            self.remove_node()
            self.key_set_.pop(self.tmp_node_.key_)



if __name__ == '__main__':
    lru = LRUCache(5)
    lru.put(1,11)
    lru.put(2,22)
    lru.put(3,33)
    lru.put(4,44)
    lru.show()
    lru.put(5,55)
    lru.put(6,66)
    lru.show()
    print(lru.get(4))
    lru.show()
    lru.get(3)
    lru.show()
    lru.put(7,77)
    lru.show()
    print(lru.get(7))
