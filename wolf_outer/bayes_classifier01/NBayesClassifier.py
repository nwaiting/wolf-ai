#coding=utf-8
import os
from sklearn.naive_bayes import MultinomialNB

def genLocalPath(file_name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)

def genFeature(file_name):
    pass

def textClassifier(train_feature_list,train_class_list,test_feature_list,test_class_list):
    pass

if __name__ == '__main__':
    train_file = ''
    test_file = ''
    train_file = genLocalPath(train_file)
    test_file = genLocalPath(test_file)
