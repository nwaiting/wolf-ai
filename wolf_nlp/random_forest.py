#coding=utf-8
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import pandas as pd
import numpy as np

from matplotlib.pylab import *

def random_forest():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75
    df['species'] = pd.Factor(iris.target, iris.target_names)
    pd.factorize
    df.head()

    train, test = df[df['is_train']==True], df[df['is_train']==False]

    features = df.columns[:4]
    clf = RandomForestClassifier(n_jobs=2)
    y, _ = pd.factorize(train['species'])
    clf.fit(train[features], y)

    preds = iris.target_names[clf.predict(test[features])]
    pd.crosstab(test['species'], preds, rownames=['actual'], colnames=['preds'])

def myshow():
    def f(x,y): return (1-x/2+x**5+y**3)*np.exp(-x**2-y**2)
    n = 256
    x = np.linspace(-3,3,n)
    y = np.linspace(-3,3,n)
    X,Y = np.meshgrid(x,y)

    contourf(X, Y, f(X,Y), 8, alpha=.75, cmap='jet')
    C = contour(X, Y, f(X,Y), 8, colors='black', linewidth=.5)
    show()

if __name__ == '__main__':
    #random_forest()
    myshow()
