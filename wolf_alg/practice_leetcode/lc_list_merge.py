#coding=utf-8


class Node(object):
    def __init__(self,data=None,next=None):
        self.data_=data
        self.next_=next

def show(l):
    while l:
        print(l.data_,end=' ')
        l = l.next_
    print('')

def merge_list(l1,l2):
    if not l1:
        return l2
    if not l2:
        return l1
    p1 = l1
    p2 = l2
    head = None
    head_next = None
    if l1.data_<l2.data_:
        head = p1
        p1 = p1.next_
    else:
        head = p2
        p2 = p2.next_
    head_next = head
    while p1 and p2:
        if p1.data_<p2.data_:
            head_next.next_ = p1
            head_next = head_next.next_
            p1 = p1.next_
        else:
            head_next.next_ = p2
            head_next = head_next.next_
            p2 = p2.next_
    if p1:
        head_next.next_ = p1
    if p2:
        head_next.next_ = p2
    return head

def merge_list2(l1,l2):
    if not l1:
        return l2
    if not l2:
        return l1
    head = Node()
    p1 = head
    while l1 and l2:
        if l1.data_ < l2.data_:
            p1.next_ = l1
            l1 = l1.next_
        else:
            p1.next_ = l2
            l2 = l2.next_
        p1 = p1.next_
    if l1:
        p1.next_ = l1
    if l2:
        p1.next_ = l2
    return head.next_



if __name__=="__main__":
    ll1 = Node(1,Node(3,Node(5,Node(7))))
    ll2 = Node(2,Node(4,Node(6,Node(8,Node(10)))))
    res = merge_list2(ll1,ll2)
    show(res)
