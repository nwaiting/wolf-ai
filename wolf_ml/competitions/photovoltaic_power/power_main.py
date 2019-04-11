#coding=utf-8

import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from power_model import PredictPowerByModel
from optparse import OptionParser

def main(model_name):
    if model_name == "xgboost":
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "results_xgb.csv")
        PredictPowerByModel(model_name="xgboost").predict_data(file_name)
    elif model_name == "lightgbm":
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "results_lgm.csv")
        PredictPowerByModel(model_name="lightgbm").predict_data(file_name)
    elif model_name == "svr"
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "results_svr.csv")
        PredictPowerByModel(model_name="svr").predict_data(file_name)
    elif model_name == "stack":
        pass

if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option('-m',
                    action="store",
                    dest="model_name",
                    type="string",
                    default="xgboost",
                    help="run the scripts daemon")
    opts, args = opt.parse_args()
    model_name = opts.model_name
    main(model_name)
