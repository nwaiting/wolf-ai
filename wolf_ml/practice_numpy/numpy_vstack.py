#coding=utf-8


import numpy as np

def main():
    # 垂直叠加，即垂直合并
    a = np.array([[1,2,3]]) #shape (1,3)
    b = np.array([[4,5,6]]) #(1,3)
    print(np.vstack((a,b))) #(2,3)


    c = np.array([[1],[2],[3]]) #(3,1)
    d = np.array([[4],[5],[6]]) #(3,1)
    print(np.vstack((c,d))) #(6,1)


    # 水平叠加，即水平合并
    print(np.hstack((a,b))) #(1,6)
    print(np.hstack((c,d))) #(3,2)


if __name__ == '__main__':
    main()
