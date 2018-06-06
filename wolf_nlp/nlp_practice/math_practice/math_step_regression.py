#coding=utf-8

import numpy as np

class StepRegression(object):
    def __init__(self,x_arr,y_arr,epochs=0.01,numit=100):
        self.x_mat_ = np.mat(x_arr)
        self.y_mat_ = np.mat(y_arr).T
        # 分布满足0均值
        self.y_mean_ = np.mean(y_mat_, 0)
        self.epochs_ = epochs
        self.numit_ = numit

    def rss_error(self,yarr,yhatarr):
        """
            计算平方误差
        """
        return ((yarr-yhatarr)**2).sum()
    def regularize(self):
        """
            标准化矩阵
        """
        in_mat = self.x_mat_.copy()
        in_means = np.mean(in_mat, 0)
        in_var = np.var(in_mat, 0)
        in_mat = (in_mat - in_means)/in_var
        return in_mat

    def stage_wise(self):
        """
            前向逐步回归
        """
        self.y_mat_ = self.y_mat_ - self.y_mean_
        self.x_mat_ = self.regularize(self.x_mat_)
        m,n = np.shape(self.x_mat_)
        return_mat = np.zeros((self.numit_, n))
        ws = np.zeros((n,1))
        ws_test = ws.copy()
        ws_max = ws.copy()
        for i in range(self.numit_):
            print(ws.T)
            lowest_error = np.inf
            for j in range(n):
                #每个特征值的权重，尝试增加或减小一定的数值来查看平方误差
                for sign in [-1,1]:
                    ws_test = ws.copy()
                    ws_test[j] += self.epochs_ * sign
                    y_test = self.x_mat_ * ws_test
                    rss_er = self.rss_error(self.y_mat_.T, y_test.T)
                    if rss_er <= lowest_error:
                        rss_er = lowest_error
                        ws_max = ws_test
            ws = ws_max.copy()
            return_mat[i,:] = ws.T
        return return_mat

if __name__ == '__main__':
    sr = StepRegression(datamat, labelmat, epochs=0.01, numit=100)
    print(sr.stage_wise())


























#
