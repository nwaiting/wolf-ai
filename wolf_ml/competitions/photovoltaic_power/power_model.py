#coding=utf-8

import os
import sys
from power_feature import HandlerFeatures
import pandas as pd
import numpy as np
from lightgbm.sklearn import LGBMRegressor
from xgboost.sklearn import XGBRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV

class PredictPowerByModel(object):
    def __init__(self, model_name="xgboost", is_merge=True, is_stack=False):
        self.model_name_ = model_name
        self.is_merge_ = is_merge
        self.best_model_ = None

    def get_best_model(self):
        rgr = None
        params = None
        if self.model_name_ == "xgboost":
            rgr = XGBRegressor(colsample_bytree=0.2,
                            gamma=0.0,
                            learning_rate=0.5,
                            max_depth=6,
                            min_child_weight=1.5,
                            n_estimators=2000,
                            reg_alpha=0.9,
                            reg_lambda=0.6,
                            subsample=0.2,
                            seed=42,
                            silent=1)

            #rgr = XGBRegressor(learning_rate=0.1, n_estimators=140, max_depth=6, min_child_weight=1, gamma=0, subsample=0.8,
            #                    colsample_bytree=0.8, objective="reg:squarederror", scale_pos_weight=1, seed=10)
            params = {}
        elif self.model_name_ == "lightgbm":
            rgr = LGBMRegressor( boosting_type='gbdt',
                                objective='regression',
                                n_estimators=300,
                                metric={'l2', 'l1'},
                                num_leaves=31,
                                learning_rate=0.05,
                                feature_fraction=0.9,
                                bagging_fraction=0.8,
                                bagging_freq=5,
                                verbose=0)
            params = {}
        elif self.model_name_ == "svr":
            rgr = SVR(kernel='rbf',
                        degree=3,
                        gamma='auto',
                        coef0=0.0,
                        tol=1e-3,
                        C=1.0,
                        #epsilon=0.1,
                        epsilon=1.0,
                        shrinking=True,
                        cache_size=200,
                        verbose=False,
                        max_iter=-1)
            params = {}

        X_train,X_train_tmp,y_train,y_train_tmp = None,None,None,None
        for i in range(1,5):
            file_name = "train_{0}.csv".format(i)
            X_train_tmp,y_train_tmp = HandlerFeatures(file_name).get_train_features()
            if X_train is None:
                X_train = X_train_tmp[:]
                y_train = y_train_tmp[:]
            else:
                X_train = np.append(X_train, X_train_tmp, axis=0)
                y_train = np.append(y_train, y_train_tmp, axis=0)

        grid = GridSearchCV(estimator=rgr, param_grid=params, cv=5, scoring=None, iid=False, n_jobs=-1)
        grid.fit(X_train, y_train)

        self.best_model_ = grid.best_estimator_

    def predict_data(self, result_file_name):
        predictions = []
        ids = []
        for i in range(1,5):
            file_name = "test_{0}.csv".format(i)
            X_id,X_test = HandlerFeatures(file_name).get_test_features()
            predictions += self.best_model_.predict(X_test).tolist()
            ids += X_id.astype(int).tolist()

        #pre_zip = list(zip(ids, predictions))
        #names=['id',"predicition"]
        #df_predictions = pd.DataFrame(pre_zip, columns=names)
        df_predictions = pd.DataFrame({"id":ids, "predicition":predictions})
        df_predictions.to_csv(result_file_name, index=0)



if __name__ == '__main__':
    main()
