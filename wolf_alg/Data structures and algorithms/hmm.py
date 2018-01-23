#coding=utf-8

import numpy as np

class HMM(object):
    def __init__(self, A, B, pi):
        self.A = A
        self.B = B
        self.pi = pi
    def _forward(self, objs):
        N = self.A.shape[0]
        T = len(objs)

        F = np.zeros((N,T))
        F[:,0] = self.pi * self.B[:,objs[0]]
        for t in xrange(1,T):
            for n in xrange(N):
                F[n,t] = np.dot(F[:,t-1], self.A[:,n]) * self.B[n, objs[t]]
        return F

    def _backward(self, objs):
        N = self.A.shape[0]
        T = len(objs)

        X = np.zeros((N,T))
        X[:,-1:] = 1
        for t in reversed(xrange(T-1)):
            for n in xrange(N):
                X[n,t] = np.sum(X[:,t+1] * self.A[n,:] * self.B[:,objs[t+1]])
        return X

    def viterbi(self, objs):
        pass

if __name__ == '__main__':
    pass
