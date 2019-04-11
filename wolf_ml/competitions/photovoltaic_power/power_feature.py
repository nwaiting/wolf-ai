#coding=utf-8

import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt

class HandlerFeatures(object):
    def __init__(self, data_file):
        self.data_file_ = data_file

    def get_data_path(self):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", self.data_file_)

    def get_train_features(self):
        columns = ['time','irradiance','wind_speed','wind_direction','temperature','pressure','humidity','solid_irradiance','power']
        df = pd.read_csv(self.get_data_path(), names=columns, header=0)
        print(df.head())
        print("=="*64)

        def split_direction(x):
            d = x["wind_direction"]
            if d < 90:
                return 1
            elif d >= 90 and d < 180:
                return 2
            elif d >= 180 and d < 270:
                return 3
            else:
                return 4
        df["w_direction"] = df.apply(split_direction, axis=1)
        dummies_direction = pd.get_dummies(df["w_direction"], prefix="w_direction")
        df = pd.concat([df, dummies_direction], axis=1)

        df_train = df.filter(regex="(^irradiance|wind_speed|w_direction_.*|temperature|pressure|humidity|power)")
        print(df_train.head())
        print("=="*64)
        data_train = df_train.values
        print("train_shape=",data_train.shape)
        return data_train[:, :-1], data_train[:, -1]


    def get_test_features(self):
        columns = ['id','time','irradiance','wind_speed','wind_direction','temperature','pressure','humidity']
        df = pd.read_csv(self.get_data_path(), names=columns, header=0)
        df_test = df.filter(regex="(id|^irradiance|wind_speed|wind_direction|temperature|pressure|humidity)")
        data_test = df_test.values
        print("test_shape=",data_test.shape)
        return data_test[:,0], data_test[:,1:]

    def parse_train_data(self):
        columns = ['time','irradiance','wind_speed','wind_direction','temperature','pressure','humidity','solid_irradiance','power']
        df = pd.read_csv(get_data_path("train_1.csv"), names=columns, header=0)
        df["wind_direction"].plot()
        plt.show()

if __name__ == '__main__':
    
    X_1,y_1 = HandlerFeatures("train_1.csv").get_train_features()
    X_2,y_2 = HandlerFeatures("train_2.csv").get_train_features()
    print(type(X_1))
    print(X_1.shape)
    print(X_2.shape)
    import numpy as np
    X_3 = np.array()
    a = np.append(X_3,X_1, axis=0)
    print(a.shape)


    #ids,fs = get_test_features("test_1.csv")
    #parse_train_data()
