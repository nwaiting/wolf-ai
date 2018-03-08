#!/usr/bin/env python
# coding: utf-8

"""
@file: heap_sort.py
@time: 2017/2/4 14:26
"""


class Heap():
    def __init__(self, heap=[]):
        self._heap = heap
        # 从堆的一半开始逐个节点向前调整
        # （因为完全二叉树的后一半节点都是叶子节点，不需要调整）
        for i in reversed(xrange(len(self._heap) / 2)):
            self._bubbleDown(i)

    def insert(self, data):
        """在堆中插入一个元素"""
        self._heap.append(data)
        self._bubbleUp(len(self._heap) - 1)

    def extract(self):
        """提取堆的最值"""
        # 根元素总是堆的最值
        result = self._heap[0]
        if self.size() > 1:
            # 交换根元素和最后一个元素，并删除掉最后一个元素
            self._heap[0] = self._heap.pop()
            # 交换之后可能会破坏堆的性质，需要向下调整根元素
            self._bubbleDown(0)
        return result

    def _bubbleUp(self, i):
        """对指定下标的元素向上进行调整，以维护堆的性质"""
        parent = (i - 1) / 2
        # 冒泡终止条件：到达根节点或者已满足堆的性质
        while parent >= 0:
            if self._heap[i] < self._heap[parent]:
                self._heap[i], self._heap[parent] = self._heap[parent], self._heap[i]
                i = parent
                parent = (i - 1) / 2
            else:
                break

    def _bubbleDown(self, i):
        """对指定下标的元素向下进行调整，以维护堆的性质"""
        smallest = i
        # 注意此处左右孩子的算法和教科书不太一样，因为实际数组下标是从0开始
        left, right = 2 * i + 1, 2 * i + 2
        # 找出i，left，right三个元素最小的一个
        if left < self.size() and self._heap[left] < self._heap[smallest]:
            smallest = left
        if right < self.size() and self._heap[right] < self._heap[smallest]:
            smallest = right
        if smallest != i:
            # 交换位置，并递归地继续向下冒泡调整
            self._heap[i], self._heap[smallest] = self._heap[smallest], self._heap[i]
            self._bubbleDown(smallest)

"""
先是一个无序的数组，然后从非叶子节点开始进行调整，比较他的左右孩子，如果有比较大的替换为根节点，然后再向下比较替换了后的孩子节点， 等到完成到root节点后创建完成
将顶点元素输出，一般将其和最后一个节点交换位置（注意这里堆的长度应该-1），因为别的非叶子节点仍然是满足要求的，所以只需要检查root节点是否满足要求，并进行相应的更新操作

注：1、从最后一个非叶子节点开始比较和调整

最大堆调整：将堆的末端子节点作调整，使得子节点永远小于父节点
start为当前需要调整最大堆的位置，end为调整边界
"""
def my_heap_adjust(data_list, begin, end):
    while True:
        child = begin * 2 + 1

        # 调整节点的子节点
        if child >= end:
            break

        # 取较大的子节点
        if child + 1 <= end and data_list[child] < data_list[child + 1]:
            child += 1

        # 较大的子节点成为父节点
        if data_list[begin] < data_list[child]:
            data_list[child], data_list[begin] = data_list[begin], data_list[child]
            begin = child
        else:
            break


def my_heap_sort(data_list):
    n = len(data_list)
    first = n / 2 - 1

    # 1. build max heap
    for i in xrange(first, -1, -1):
        my_heap_adjust(data_list, i, n - 1)

    # 2. sort max heap to array
    for i in xrange(n - 1, 0, -1):
        data_list[i], data_list[0] = data_list[0], data_list[i]
        my_heap_adjust(data_list, 0, i - 1)
    return data_list


if __name__ == "__main__":
    data = [8, 1, 5, 2, 400, 32, 128, 64]
    print my_heap_sort(data)
