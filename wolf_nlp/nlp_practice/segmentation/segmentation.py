#coding=utf-8

"""
    N-short分词是ICTCLAS分词系统和HaNLP分词库中粗分阶段使用的分词算法
        参考：http://www.cnblogs.com/zhenyulu/articles/669795.html

    N-short最短路径：
        1、计算最短路径的一批路径集合
        2、如果要计算N最短路径，比如计算2最短路径，则需要计算最短路径集合、次短路径集合2中集合路径
"""

#主路径上的每个节点对应的前驱节点
class Node(object):
    def __init__(self):
        self.pre_node_ = []
        self.current_index_ = 0

main_path = [Node() for _ in range(7)]
def init():
    #节点索引
    main_path[1].pre_node_ = [0]
    main_path[2].pre_node_ = [1]
    main_path[3].pre_node_ = [1,2]
    main_path[4].pre_node_ = [2]
    main_path[5].pre_node_ = [4]
    main_path[6].pre_node_ = [3,5]

def main():
    init()
    #用栈模拟选择所有的最短路径
    main_stack = []

    """
        第一步，从后向前依次取出PreNode队列中的当前元素压入栈中
    """
    main_stack.append(len(main_path)-1)
    if len(main_path[len(main_path)-1].pre_node_) > 0:
        tmp_obj = main_path[len(main_path)-1]
        tmp_v = tmp_obj.pre_node_[tmp_obj.current_index_]
        tmp_obj.current_index_ += 1
        main_stack.append(tmp_v)
        if len(main_path[tmp_v].pre_node_) > 0:
            tmp_obj = main_path[tmp_v]
            tmp_v = tmp_obj.pre_node_[tmp_obj.current_index_]
            tmp_obj.current_index_ += 1
            main_stack.append(tmp_v)

        if len(main_path[tmp_v].pre_node_) > 0:
            tmp_obj = main_path[tmp_v]
            tmp_v = tmp_obj.pre_node_[tmp_obj.current_index_]
            tmp_obj.current_index_ += 1
            main_stack.append(tmp_v)

        if len(main_path[tmp_v].pre_node_) > 0:
            tmp_obj = main_path[tmp_v]
            tmp_v = tmp_obj.pre_node_[tmp_obj.current_index_]
            tmp_obj.current_index_ += 1
            main_stack.append(tmp_v)
    print('first path ', main_stack[::-1])

    """
        第二步，将栈中元素依次弹出，弹出一个改变压栈时，PreNode的当前指针
        弹出一个栈中元素，检测PreNode中指针是否可以后移，如果可以后移则向前查找路径
    """
    while len(main_stack) > 0:
        tmp_v = main_stack.pop()
        #print('first ', tmp_v)
        const_tmp_v = tmp_v
        if main_path[tmp_v].current_index_ >= len(main_path[tmp_v].pre_node_):
            continue

        #print('do ', tmp_v)
        main_stack.append(tmp_v)
        tmp_obj = main_path[tmp_v]
        tmp_v = tmp_obj.pre_node_[tmp_obj.current_index_]
        main_stack.append(tmp_v)
        while tmp_v > 0:
            tmp_obj = main_path[tmp_v]
            tmp_v = tmp_obj.pre_node_[tmp_obj.current_index_-1]
            main_stack.append(tmp_v)
            #print('second ', tmp_v)
        main_path[const_tmp_v].current_index_ += 1

        print('path ', main_stack)


if __name__ == '__main__':
    main()
