#coding=utf-8

import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from power_model import get_model, predict_data

def main():
    model = get_model("xgboost")

    file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "results.csv")
    predict_data(model, file_name)

if __name__ == '__main__':
    main()
