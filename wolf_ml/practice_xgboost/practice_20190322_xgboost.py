#coding=utf-8


"""
    xgboost base
"""


import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def main():
    trainx = pd.DataFrame(np.random.randn(100,5))
    trainy = pd.Series(np.random.randn(100))
    df = pd.read_csv('a.csv')
    X_train,X_test,y_train,y_test = train_test_split(trainx.values,trainy.values, test_size=0.3, random_state=1)
    data_train = xgb.DMatrix(X_train, y_train)
    data_test = xgb.DMatrix(X_test, y_test)
    params = {'max_depth': 5, 'eta': 1, 'objective': 'reg:linear'}
    max_round = 3
    watchlist = [(data_train, 'train'), (data_test, 'valid')]
    best_model = xgb.train(params, data_train, max_round, evals=watchlist)
    print("best_model ", best_model)

    
    booster = xgb.XGBRegressor(max_depth=5, n_estimators=200, learn_rate=0.01)
    booster.fit(X_train, y_train)
    test_score = booster.score(X_test, y_test)
    print("test_score ", test_score)


if __name__ == '__main__':
    main()
