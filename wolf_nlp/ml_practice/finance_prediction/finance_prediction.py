#coding=utf-8

import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

def func1():
    train_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'exam_data', 'train.csv')
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'exam_data', 'test.csv')
    pf_train = pd.read_csv(train_file)
    pf_test = pd.read_csv(test_file)
    print(pf_train.head())
    print('===============')
    print(pf_train.label.head())
    print('=================')
    print(pf_train['label'].head())
    all_train_data = pf_train.as_matrix()
    X_train = all_train_data[:, 1:-1]
    y_train = all_train_data[:, -1]

    all_test_data = pf_test.as_matrix()
    X_test = all_test_data[:, 1::]

    clf_forest = RandomForestClassifier(n_estimators=1000, max_depth=5, n_jobs=-1, random_state=int(time.time()))
    param_grid = {
        'clf__n_estimators':[500,1000,2000,3000],
        'clf__max_depth':[5,7,9,10]
        }
    piple = Pipeline([('clf', clf_forest)])
    stra_cv = StratifiedShuffleSplit(n_splits=10, test_size=0.2, train_size=None, random_state=int(time.time()))
    grid_search = GridSearchCV(piple, param_grid=param_grid, verbose=3, scoring='accuracy', cv=stra_cv).fit(X_train, y_train)
    print('best score {0} best estimator {1} best grid socre {2}'.format(grid_search.best_score_, grid_search.best_estimator_, grid_search.grid_scores_))


if __name__ == '__main__':
    func1()
