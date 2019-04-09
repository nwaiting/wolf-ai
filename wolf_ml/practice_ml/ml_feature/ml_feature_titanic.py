# coding=utf-8

"""
    主要是分析Titanic数据
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split,learning_curve
from pandas import DataFrame, Series

# 对每次迭代结果进行输出
from sklearn.metrics import classification_report
from sklearn.externals import joblib

"""
    构建特征：
        首先进行简单的特征统计与结果的相关性，先做一个baseline

        Sex属性，如果是female会极大提高最后获救的概率，而male会很大程度拉低这个概率。
        Pclass属性，1等舱乘客最后获救的概率会上升，而乘客等级为3会极大地拉低这个概率。
        有Cabin值会很大程度拉升最后获救概率(这里似乎能看到了一点端倪，事实上从最上面的有无Cabin记录的Survived分布图上看出，即使有Cabin记录的乘客也有一部分遇难了，估计这个属性上我们挖掘还不够)
        Age是一个负相关，意味着在我们的模型里，年龄越小，越有获救的优先权(还得回原数据看看这个是否合理）
        有一个登船港口S会很大程度拉低获救的概率，另外俩港口压根就没啥作用(这个实际上非常奇怪，因为我们从之前的统计图上并没有看到S港口的获救率非常低，所以也许可以考虑把登船港口这个feature去掉试试)。
        船票Fare有小幅度的正相关(并不意味着这个feature作用不大，有可能是我们细化的程度还不够，举个例子，说不定我们得对它离散化，再分至各个乘客等级上？)

        比如说Name和Ticket两个属性被我们完整舍弃了(好吧，其实是一开始我们对于这种，每一条记录都是一个完全不同的值的属性，并没有很直接的处理方式)
        比如说，我们想想，年龄的拟合本身也未必是一件非常靠谱的事情
        另外，以我们的日常经验，小盆友和老人可能得到的照顾会多一些，这样看的话，年龄作为一个连续值，给一个固定的系数，似乎体现不出两头受照顾的实际情况，所以，说不定我们把年龄离散化，按区段分作类别属性会更合适一些

    特征优化操作：
        Age属性不使用现在的拟合方式，而是根据名称中的『Mr』『Mrs』『Miss』等的平均值进行填充。
        Age不做成一个连续值属性，而是使用一个步长进行离散化，变成离散的类目feature。
        Cabin再细化一些，对于有记录的Cabin属性，我们将其分为前面的字母部分(我猜是位置和船层之类的信息) 和 后面的数字部分(应该是房间号，有意思的事情是，如果你仔细看看原始数据，你会发现，这个值大的情况下，似乎获救的可能性高一些)。
        Pclass和Sex俩太重要了，我们试着用它们去组出一个组合属性来试试，这也是另外一种程度的细化。
        单加一个Child字段，Age<=12的，设为1，其余为0(你去看看数据，确实小盆友优先程度很高啊)
        如果名字里面有『Mrs』，而Parch>1的，我们猜测她可能是一个母亲，应该获救的概率也会提高，因此可以多加一个Mother字段，此种情况下设为1，其余情况下设为0
        登船港口可以考虑先去掉试试(Q和C本来就没权重，S有点诡异)
        把堂兄弟/兄妹 和 Parch 还有自己 个数加在一起组一个Family_size字段(考虑到大家族可能对最后的结果有影响)
        Name是一个我们一直没有触碰的属性，我们可以做一些简单的处理，比如说男性中带某些字眼的(‘Capt’, ‘Don’, ‘Major’, ‘Sir’)可以统一到一个Title，女性也一样。

    相关内容：
        1、先进行统计，选择特征
        2、特征预处理，离散化、无量纲化、dummy化
        3、空值处理（简单填充，模型简单预测）
        4、判断当前模型状态（是否过拟合/欠拟合）
        5、特征细化（挖掘深层次特征、隐含特征、组合特征）
            对比bad case和预测正确的case，继续挖掘深层的特征
        6、交叉验证（验证细化特征的有效性）
        7、模型融合

    特征组合：
        使用特征组合 + 大量数据是学习高度复杂模型的一种有效策略

        在做组合特征的时候，如果只是简单的进行两两组合，很容易导致参数过多、多拟合等问题，而且并不是所有的特征组合都有意义。
        特征组合方法：（类似于ngram组合）
            所以该怎么进行有效的特征组合呢，最常用的是基于决策树的特征组合寻找方法，在将训练数据构造成一棵决策树之后，每一条从根节点到叶节点的路径都可以看成是一种特征组合的方式
        例如
            案例1：
                做影视推荐模型的时候，原始输入特征有年龄、性别（男，女）、用户类型（已工作，学生），类型（电影，电视剧）4个特征信息，它的标签是（观看/未观看），
                根据这些信息构造决策树，可以得到4种特征组合的方式：1）年龄30性别=女，2）年龄30类型=电视剧，3)用户类型=已工作类型=电影，4）用户类型=已工作年龄=30
            案例2：
                组合 latitude 和 longitude 特征（例如，假设 longitude 被分到 2 个分桶中，而 latitude 有 3 个分桶），
                组合后实际上会得到 6 个组合的二元特征。当训练模型时，每个特征都会分别获得自己的权重
            案例3：
                做影视推荐模型的时候，有语言（中文，英文）和类型（电影，电视剧）这两种离散特征，做了组合特征之后，变成了2x2=4个特征：语言=中文类型=电影，语言=中文类型=电视剧，语言=英文类型=电影，语言=英文类型=电视剧


    模型验证的五种方法：
        一、通过交叉验证计算得分（model_selection.cross_val_score(estimator,x)）
            将数据集分为10折，做一次交叉验证，实际上它是计算了十次，将每一折都当做一次测试集，其余九折当做训练集，这样循环十次。通过传入的模型，训练十次，最后将十次结果求平均值。将每个数据集都算一次
                1、交叉验证用于评估模型的预测性能，尤其是训练好的模型在新数据上的表现，可以在一定程度上减小过拟合。
                2、还可以从有限的数据中获取尽可能多的有效信息。
        二、对每一个输入数据点产生交叉验证估计（model_selection.cross_val_predict(estimator,x)）
        三、计算绘制模型的学习率曲线（model_selection.learning_curve(estimator,x,y)）
        四、计算并绘制模型验证曲线（model_selection.validation_curve(estimator…)）
        五、通过排序评估交叉验证得分的重要性（model_selection.permatation_test_score()）
        参考：http://studyai.com/article/c8a5e7dd


"""

rfr = None
scaler = None
age_scale_param = None
fare_scale_param = None
lr = None

def load_data():
    return pd.read_csv(train_file)

def load_train_data():
    train_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "train.csv")
    df_train = pd.read_csv(train_file)
    return df_train

def load_test_data():
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test.csv")
    df_test = pd.read_csv(test_file)
    return df_test

def f1():
    """
        数据总体概括
    """
    df_train = load_train_data()
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

    df_train = load_train_data()
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

    df_train = load_train_data()
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
    df_train = load_train_data()
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
    df_train = load_train_data()
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
    df_train = load_train_data()
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
    df_train = load_train_data()
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
    df_train = load_train_data()
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
    df_train = load_train_data()
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
    #df_train.drop(['Pclass', 'Name', 'Sex', 'Ticket', 'Cabin', 'Embarked'], axis=1, inplace=True)
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
    global lr
    lr = LogisticRegression(penalty='l1', C=1.0)
    lr.fit(X, y)
    plot_learning_curve(lr, "学习曲线", X, y)
    return lr,df_train


def plot_learning_curve(estimator,title,X,y,ylim=None,cv=None,n_jobs=-1,train_size=np.linspace(0.05,1.0,10),verbose=0,plot=True):
    train_sizes,train_scores,test_scores = learning_curve(estimator,X,y,train_sizes=train_size,cv=cv,n_jobs=n_jobs,verbose=verbose)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    if plot:
        plt.figure()
        plt.title(title)
        if ylim:
            # 设置y轴范围
            plt.ylim(*ylim)
        plt.xlabel("训练样本")
        plt.ylabel("得分")
        # y轴反向
        plt.gca().invert_yaxis()
        plt.grid()
        plt.fill_between(train_sizes, train_scores_mean-train_scores_std, train_scores_mean+train_scores_std,alpha=0.1,color='r')
        plt.fill_between(train_sizes,test_scores_mean-test_scores_std, test_scores_mean+test_scores_std,alpha=0.1,color='g')
        plt.plot(train_sizes,train_scores_mean,'o-',color='r',label="训练集上得分")
        plt.plot(train_sizes,test_scores_mean,'o-',color='g',label="交叉验证集上得分")
        plt.legend(loc='best')
        plt.draw()
        plt.gca().invert_yaxis()
        plt.show()
    midpoint = ((train_scores_mean[-1]+train_scores_std[-1]) + (test_scores_mean[-1]-test_scores_std[-1]))/2
    diff = ((train_scores_mean[-1]+train_scores_std[-1]) - (test_scores_mean[-1]-test_scores_std[-1]))/2
    return midpoint,diff

def f12():
    """
        对测试集做相同操作，构造特征
    """
    global lr
    lr,df_train = f11()
    df_test = load_test_data()

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
    result_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logistic_regression_predictions.csv")
    print(result_file)
    result.to_csv(result_file, index=False)

    # 添加组合特征
    df_train["Sex_Pclass"] = df_train.Sex + "_" + df_train.Pclass.map(str)
    dummies_Sex_Pclass = pd.get_dummies(df_train.Sex_Pclass, prefix="Sex_Pclass")
    df_train = pd.concat([df_train, dummies_Sex_Pclass], axis=1)
    df_train.drop(["Sex_Pclass"], axis=1, inplace=True)

    # 先看一下打分情况
    train_data = df_train.filter(regex="Survived|Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*|Sex_Pclass_.*")
    #print(train_data.head())
    #print("=="*64)
    X = train_data.as_matrix()[:,1:]
    y = train_data.as_matrix()[:,0]
    from sklearn.model_selection import cross_val_score
    print("cross_val_score=",cross_val_score(lr, X, y, cv=5))
    print("=="*64)

    # 对比base case，分析还有哪些特征需要细化
    train_data_split,test_data_split = train_test_split(df_train, test_size=0.3, random_state=0)
    train_data_split = train_data_split.filter(regex="Survived|Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*|Sex_Pclass_.*")
    train_data_split = train_data_split.as_matrix()
    lr.fit(train_data_split[:,1:], train_data_split[:,0])

    test_data = test_data_split.filter(regex="Survived|Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*|Sex_Pclass_.*")
    test_data = test_data.as_matrix()
    predictions = lr.predict(test_data[:,1:])
    # 下面的方法直接运行有问题，会报错，因为drop()函数的调用方法，必须有参数labels='某个字段'，指定即可！
    # 或者也可以尝试去掉drop函数直接输出！ 解决问题
    bad_cases = test_data_split[predictions != test_data[:,0]]

    origin_df_train = load_train_data()
    bad_cases_to_file = origin_df_train.loc[origin_df_train.PassengerId.isin(test_data_split[predictions != test_data[:,0]].PassengerId.values)]
    result_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bad_cases.csv")
    bad_cases_to_file.to_csv(result_file, index=False)

    #print(bad_cases)
    #print("=="*64)


def f13():
    """
        继续挖掘特征
    """
    df_train = load_train_data()
    print(df_train[df_train["Name"].str.contains("Major")])


def string_in_string(full_string, string_list):
    #print("full string {}".format(full_string))
    for s in string_list:
        if full_string.find(s) != -1:
            return s
    return np.nan


def f14():
    """
        数据清洗、预处理
    """
    df_train = load_train_data()
    print(df_train.head())
    # 处理Fare空值，下面两种方法都可以
    #df_train.Fare = df_train.Fare.map(lambda x:np.nan if x==0 else x)
    df_train["Fare"] = df_train["Fare"].map(lambda x:np.nan if x==0 else x)

    # 处理名字，生成title字段
    title_list = ['Mrs', 'Mr', 'Master', 'Miss', 'Major', 'Rev',
                'Dr', 'Ms', 'Mlle','Col', 'Capt', 'Mme', 'Countess',
                'Don', 'Jonkheer']
    df_train["Title"] = df_train["Name"].map(lambda x:string_in_string(x, title_list))


    #对于特殊称呼，全处理成mr, mrs, miss, master
    def handler_title(x):
        title = x["Title"]
        if title in ['Mr','Don', 'Major', 'Capt', 'Jonkheer', 'Rev', 'Col']:
            return "Mr"
        elif title in ['Master']:
            return "Master"
        elif title in ['Countess', 'Mme','Mrs']:
            return "Mrs"
        elif title in ['Mlle', 'Ms','Miss']:
            return "Miss"
        elif title == "Dr":
            if x["Sex"] == "Male":
                return "Mr"
            else:
                return "Mrs"
        elif title == "":
            if x["Sex"] == "Male":
                return "Master"
            else:
                return "Miss"
        else:
            return title
    df_train["Title"] = df_train.apply(handler_title, axis=1)
    df_train["Family_Size"] = df_train["SibSp"] + df_train["Parch"]
    df_train["Family"] = df_train["SibSp"]*df_train["Parch"]
    df_train.loc[(df_train["Fare"].isnull()) & (df_train["Pclass"]==1), "Fare"] = np.median(df_train[df_train["Pclass"]==1]["Fare"].dropna())
    df_train.loc[(df_train["Fare"].isnull()) & (df_train["Pclass"]==2), "Fare"] = np.median(df_train[df_train["Pclass"]==2]["Fare"].dropna())
    df_train.loc[(df_train["Fare"].isnull()) & (df_train["Pclass"]==3), "Fare"] = np.median(df_train[df_train["Pclass"]==3]["Fare"].dropna())
    df_train["Gender"] = df_train["Sex"].map({"female":0,"male":1}).astype(int)
    df_train["AgeFill"] = df_train["Age"]
    mean_ages = np.zeros(4)
    mean_ages[0] = np.average(df_train[df_train["Title"]=="Miss"]["Age"].dropna())
    mean_ages[1] = np.average(df_train[df_train["Title"]=="Mrs"]["Age"].dropna())
    mean_ages[2] = np.average(df_train[df_train["Title"]=="Mr"]["Age"].dropna())
    mean_ages[3] = np.average(df_train[df_train["Title"]=="Master"]["Age"].dropna())

    # 里面的条件一定要加括号，不然会报错 TypeError: invalid type comparison
    df_train.loc[(df_train["Age"].isnull()) & (df_train["Title"]=="Miss"), "AgeFill"] = mean_ages[0]
    df_train.loc[(df_train["Age"].isnull()) & (df_train["Title"]=="Mrs"), "AgeFill"] = mean_ages[1]
    df_train.loc[(df_train["Age"].isnull()) & (df_train["Title"]=="Mr"), "AgeFill"] = mean_ages[2]
    df_train.loc[(df_train["Age"].isnull()) & (df_train["Title"]=="Master"), "AgeFill"] = mean_ages[3]
    df_train["AgeCat"] = df_train["AgeFill"]

    # 第一次比较之后，后面有的AgeCat字段就为str，所以后面比较会报错
    #df_train.loc[df_train["AgeCat"]<=10, "AgeCat"] = "child"
    #df_train.loc[df_train["AgeCat"]>10 & df_train["AgeCat"]<=30, "AgeCat"] = "adult"
    #df_train.loc[df_train["AgeCat"]>30 & df_train["AgeCat"]<=60, "AgeCat"] = "senior"
    #df_train.loc[df_train["AgeCat"]>60, "AgeCat"] = "aged"
    def handler_agecat(x):
        age = x["AgeCat"]
        if age <= 10:
            return "child"
        elif age > 10 and age <= 30:
            return "adult"
        elif age > 30 and age <= 60:
            return "senior"
        else:
            return "aged"
    df_train["AgeCat"] = df_train.apply(handler_agecat, axis=1)

    df_train["Embarked"] = df_train["Embarked"].fillna("S")

    df_train.loc[(df_train["Cabin"].isnull()==True), "Cabin"] = 0.5
    df_train.loc[(df_train["Cabin"].isnull()==False), "Cabin"] = 1.5


    df_train["Fare_Per_Person"] = df_train["Fare"] / (df_train["Family_Size"]+1)

    # age times class
    df_train["AgeClass"] = df_train["AgeFill"]*df_train["Pclass"]
    df_train["ClassFare"] = df_train["Pclass"]*df_train["Fare_Per_Person"]

    df_train["HighLow"] = df_train["Pclass"]
    df_train.loc[(df_train["Fare_Per_Person"]>=8), "HighLow"] = "High"
    df_train.loc[(df_train["Fare_Per_Person"]<8), "HighLow"]= "Low"

    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    x_sex = le.fit_transform(df_train["Sex"])
    # 会报错
    # df_train.loc["Sex"] = x_sex.astype(int)
    df_train["Sex"] = x_sex.astype(np.float)

    x_ticket = le.fit_transform(df_train["Ticket"])
    df_train["Ticket_Label"] = x_ticket.astype(np.float)

    x_title = le.fit_transform(df_train["Title"])
    df_train["Title_Label"] = x_title.astype(np.float)

    x_highlow = le.fit_transform(df_train["HighLow"])
    df_train["HighLow_Label"] = x_highlow.astype(np.float)

    x_agecat = le.fit_transform(df_train["AgeCat"])
    df_train["AgeCat_Label"] = x_agecat.astype(np.float)

    x_embarked = le.fit_transform(df_train["Embarked"])
    df_train["Embarked_Label"] = x_embarked.astype(np.float)

    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "feature_file.csv")
    df_train.to_csv(file_path, index=0)

    print("==" * 64)
    print(df_train.head())
    print("==" * 64)
























if __name__ == '__main__':
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
    #f12()
    #f13()
    f14()
