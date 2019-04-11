#coding=utf-8

import os
from matp_config import config_excel_path
import pandas as pd
import matplotlib.pyplot as plt


def get_excel_files():
    all_excel_files = []
    for i in os.listdir(config_excel_path):
        full_path = os.path.join(config_excel_path, i)
        if os.path.isfile(full_path) and full_path.endswith(".xlsx"):
            all_excel_files.append(full_path)
    return all_excel_files

def statistic_excel():
    all_files = get_excel_files()
    for i in all_files:
        df = pd.read_excel(i)
        error_main = df["故障所属主系统"].value_counts()
        error_main.plot(kind="bar", label="各系统故障率统计图")
        plt.title("各系统故障率统计图")
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.legend(loc="best")
        plt.show()


if __name__ == '__main__':
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    statistic_excel()
