#coding=utf-8

import os
import pandas as pd
import matplotlib.pyplot as plt

"""
    kaggle的一个题目：https://www.kaggle.com/c/titanic/data
"""

def titanic(train_file, test_file):
    pf_train = pd.read_csv(train_file)
    #print(pf_train.columns)
    #print(pf_train.head())
    #print(pf_train.info())
    #print(pf_train.describe())

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    """
    fig = plt.figure()
    fig.set(alpha=0.2) #设置图表颜色alpha参数，设置图片透明度

    plt.subplot2grid((2,3),(0,0)) #一张大图里分裂几个小图
    pf_train.Survived.value_counts().plot(kind='bar') # plots a bar graph of those who surived vs those who did not
    plt.title("获救情况（1为获救）")
    plt.ylabel("人数")

    plt.subplot2grid((2,3), (0,1))
    pf_train.Pclass.value_counts().plot(kind='bar')
    plt.title("乘客等级分布")
    plt.ylabel("人数")

    plt.subplot2grid((2,3), (0,2))
    plt.scatter(pf_train.Survived, pf_train.Age)
    plt.grid(b=True, which='major', axis='y')
    plt.title("年龄看获救分布（1为获救）")
    plt.ylabel("年龄")

    plt.subplot2grid((2,3), (1,0), colspan=2)
    pf_train.Age[pf_train.Pclass==1].plot(kind='kde')
    pf_train.Age[pf_train.Pclass==2].plot(kind='kde')
    pf_train.Age[pf_train.Pclass==3].plot(kind='kde')
    plt.xlabel("年龄")
    plt.ylabel("密度")
    plt.title("各等级的乘客年龄分布")
    plt.legend(("头等舱","2等仓","3等仓"), loc='best')

    plt.subplot2grid((2,3),(1,2))
    pf_train.Embarked.value_counts().plot(kind='bar')
    plt.title("各登船口岸上船人数")
    plt.ylabel("人数")
    #plt.show()

    #查看各乘客等级的获救情况
    fig = plt.figure()
    fig.set(alpha=0.2)
    Survived_0 = pf_train.Pclass[pf_train.Survived==0].value_counts()
    Survived_1 = pf_train.Pclass[pf_train.Survived==1].value_counts()
    df = pd.DataFrame({"获救":Survived_1,"未获救":Survived_0})
    df.plot(kind='bar', stacked=True)
    plt.title("乘客各等级的获救情况")
    plt.xlabel("乘客等级")
    plt.ylabel("人数")
    #plt.show()

    #查看各登录港口获救的情况
    fig = plt.figure()
    fig.set(alpha=0.2) #设置图标颜色参数
    Survived_0 = pf_train.Embarked[pf_train.Survived==0].value_counts()
    Survived_1 = pf_train.Embarked[pf_train.Survived==1].value_counts()
    df = pd.DataFrame({"获救":Survived_1, "未获救":Survived_0})
    df.plot(kind="bar", stacked=True)
    plt.title("各登录港口乘客获救情况")
    plt.ylabel("登录港口")
    plt.xlabel("人数")
    #plt.show()

    #看看个性别的获救情况
    fig = plt.figure()
    fig.set(alpha=0.2)
    Survived_m = pf_train.Survived[pf_train.Sex=='male'].value_counts()
    Survived_f = pf_train.Survived[pf_train.Sex=='female'].value_counts()
    df=pd.DataFrame({"男性":Survived_m,"女性":Survived_f})
    df.plot(kind="bar", stacked=False) #stacked设置是否堆叠起来
    plt.title("按性别看获救情况")
    plt.xlabel("性别")
    plt.ylabel("人数")
    plt.show()
    """

    """
    #查看一下各个舱级别情况下各性别的获救情况
    fig = plt.figure()
    fig.set(alpha=0.65) #设置图像的透明度
    plt.title("根据舱等级和性别的获救情况")

    ax1 = fig.add_subplot(141)
    pf_train.Survived[pf_train.Sex=='female'][pf_train.Pclass!=3].value_counts().plot(kind="bar", label='female high class', color='#FA2479')
    ax1.set_xticklabels(["获救","未获救"],rotation=0)
    plt.legend(["女性/高级舱"], loc="best")

    ax2 = fig.add_subplot(142, sharey=ax1)
    pf_train.Survived[pf_train.Sex=='female'][pf_train.Pclass==3].value_counts().plot(kind="bar", label="female low class", color='pink')
    ax2.set_xticklabels(["未获救","获救"], rotation=0)
    plt.legend(["女性/低级舱"], loc="best")

    ax3 = fig.add_subplot(143, sharey=ax1)
    pf_train.Survived[pf_train.Sex=='male'][pf_train.Pclass!=3].value_counts().plot(kind="bar", label='male high class', color='lightblue')
    ax3.set_xticklabels(["未获救","获救"],rotation=0)
    plt.legend(["男性/高级舱"], loc='best')

    ax4 = fig.add_subplot(144, sharey=ax1)
    pf_train.Survived[pf_train.Sex=='male'][pf_train.Pclass==3].value_counts().plot(kind='bar', label='male low class', color='steelblue')
    ax4.set_xticklabels(['未获救','获救'], rotation=0)
    plt.legend(["男性/低级舱"], loc='best')

    plt.show()
    """

    """
    #查看堂兄妹和父母，看看大家族是否会有优势
    g = pf_train.groupby(['SibSp', 'Survived'])
    #print(pd.DataFrame(g.count()['PassengerId']))

    g = pf_train.groupby(['Parch', 'Survived'])
    print(pd.DataFrame(g.count()['PassengerId']))

    #船票编号应该和结果没有什么关系，应该不用计入特征
    #cabin只有204个乘客，查看一下分布
    print(pf_train.Cabin.value_counts())
    """

    """
        这三三两两的…如此不集中…我们猜一下，也许，前面的ABCDE是指的甲板位置、然后编号是房间号？…好吧，我瞎说的，别当真…
        关键是Cabin这鬼属性，应该算作类目型的，本来缺失值就多，还如此不集中，注定是个棘手货…第一感觉，这玩意儿如果直接按照类目特征处理的话，太散了，估计每个因子化后的特征都拿不到什么权重。
        加上有那么多缺失值，要不我们先把Cabin缺失与否作为条件(虽然这部分信息缺失可能并非未登记，maybe只是丢失了而已，所以这样做未必妥当)，先在有无Cabin信息这个粗粒度上看看Survived的情况好了。
    """
    #查看有无Cabin信息下Survived的情况
    #明显可以看出有Cabin获救的比例大，可以按照有无Cabin作为特征
    """
    fig = plt.figure()
    fig.set(alpha=0.2)
    Survived_cabin = pf_train.Survived[pd.notnull(pf_train.Cabin)].value_counts()
    Survived_nocabin = pf_train.Survived[pd.isnull(pf_train.Cabin)].value_counts()
    df = pd.DataFrame({'有':Survived_cabin, '无':Survived_nocabin}).transpose()
    df.plot(kind='bar', stacked=True)
    plt.title("有无Cabin情况下获救情况")
    plt.xlabel("Cabin有无")
    plt.ylabel("人数")
    plt.show()
    """

    """
    注意：
        先从最突出的数据属性开始吧，对于Cabin和Age，有丢失数据对后一步的工作影响较大，
        对于Cabin：
            按照有无Cabin，可以将属性分为yes和no两个类型特征
        对于Age：
            对于缺失值有几种常见的处理方式
            1、如果缺值的样本占总数比例极高，可能就直接舍弃，如果作为特征加入的话，可能反而会带入noise，影响最后结果
            2、如果缺值的样本适中，该属性为非连续特征属性（比如类目属性），那么就把NaN作为一个新的类别，加入到特征中
            3、如果缺值的样本适中，如果该属性为连续属性的话，可以考虑离散化，然后把NaN作为一个类型加入到属性类目中
            4、如果缺值的数据较少，可以根据已有的数据对已有的数据进行拟合，补充缺少的值
            当前这个例子中，3和4方法都是可行的，先试一下拟合数据（由于没有比较多的背景供我们拟合，所以选择不一定好）
    """
    from sklearn.ensemble import RandomForestRegressor
    import time
    #对缺少值进行拟合
    def set_missing_ages(df):
        #把已有的数值特征取出来加入到RandomForestRegressor
        df_age = df[['Age', 'Fare', 'Parch', 'SibSp', 'Pclass']]

        #乘客分成已知和未知年龄两部分
        known_age = df_age[df_age.Age.notnull()].as_matrix()
        unknown_age = df_age[df_age.Age.isnull()].as_matrix()

        #y即为目标年龄
        y = known_age[:, 0]
        #X即为属性值
        X = known_age[:, 1:]

        #使用RandomForestRegressor进行拟合
        rfr = RandomForestRegressor(random_state=int(time.time()), n_estimators=2000, n_jobs=-1)
        rfr.fit(X, y)

        #对未知年龄进行预测
        #unknown_age[:, 1::] 取第二列开始的所有数据
        predict_ages = rfr.predict(unknown_age[:, 1::])

        #用得到的数据对之前的数据进行填充
        df.loc[(df.Age.isnull()), 'Age'] = predict_ages

        return df, rfr

    def set_cabin_type(df):
        df.loc[(df.Cabin.isnull()), 'Cabin'] = 'No'
        df.loc[(df.Cabin.notnull()), 'Cabin'] = 'Yes'
        return df

    data_train, rfr = set_missing_ages(pf_train)
    data_train = set_cabin_type(data_train)
    #print(data_train.head())

    """
    注意：
        因为逻辑回归模型中，需要输入的特征都是数值型特征，我们通常会对类目型的特征因子化/one-hot编码
        pandas的get_dummies可以处理这种情况，然后拼接在原来的data_train

    """
    dummies_Cabin = pd.get_dummies(data_train['Cabin'], prefix='Cabin')
    dummies_Embarke = pd.get_dummies(data_train['Embarked'], prefix='Embarked')
    dummies_Sex = pd.get_dummies(data_train['Sex'], prefix='Sex')
    dummies_Pclass = pd.get_dummies(data_train['Pclass'], prefix='Pclass')
    df = pd.concat([data_train, dummies_Cabin, dummies_Embarke, dummies_Sex, dummies_Pclass], axis=1)
    df.drop(['Pclass', 'Cabin', 'Embarked', 'Sex'], axis=1, inplace=True)
    #print(df.head())

    """
    注意：
        观察Age和Fare两个属性，数值幅度变化很大，如果大家了解逻辑回归和梯度下降的话，会知道，如果各属性值之间scale差距太大，
        将对收敛速度影响很大，甚至不收敛，所以我们需要进行幅度缩放，sklearn里面的preprocessing模块可以scaling，
        其实就是将一些幅度较大的特征缩放到[-1,1]之内，可以加速logistic regression的收敛
    """
    from sklearn import preprocessing
    scaler = preprocessing.StandardScaler()
    age_scaler_param = scaler.fit([df['Age']])
    df['Age_scaled'] = scaler.fit_transform(df['Age'], age_scaler_param)
    fare_scale_param = scaler.fit([df['Fare']])
    df['Fare'] = scaler.fit_transform([df['Fare']], fare_scale_param)
    print(df.head())



if __name__ == '__main__':
    train_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'train.csv')
    test_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.csv')
    titanic(train_file_name, test_file_name)
