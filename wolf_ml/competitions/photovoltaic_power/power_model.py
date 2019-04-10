#coding=utf-8

import os
import sys
from power_feature import get_train_feafures, get_test_feature
import pandas as pd
from lightgbm.sklearn import LGBMRegressor
from xgboost.sklearn import XGBRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV


def get_best_model(model_name):
    rgr = None
    params = None
    if model_name == "xgboost":
        rgr = XGBRegressor(learning_rate=0.1, n_estimators=140, max_depth=6, min_child_weight=1, gamma=0, subsample=0.8,
                            colsample_bytree=0.8, objective="reg:squarederror", scale_pos_weight=1, seed=10)
        params = {"max_depth":list(range(3,8,1)), "min_child_weight":list(range(1,6,2))}
    elif model_name == "lightgbm":
        rgr = LGBMRegressor()
        params = {}
    elif model_name == "SVR":
        rgr = SVR()
        params = {}

    for i in range(1,5):
        file_name = "train_{0}.csv".format(i)
        X_train,y_train = get_train_feafures(file_name)
        grid = GridSearchCV(estimator=rgr, param_grid=params, cv=10, scoring=None, iid=False, n_jobs=-1)
        grid.fit(X_train, y_train)

    return grid.best_estimator_

def get_model(model_name):
    rgr = get_best_model(model_name)


def predict_data(rgr, result_file_name):
    predictions = []
    ids = []
    for i in range(1, 5):
        file_name = "test_{0}.csv".format(i)
        X_id,X_test = get_test_feature(file_name)
        predictions += model.predict(X_test)
        ids += X_id

    pre_zip = list(zip(ids, predictions))
    names=['id',"predicition"]
    df_predictions = pd.DataFrame(pre_zip, columns=names)
    df_predictions.to_csv(result_file_name)



if __name__ == '__main__':
    main()
