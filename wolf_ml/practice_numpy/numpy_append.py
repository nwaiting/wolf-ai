#coding=utf-8

"""
    numpy的append将array进行追加，追加的时候数据进行深拷贝进去
"""



import numpy as np


def main():
    X_train,X_train_tmp,y_train,y_train_tmp = None,None,None,None
    for i in range(3):
        X_train_tmp,y_train_tmp = np.random.rand(2,5),np.random.rand(2,5)
        print(X_train_tmp)
        print("=="*64)
        if X_train is None:
            X_train = X_train_tmp[:]
            y_train = y_train_tmp[:]
        else:
            X_train = np.append(X_train, X_train_tmp, axis=0)
            y_train = np.append(y_train, y_train_tmp, axis=0)
    print(X_train)







if __name__ == '__main__':
    main()
