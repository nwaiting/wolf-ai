#coding=utf8

"""
线段树：
    概述：从一个实例引入，如何求在A[1]...A[10000]中，求A[L...R]和最高效
    方法一：对A[L...R]中数据逐个相加，计算R-L+1次
    方法二：前缀和，
            令S[0]=A[0],S[k]=A[1...k]，则A[L...R]=S[R]-S[L]
            缺点：当修改其中某一个值，如果A[L]+=c,则A[L...R]全部需要更新
    方法三：线段树
            对于任意区间[L,R],线段树在上述子区间选择约2*log(R-L+1)个拼成区间[L,R]
            如果A[L]+=c，线段树子区间中，约有log(10000)个包含了L，所以需要修改log(10000)个

"""

class LineTree(object):
    def __init__(self, n=None):
        self._A = [0] * n if n else 1024
        l = len(self._A)
        self._SumA = [0] * (l<<2)
        print('a len {0} suma len {1}'.format(len(self._A), len(self._SumA)))

    def build(self,l,r,rt):
        """
        建立线段树，将self._A中的数值累加到self._SumA
        @ [l,r]表示当前区间
        @rt 表示当前节点实际存储的位置
        """
        if l >= r:
            self._SumA[rt] = self._A[l]
            return
        m = (r-l)>>1
        self.build(l,l+m,rt<<1)
        self.build(l+m+1,r,rt<<1|1)
        self.pushup(rt)

    def update(self,L,C,l,r,rt):
        """
        @[l,r]节点区间
        @rt节点存储位置
        @C更新的值
        """
        if l >= r:
            self._A[rt] += C
        m = (r-l)>>1
        #更新只更新其中某一边的值，更新左边或者右边
        if rt <= l+m:
            self.update(L,C,l,l+m,rt<<1)
        else:
            self.update(L,C,l+m+1,r,rt<<1|1)
        self.pushup(rt)

    def query(self,L,R,l,r,rt):
        """
        @[L,R]操作区间 求和区间
        @[l,r]当前区间
        @rt当前节点编号
        """
        if l >= L or r <= R:
            return self._SumA[rt]
        m = (r-l)>>1
        sum_value = 0
        if L <= l + m:
            sum_value += self.query(L,R,l,l+m,rt<<1)
        if R >= l+m+1:
            sum_value += self.query(L,R,l+m+1,r,rt<<1|1)
        return sum_value

    def pushup(self, rt):
        """
        更新节点信息，比如求和
        rt 当前节点存储位置
        """
        self._SumA[rt] = self._SumA[rt<<1] + self._SumA(rt<<1|1)

if __name__ == "__main__":
    ltree = LineTree(4)
