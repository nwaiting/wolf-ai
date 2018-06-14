#coding=utf-8

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import re
import time
import os

class LanguageDetector(object):
    def __init__(self,classifier=MultinomialNB(), vectorizer=None):
        self.classifier = classifier
        if vectorizer:
            self.vectorizer = vectorizer
        else:
            self.vectorizer = CountVectorizer(lowercase=True, analyzer='char_wb', ngram_range=(1, 2), max_features=1000, preprocessor=self.remove_noise)

    def remove_noise(self, doc):
        noise_pattern = re.compile('|'.join(['http\S+', '\@\w+', '\#\w+']))
        text_clean = re.sub(noise_pattern, '', doc)
        return text_clean

    def features(self, X):
        return self.vectorizer.transform(X).toarray()

    def fit(self, X, y):
        self.vectorizer.fit(X)
        self.classifier.fit(self.features(X), y)

    def predict(self, X):
        return self.classifier.predict(self.features([X]))

    def score(self, X, y):
        return self.classifier.score(self.features(X), y)


def func1(file):
    data_list = []
    with open(file=file) as fd:
        data_list = [(line.strip()[:-3], line.strip()[-2:]) for line in fd.readlines()]
    x,y = zip(*data_list)
    x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=int(time.time()))
    language_detector = LanguageDetector()
    language_detector.fit(x_train, y_train)
    for item in ['this is english', 'van hout vrijspraak', 'poursuite du processus']:
        res = language_detector.predict(item)
        print(res)

    res = language_detector.score(x_test, y_test)
    print(res)

if __name__ == '__main__':
    file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.csv')
    func1(file_name)
    #print(help(CountVectorizer))
