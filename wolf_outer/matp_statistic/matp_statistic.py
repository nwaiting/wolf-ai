#coding=utf-8

import os
from matp_config import config_excel_path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig

"""
    matp_statistic_20190413.zip
"""

def get_excel_files():
    all_excel_files = []
    for i in os.listdir(config_excel_path):
        full_path = os.path.join(config_excel_path, i)
        if os.path.isfile(full_path) and full_path.endswith(".xlsx"):
            all_excel_files.append(full_path)
    return all_excel_files

def full_save_fig_path(file_name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)

def statistic_excel():
    all_files = get_excel_files()
    error_main_tmp = None
    error_main = None

    errors_union = None
    errors_union_tmp = None

    for i in all_files:
        df = pd.read_excel(i)
        error_main_tmp = df["故障所属主系统"]
        errors_union_tmp = pd.concat((df["故障所属主系统"], df["故障处理方式"]), axis=1)

        if error_main is None:
            error_main = error_main_tmp
            errors_union = errors_union_tmp
        else:
            error_main = pd.concat((error_main, error_main_tmp), axis=0)
            errors_union = pd.concat((errors_union, errors_union_tmp), axis=0)

    if error_main is not None:
        error_main.value_counts().plot(kind="bar", label="各系统故障率统计图")
        plt.title("各系统故障率统计图", fontsize=20)
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        savefig(full_save_fig_path("main_errors.jpg"), format='jpg', dpi=300)
        #plt.legend(loc="upper center")
        #plt.show()

    if errors_union is not None:
        errors_union = errors_union.groupby(by=["故障所属主系统","故障处理方式"]).counts()
        #print("errors_union=",errors_union["列车号"])
        errors_union.plot(kind="hist", stacked=True)
        plt.title("运营期间系统按故障处理方式占比图", fontsize=20)
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        savefig(full_save_fig_path("errors_union.jpg"), format='jpg', dpi=300)


if __name__ == '__main__':
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    statistic_excel()
