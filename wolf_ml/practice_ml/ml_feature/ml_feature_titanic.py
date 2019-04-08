# coding=utf-8

"""
    主要是分析Titanic数据
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from pandas import DataFrame, Series


rfr = None
scaler = None
age_scale_param = None
fare_scale_param = None

def load_data():
    return pd.read_csv(train_file)

def f1():
    """
        数据总体概括
    """

    print(df_train.columns)
    print("=="*64)
    print(df_train.Survived.value_counts())
    print("=="*64)
    print(df_train[df_train.Cabin.notnull()]['Survived'].value_counts())
    print("=="*64)
    print(df_train.info())
    print("=="*64)
    print(df_train.describe())

def f2():
    """
        详细统计分析
    """

    fig = plt.figure()
    fig.set(alpha=0.2)

    plt.subplot2grid((2,3), (0,0))
    df_train.Survived.value_counts().plot(kind="bar")
    plt.title("获救情况 (1为获救)")
    plt.ylabel("人数")

    plt.subplot2grid((2,3),(0,1))
    df_train.Pclass.value_counts().plot(kind="bar")
    plt.title("乘客等级分布")
    plt.ylabel("人数")

    plt.subplot2grid((2,3),(0,2))
    plt.scatter(df_train.Survived, df_train.Age)
    plt.title("年龄看获救分布")
    plt.ylabel("年龄")
    plt.grid(b=True, axis='y')

    plt.subplot2grid((2,3),(1,0), colspan=2)
    df_train.Age[df_train.Pclass==1].plot(kind="kde")
    df_train.Age[df_train.Pclass==2].plot(kind="kde")
    df_train.Age[df_train.Pclass==3].plot(kind="kde")
    plt.xlabel("年龄")
    plt.ylabel("密度")
    plt.title("各等级的年龄分布")
    plt.legend(("头等舱","二等舱","三等舱"), loc="best")

    plt.subplot2grid((2,3), (1,2))
    df_train.Embarked.value_counts().plot(kind="bar")
    plt.title("各个登船岸口上船人数")
    plt.ylabel("人数")

    plt.show()


def f3():
    """
        查看乘客等级的获救情况
        结果：
            仓位越好，获救概率越高
    """
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams['axes.unicode_minus'] = False

    #fig = plt.figure()
    #fig.set(alpha=0.2)
    #fig.suptitle("乘客等级的获救情况")

    survived_0 = df_train.Pclass[df_train.Survived==0].value_counts()
    survived_1 = df_train.Pclass[df_train.Survived==1].value_counts()
    df1 = DataFrame({"获救":survived_1,"为获救":survived_0})
    print('df1=',df1)
    ax1 = df1.plot(kind="bar", stacked=False)
    plt.title("看各个等级的获救情况")
    plt.xlabel("乘客等级")
    plt.ylabel("人数")
    plt.legend()
    plt.show()


def f4():
    """
        查看登岸口获救情况
        结果：
            为得出明显结论
    """

    survived_0 = df_train.Embarked[df_train.Survived==0].value_counts()
    survived_1 = df_train.Embarked[df_train.Survived==1].value_counts()
    df1 = DataFrame({"获救":survived_1,"未获救":survived_0})
    ax1 = df1.plot(kind="bar", stacked=True)
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(0)
    plt.title("各个登岸口获救情况")
    plt.xlabel("登岸口")
    plt.ylabel("人数")
    plt.legend()
    plt.show()


def f5():
    """
        性别与获救情况关系
    """
    survived_male = df_train.Survived[df_train.Sex=="male"].value_counts()
    survived_female = df_train.Survived[df_train.Sex=="female"].value_counts()
    df1 = DataFrame({"male":survived_male, "female":survived_female})
    df1.plot(kind="bar", stacked=True)
    plt.title("性别与获救关系")
    plt.xlabel("是否获救(1获救)")
    plt.ylabel("人数")
    plt.legend()
    plt.show()

def f6():
    """
        详细分析各个舱级别各个性别获救
    """
    fig = plt.figure()
    fig.set(alpha=0.2)
    plt.suptitle("舱位等级下性别获救情况")

    ax1 = plt.subplot2grid((2,2), (0,0))
    df_train.Survived[df_train.Sex=="female"][df_train.Pclass!=3].value_counts().plot(kind="bar", label="女性高级舱")
    print(df_train.Survived[df_train.Sex=="female"][df_train.Pclass!=3].value_counts())
    # rotation 显示倾斜角度
    ax1.set_xticklabels(["获救","未获救"], rotation=0)
    #plt.title("女性高级舱")
    #plt.xlabel("是否获救")
    plt.ylabel("人数")
    plt.legend(["女性/高级舱"])

    ax2 = plt.subplot2grid((2,2),(0,1))
    df_train.Survived[df_train.Sex=="female"][df_train.Pclass==3].value_counts().plot(kind="bar")
    print(df_train.Survived[df_train.Sex=="female"][df_train.Pclass==3].value_counts())
    ax2.set_xticklabels(["获救","未获救"], rotation=0)
    #plt.title("女性低级舱")
    #plt.xlabel("是否获救")
    plt.ylabel("人数")
    plt.legend(["女性/低级舱"])

    ax3 = plt.subplot2grid((2,2), (1,0))
    df_train.Survived[df_train.Sex=="male"][df_train.Pclass!=3].value_counts().plot(kind="bar")
    ax3.set_xticklabels(["获救","未获救"], rotation=0)
    plt.ylabel("人数")
    plt.legend(["男性/高级舱"])

    ax4 = plt.subplot2grid((2,2),(1,1))
    df_train.Survived[df_train.Sex=="male"][df_train.Pclass==3].value_counts().plot(kind="bar")
    ax4.set_xticklabels(["获救","未获救"],rotation=0)
    plt.legend(["男性/低级舱"])

    plt.show()


def f7():
    """
        堂兄弟，父母特征统计
    """
    g = df_train.groupby(["SibSp","Survived"])
    print(g.count())
    print("=="*64)
    df1 = DataFrame(g.count()["PassengerId"])
    print(df1)
    print("=="*64)

    g2 = df_train.groupby(["Parch", "Survived"])
    df2 = DataFrame(g2.count()["PassengerId"])
    print(df2)
    print("=="*64)

def f8():
    """
        cabin的值计数太分散了，绝大多数Cabin值只出现一次。感觉上作为类目，加入特征未必会有效，那看看这个值的有无，对于survival的分布状况，影响如何
    """
    #fig = plt.figure()
    #fig.set(alpha=0.2)

    survived_hasC = df_train.Survived[pd.notnull(df_train.Cabin)].value_counts()
    survived_noC = df_train.Survived[pd.isnull(df_train.Cabin)].value_counts()
    #df1 = DataFrame({"有":survived_hasC, "无":survived_noC})
    df1 = DataFrame({"有":survived_hasC, "无":survived_noC}).transpose()
    df1.plot(kind="bar", stacked=True)
    plt.title("根据Cabin是否有无看获救情况")
    plt.ylabel("人数")
    plt.xlabel(u"Cabin有无")
    plt.show()


def f9():
    """
        使用模型对年龄空值进行简单填充，将数值型特征直接丢进RandomForestRegressor模型中，进行预测
    """
    print(df_train.Survived[df_train.Age.notnull()].value_counts())

    from sklearn.ensemble import RandomForestRegressor
    age_feature_df = df_train[['Age','Fare', 'Parch', 'SibSp', 'Pclass']]
    known_age = age_feature_df[age_feature_df.Age.notnull()].as_matrix()
    unknown_age = age_feature_df[age_feature_df.Age.isnull()].as_matrix()

    y = known_age[:, 0]
    x = known_age[:, 1:]

    global rfr
    rfr = RandomForestRegressor(random_state=0, n_estimators=2000, n_jobs=-1)
    rfr.fit(x,y)

    x_test = unknown_age[:,1:]
    y_test = rfr.predict(x_test)
    df_train.loc[(df_train.Age.isnull()), "Age"] = y_test
    print(df_train.Survived[df_train.Age.notnull()].value_counts())
    return df_train


def set_Cabin(data_set):
    # 两个顺序设置不一样导致结果不一样，具体原因后面分析????
    #data_set.loc[(data_set.Cabin.isnull()), "Cabin"] = "No"
    #data_set.loc[(data_set.Cabin.notnull()), "Cabin"] = "Yes"

    data_set.loc[(data_set.Cabin.notnull()), "Cabin"] = "Yes"
    data_set.loc[(data_set.Cabin.isnull()), "Cabin"] = "No"
    return data_set


def f10():
    """
        对类目型的特征离散/因子化
    """
    df_train = f9()

    set_Cabin(df_train)

    dummies_Cabin = pd.get_dummies(df_train["Cabin"], prefix="Cabin")
    dummies_Embarked = pd.get_dummies(df_train["Embarked"], prefix="Embarked")
    dummies_Sex = pd.get_dummies(df_train["Sex"], prefix="Sex")
    dummies_Pclass = pd.get_dummies(df_train["Pclass"], prefix="Pclass")

    df_train = pd.concat([df_train, dummies_Cabin, dummies_Embarked, dummies_Sex, dummies_Pclass], axis=1)
    df_train.drop(['Pclass', 'Name', 'Sex', 'Ticket', 'Cabin', 'Embarked'], axis=1, inplace=True)
    print(df_train.head())
    print("=="*64)
    """
        无量纲化，对Age和Fare
    """
    from sklearn.preprocessing import StandardScaler
    global scaler
    scaler = StandardScaler()
    # 原因是 sklearn 的新版本中，fit_transform的输入必须是 2-D array，而 data_train['Fare'] 返回的 Series 本质上是 1-D array
    # 下面方法使用时，会报错，ValueError: Expected 2D array, got 1D array instead:
    # df_train["Age"] = scaler.fit_transform(df_train["Age"])
    age_scale_param = scaler.fit(df_train[['Age']])
    df_train["Age_scaled"] = scaler.fit_transform(df_train[["Age"]], age_scale_param)
    fare_scale_param = scaler.fit(df_train[["Fare"]])
    df_train["Fare_scaled"] = scaler.fit_transform(df_train[["Fare"]], fare_scale_param)
    print(df_train.head())
    return df_train

def f11():
    """
        转换成array形式进行建模
    """
    df_train = f10()
    train_data = df_train.filter(regex='Survived|Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    print(train_data.head())
    print("=="*64)
    train_data = train_data.as_matrix()
    print(train_data)
    print("=="*64)
    X = train_data[:,1:]
    y = train_data[:,0]
    from sklearn.linear_model import LogisticRegression
    lr = LogisticRegression(penalty='l1', C=1.0)
    lr.fit(X, y)
    
    return lr


def f12():
    """
        对测试集做相同操作，构造特征
    """
    lr = f11()
    df_test = pd.read_csv("test.csv")

    df_test.loc[(df_test.Fare.isnull()), "Fare"] = 0
    tmp_df = df_test[['Age','Fare', 'Parch', 'SibSp', 'Pclass']]
    null_age = tmp_df[(df_test.Age.isnull())].as_matrix()
    X = null_age[:, 1:]
    global rfr
    predict_ages = rfr.predict(X)
    df_test.loc[(df_test.Age.isnull()), "Age"] = predict_ages
    df_test = set_Cabin(df_test)
    print(df_test)
    print("=="*64)
    dummies_Cabin = pd.get_dummies(df_test["Cabin"], prefix="Cabin")
    dummies_Embarked = pd.get_dummies(df_test["Embarked"], prefix="Embarked")
    dummies_Sex = pd.get_dummies(df_test["Sex"], prefix="Sex")
    dummies_Pclass = pd.get_dummies(df_test["Pclass"], prefix="Pclass")
    df_test = pd.concat([df_test, dummies_Cabin, dummies_Embarked, dummies_Sex, dummies_Pclass], axis=1)
    df_test.drop(['Pclass', 'Name', 'Sex', 'Ticket', 'Cabin', 'Embarked'], axis=1, inplace=True)
    global scaler, fare_scale_param, age_scale_param
    df_test["Age_scaled"] = scaler.fit_transform(df_test[["Age"]], age_scale_param)
    df_test["Fare_scaled"] = scaler.fit_transform(df_test[["Fare"]], fare_scale_param)
    print(df_test.head())
    print("df_test ==" * 64)
    test_data = df_test.filter(regex='Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    predictions = lr.predict(test_data)
    result = DataFrame({"PassengerId":df_test["PassengerId"].as_matrix(),"Survived":predictions.astype(np.int32)})
    result.to_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "logistic_regression_predictions.csv"), index=False)


if __name__ == '__main__':
    train_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "train.csv")
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test.csv")
    df_train = pd.read_csv(train_file)

    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams['axes.unicode_minus'] = False

    #f1()
    #f2()
    #f3()
    #f4()
    #f5()
    #f6()
    #f7()
    #f8()
    #f9()
    #f10()
    #f11()
    f12()


