#coding=utf-8

import numpy as np


def func1():
    """
    np计算矩阵乘法：
        np.dot()    真正意义上的矩阵乘法，同线性代数中的乘法定义
        np.multiply()   对于元素相乘
    """
    #np.dot() 使用方法1
    # 2*3
    a = np.array([[1, 2, 3], [4, 5, 6]])
    # 3*2
    b = np.array([[1, 2], [3, 4], [5, 6]])
    # [2*3] * [3*2] = [2*2] 结果
    # [[22 28],[49 64]]
    np.dot(a,b)

    #np.dot()使用方法2
    # !!!!!!!一维矩阵!!!!!!!!!!!!!，相当于矩阵的内积
    # 1*3
    a = np.array([1, 2, 3])
    # 1*3
    b = np.array([4, 5, 6])
    # 32
    print(np.dot(a,b))

    # 3*1
    a = np.array([[1], [2], [3]])
    # 3*1
    b = np.array([[4], [5], [6]])
    # 错误 error !!!!!!!!!!!!!!
    #print(np.dot(a,b))


    #矩阵对于元素相乘
    #方法1 np.multiply()
    # 2*3
    a = np.array([[1, 2, 3], [4, 5, 6]])
    # 2*3
    b = np.array([[7,8,9],[4,7,1]])
    # 对应元素相乘 [[7,16,27],[16,35,6]]
    np.multiply(a,b)

    #方法2 矩阵直接相乘
    # 2*3
    a = np.array([[1, 2, 3], [4, 5, 6]])
    # 2*3
    b = np.array([[7,8,9],[4,7,1]])
    # 对应元素相乘 [[7,16,27],[16,35,6]]
    a*b

def func2():
    """
    填充矩阵：
        numpy.full(shape, fill_value, dtype=None, order='C')
    """
    import numpy as np
    print(np.full((3,2), 100))

def func3():
    """
    随机数：
        numpy.random.choice(a, size=None, replace=True, p=None)
        #表示从a中以概率p随机取3个，p没指定时相当于是一致的分布，replace表示抽取之后是否还放回去，False表示不放回去
        np.random.choice(a=5, size=3, replace=False, p=None)
        np.random.choice(a=5, size=3, replace=False, p=[0.2, 0.1, 0.3, 0.4, 0.0])
    """
    a = [1,2,3,4,5,6,7,8]
    print(np.random.choice(a, size=7, replace=False))

    a = 10
    print(np.random.choice(a, size=3, replace=False))

def func4():
    """
    单个元素使用矩阵数据结构传入，在tf.placeholder()中定义，在传入参数时候会使用到
    np.zeros((1,1))
    """
    a = np.zeros((1,1))
    print(a)
    a[0,0] = 100
    print(a)

if __name__ == '__main__':
    #func1()

    #func2()

    #func3()

    func4()
