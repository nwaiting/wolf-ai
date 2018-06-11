#coding=utf-8

import numpy as np

#多元正太分布
np.random.multivariate_normal()
#狄利克雷分布
np.random.dirichlet()
#伽马分布
np.random.gamma()
#logistic分布
np.random.logistic()

#从x中根据概率p，抽取出一个y大小的矩阵 
np.random.choice(x, y, p=None)

if __name__ == '__main__':
    main()
