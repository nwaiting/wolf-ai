#coding=utf-8

class Node(object):
    def __init__(self,item=None):
        self.item_ = item
        self.contents_ = set()
        self.fre_ = -1
        self.is_root_ = False
        self.is_end_ = False
        self.childrens_ = {}
    def GetContents(self):
        return self.contents_
    def SetContents(self, contents):
        self.contents_ = contents
    def GetItem(self):
        return self.item_
    def GetFre(self):
        return self.fre_
    def SetFre(self, fre):
        self.fre_ = fre
    def IsEnd(self):
        return self.is_end_;
    def SetIsEnd(self,flag):
        self.is_end_ = flag
    def IsRoot(self):
        return is_root_
    def SetIsRoot(self,flag):
        is_root_ = flag
    def GetChildrens(self):
        return self.childrens_

class TrieTree(object):
    def __init__(self):
        self.root_ = Node("root")
        self.root_.SetIsRoot(True)
        self.root_.SetFre(0)
        self.root_.SetIsEnd(False)
    def GetRootNode(self):
        return self.root_
    def Insert(self, items, contents=None):
        node = self.root_
        for i in xrange(len(items)):
            if items[i] in node.childrens_:
                if i == len(items)-1:
                    t = node.childrens_[items[i]]
                    t.SetIsEnd(True)
                    t.SetFre(t.GetFre()+1)
                    if contents:
                        t.contents_.add(contents)
            else:
                t = Node(items[i])
                if i == len(items) - 1:
                    t.SetFre(1)
                    t.SetIsEnd(True)
                else:
                    t.SetFre(0)
                if contents:
                    t.contents_.add(contents)
                node.childrens_[items[i]] = t
            node = node.childrens_[items[i]]

    def SearchFre(self, items):
        node = self.root_
        for i in xrange(len(items)):
            if items[i] in node.childrens_:
                t = node.childrens_[items[i]]
                if i == len(items) - 1 and t.IsEnd():
                    return t.GetFre()
                node = node.childrens_[items[i]]
        return -1

    def SearchNode(self, items):
        node = self.root_
        for i in xrange(len(items)):
            if items[i] in node.childrens_:
                t = node.childrens_[items[i]]
                if i == len(items) - 1 and t.IsEnd():
                    return t
                node = node.childrens_[items[i]]
        return None

if __name__ == '__main__':
    tree = TrieTree()
    tree.Insert('tree1')
    tree.Insert('tree1')
    tree.Insert('tree2')
    tree.Insert('tree3')
    tree.Insert('tree4')
    tree.Insert('tree4')
    tree.Insert(['hang','kong','mu','jian','zhan','dou','qun','航空母舰战斗群'])
    print tree.SearchFre('tree1')
    print tree.SearchFre('tre')
    print tree.SearchFre('tree4')
    print tree.SearchFre(['hang','kong','mu','jian','zhan','dou','qun','航空母舰战斗群'])
