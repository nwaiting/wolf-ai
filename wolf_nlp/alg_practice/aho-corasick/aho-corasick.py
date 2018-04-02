#coding=utf8
import queue

class StateNode(object):
    def __init__(self, finish=False, state=0, pattern=None, transition_table=None):
        self.finish_ = finish
        self.state_ = state
        self.pattern_ = pattern
        self.transition_table_ = transition_table if transition_table else dict()

class AC(object):
    def __init__(self):
        self.start_node = StateNode()
        self.state_count = 0
        self.correctponding_node = []
        self.fail = {}
        self.alphabet_num = 26

    def load(self, patterns):
        latest_state = 1
        for item in patterns:
            p = self.start_node
            for i in item:
                next_node = p.transition_table_.get(ord(i)-ord('a'), None)
                if not next_node:
                    next_node = StateNode()
                if next_node.state_ == 0:
                    next_node.state_ = latest_state
                    latest_state += 1
                    self.correctponding_node.append(next_node)
                p.transition_table_[ord(i) - ord('a')] = next_node
                p = next_node
            p.finish_ = True
            p.pattern_ = item

        self.state_count = latest_state
        for i in range(self.alphabet_num):
            if not self.start_node.transition_table_.get(i, None):
                self.start_node.transition_table_[i] = self.start_node

        self.dispose()

    def dispose(self):
        q = queue.Queue()
        self.fail = [StateNode() for _ in range(self.state_count)]
        for item in self.start_node.transition_table_.values():
            if item.state_ != 0:
                self.fail[item.state_] = self.start_node
                q.put(item)

        while not q.empty():
            known = q.get()
            for i in range(self.alphabet_num):
                nxt = known.transition_table_.get(i, None)
                if nxt and nxt.state_ != 0:
                    p = self.fail[known.state_]
                    while not p.transition_table_[i]:
                        p = self.fail[p.state_]
                    self.fail[nxt.state_] = p.transition_table_[i]
                    q.put(nxt)

    def match(self, s):
        res = []
        p = self.start_node
        i = 0
        while i < len(s):
            if p.transition_table_.get(ord(s[i])-ord('a'), None):
                p = p.transition_table_.get(ord(s[i])-ord('a'), None)
            else:
                p = self.fail[p.state_]
                i -= 1
            if p.finish_:
                res.append(p.pattern_)
            i += 1
        return res

if __name__ == '__main__':
    ac = AC()
    pts = []
    pts.append('hers')
    pts.append('she')
    pts.append('his')
    ac.load(pts)
    s = 'asldflsdhflkhessldhflasdhfshesdlfhsakdhishsdhflaskdhfksad'
    res = ac.match(s)
    print(res)
