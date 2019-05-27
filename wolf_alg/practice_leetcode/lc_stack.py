#coding=utf-8


"""
    push，pop，top 操作，并能在常数时间内检索到最小元素的栈
"""

class MinStack(object):
    def __init__(self):
        """
        initialize your data structure here.
        """
        self.values_ = []
        self.min_values_index_ = -1

    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
        if len(self.values_) <= 0:
            self.values_.append(x)
            self.min_values_index_ = 0
        else:
            if x < self.values_[self.min_values_index_]:
                self.values_.append(x)
                self.min_values_index_ = len(self.values_)-1
            else:
                self.values_.append(x)

    def pop(self):
        """
        当连续pop的时候需要找到当前最小的值
        :rtype: None
        """
        if self.min_values_index_ == len(self.values_)-1:
            self.values_.pop()
            if len(self.values_) > 0:
                key = self.values_[0]
                for i in range(len(self.values_)):
                    if self.values_[i] <= key:
                        self.min_values_index_ = i
                        key = self.values_[i]
        else:
            self.values_.pop()

    def top(self):
        """
        :rtype: int
        """
        return self.values_[-1]


    def getMin(self):
        """
        :rtype: int
        """
        if self.min_values_index_ >= 0 and self.min_values_index_ < len(self.values_):
            return self.values_[self.min_values_index_]
        return 0

if __name__ == '__main__':
    ms = MinStack()
    ms.push(20)
    ms.push(15)
    ms.push(4)
    ms.push(12)
    ms.push(11)
    ms.push(10)
    ms.push(3)
    ms.pop()
    print(ms.getMin())
    ms.pop()
    print(ms.getMin())
    ms.pop()
    print(ms.getMin())
    ms.pop()
    print(ms.getMin())
    ms.pop()
    print(ms.getMin())
    ms.pop()
    print(ms.getMin())
