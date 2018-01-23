#!/usr/bin/env python
# coding: utf-8

"""
@file: sums_in_tree.py
@time: 2017/2/21 9:55
"""

"""
  有了第一题作为基础，这一题写起来也相当简单。只是搜索的时候呢，可以剪枝一下。这个是搜索的技巧，用多了就自然有这个习惯了！
    建树依然建立二元查找树，然后用深搜，用一个path数组把结点的值存储起来。用深搜打印路径比较方便。没有什么特殊和很难的地方。
    这里需要注意的是：这个系列中我在系列（一）中上传的pdf文件里题目4的图形没对，可能会有误导。树的形状应该是
         10
        /  \
       5   12
      / \
     4   7
    最后，依然贴代码吧！

通过建立辅助栈。先序遍历树，
1、如果节点为null，返回
2、计算栈内所有节点数值与当前节点数值的和，如果结果大于期望值，此路不通，返回；如果结果小于期望值且当前节点不为叶子，把当前节点进栈，继续遍历，否则返回；如果当前节点为叶子，且和正好是期望值，当前栈内节点和当前叶子节点组成的路径即是所求路径。
3、遍历左子树
4、遍历右子树

/////////////////////////////////////////////////////
// 输出和为sum的所有路径
void PrintPathBy(TreeNode<int>* pRoot, int sum)
{
    static std::deque<int> stack;
    static int sSum = 0;
    if(pRoot == NULL)
    {
        return;
    }
    // 如果当前节点是叶子，则是该路径的终点
    if(pRoot->pLChild == NULL && pRoot->pRChild == NULL)
    {
        if(sSum + pRoot->data == sum)
        {
            // 此为一个目标路径，打印出来，并且出栈一个节点
            for(std::deque<int>::const_iterator iter = stack.begin(); iter != stack.end(); ++iter)
            {
                printf("%d ", *iter);
            }
            printf("%d/n", pRoot->data);
            sSum -= stack.back();
            stack.pop_back();
        }
        return;
    }
    else if(sSum + pRoot->data < sum)
    {
        // 如果新节点加入，小于sum，进栈
        stack.push_back(pRoot->data);
        sSum += pRoot->data;
    }
    else
    {
        // 此路不通
        return;
    }
    // 先序遍历左子树
    PrintPathBy(pRoot->pLChild, sum);
    // 遍历右子树
    PrintPathBy(pRoot->pRChild, sum);
}
/////////////////////////////////////////////////////


/*
 * Problem_4.cpp
 * 在二元树中找出和为某一值的所有路径
 *  Created on: 2012-8-28
 *      Author: Administrator
 */
#include<stdio.h>
struct BinaryTreeNode{
    int data;
    BinaryTreeNode *pLeft,*pRight;
    BinaryTreeNode(){
        pLeft=pRight=NULL;
    }
};
#define M 100
int path[M],top=-1;
bool addNode(BinaryTreeNode **root,int value){
    if(*root!=NULL){
        if(value>(*root)->data){
            addNode(&((*root)->pRight),value);
        }else if(value<(*root)->data){
            addNode(&((*root)->pLeft),value);
        }else{
            printf("repeated node!\n");
            return false;
        }
    }else{
        BinaryTreeNode *p;
        p=new BinaryTreeNode();
        p->data=value;
        *root=p;
    }
    return true;
}
/*
 *
 * */
void search(BinaryTreeNode *cur,int sum,int &s){
    path[++top]=cur->data;
    if(cur->pLeft==NULL&&cur->pRight==NULL&&s==sum+cur->data){
        for(int i=0;i<=top;i++){
            printf("%d ",path[i]);
        }
        printf("\n");
    }
    if(sum+cur->data>=s){//剪枝
        --top;
        return;
    }
    if(cur->pLeft!=NULL)
        search(cur->pLeft,sum+cur->data,s);
    if(cur->pRight!=NULL)
        search(cur->pRight,sum+cur->data,s);
    --top;
}
int main(){
    int data[5]={10,5,12,4,7};
    BinaryTreeNode *root=NULL;
    for(int i=0;i<5;i++){
        addNode(&root,data[i]);
    }
    int a=22;
    search(root,0,a);
    return 0;
}
"""


class Stack(object):
    def __init__(self):
        self.internal_list = list()

    def push(self, obj):
        self.internal_list.append(obj)

    def front(self):
        if len(self.internal_list) > 0:
            return self.internal_list[0]

    def pop(self):
        if len(self.internal_list) > 0:
            t = self.internal_list[-1]
            self.internal_list.pop(-1)
            return t

    def pop_back(self):
        if len(self.internal_list) > 0:
            t = self.internal_list[0]
            self.internal_list.pop(0)
            return t

    def back(self):
        if len(self.internal_list) > 0:
            return self.internal_list[0]

    def size(self):
        return len(self.internal_list)

    def display(self):
        print self.internal_list


class Node(object):
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinaryTree(object):
    def __init__(self):
        self.root = None
        self.size_ = 0

    def add(self, node_value):
        if not self.root:
            self.root = Node(node_value)
            self.size_ += 1
        else:
            self.add_node(node_value, self.root)
            self.size_ += 1

    def add_node(self, value, current_node):
        if value < current_node.value:
            if current_node.left:
                self.add_node(value, current_node.left)
            else:
                current_node.left = Node(value)
        else:
            if current_node.right:
                self.add_node(value, current_node.right)
            else:
                current_node.right = Node(value)

    def display(self):
        if not self.root:
            return

        self.display_first(self.root)
        print "=============="
        self.display_mid(self.root)

    def display_first(self, current):
        if current:
            print current.value
            self.display_first(current.left)
            self.display_first(current.right)

    def display_mid(self, current):
        if current:
            self.display_first(current.left)
            print current.value
            self.display_first(current.right)

num = 0
stack = Stack()
g_list = list()


def print_path_by(root, nsum):
    if not root:
        return
    global num
    global g_list

    g_list.append(root.value)
    num += root.value

    if not root.left and not root.right:
        if num == nsum:
            print "route begin"
            print g_list
            print "route end"

    print_path_by(root.left, nsum)
    print_path_by(root.right, nsum)

    if len(g_list) > 0:
        num -= g_list[-1]
        g_list.pop(-1)


if __name__ == "__main__":
    bt = BinaryTree()
    bt.add(10)
    bt.add(5)
    bt.add(4)
    bt.add(3)
    bt.add(6)
    bt.add(11)
    bt.display()

    print "=============="
    print_path_by(bt.root, 21)






















