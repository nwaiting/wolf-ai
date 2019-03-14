#coding=utf-8

import numpy as np
from sklearn.metrics import auc
from sklearn.metrics import roc_auc_score,roc_curve


def main():
    y = np.array([0,0,1,1])
    pred = np.array([0.1, 0.4, 0.35, 0.8])
    fpr,tpr,thresholds = roc_curve(y, pred, pos_label=1)
    print(fpr,tpr,thresholds)
    print(auc(fpr, tpr))
    print(roc_auc_score(y, pred))

if __name__ == '__main__':
    main()
