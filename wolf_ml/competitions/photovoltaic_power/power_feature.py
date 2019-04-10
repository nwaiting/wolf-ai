#coding=utf-8

import os
import pandas as pd

def get_data_path(data_file):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", data_file)

def get_train_feafures(data_file):
    columns = ['time','irradiance','wind_speed','wind_direction','temperature','pressure','humidity','solid_irradiance','power']
    df = pd.read_csv(get_data_path(data_file), names=columns, header=0)
    df_train = df.filter(regex="(^irradiance|wind_speed|wind_direction|temperature|pressure|humidity|power)")
    data_train = df_train.as_matrix()
    return data_train[:, :-1], data_train[:, -1]


def get_test_feature(data_file):
    columns = ['id','time','irradiance','wind_speed','wind_direction','temperature','pressure','humidity']
    df = pd.read_csv(get_data_path(data_file), names=columns, header=0)
    df_test = df.filter(regex="(id|irradiance|wind_speed|wind_direction|temperature|pressure|humidity)")
    data_test = df_test.as_matrix()
    return data_test[:,0], data_test[:,1:]


if __name__ == '__main__':
    import os
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    train_file = os.path.join(data_path, "train_1.csv")
    get_train_feafures(train_file)
