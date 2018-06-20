#coding=utf-8

import os
import pandas as pd
import numpy as np
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
    #print(data_train)

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
    df.drop(['Pclass', 'Name', 'Ticket', 'Cabin', 'Embarked', 'Sex'], axis=1, inplace=True)
    #print(df.head())

    """
    注意：
        观察Age和Fare两个属性，数值幅度变化很大，如果大家了解逻辑回归和梯度下降的话，会知道，如果各属性值之间scale差距太大，
        将对收敛速度影响很大，甚至不收敛，所以我们需要进行幅度缩放，sklearn里面的preprocessing模块可以scaling，
        其实就是将一些幅度较大的特征缩放到[-1,1]之内，可以加速logistic regression的收敛
    """

    from sklearn import preprocessing
    scaler = preprocessing.StandardScaler()
    age_scale_param = scaler.fit(df['Age'].values.reshape(-1, 1))
    df['Age_scaled'] = scaler.fit_transform(df['Age'].values.reshape(-1, 1), age_scale_param)
    #df['Age_scaled'] = scaler.fit_transform(df['Age'].values.reshape(-1, 1))

    fare_scale_param = scaler.fit(df['Fare'].values.reshape(-1, 1))
    df['Fare_scaled'] = scaler.fit_transform(df['Fare'].values.reshape(-1, 1), fare_scale_param)
    #df['Fare_scaled'] = scaler.fit_transform(df['Fare'].values.reshape(-1, 1))
    #print(df.head())


    """
        需要把feature字段取出来，转成numpy格式，然后使用logisticRegression建模
    """
    from sklearn.linear_model import LogisticRegression
    train_df = df.filter(regex='Survived|Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    train_np = train_df.as_matrix()
    #y 即为Survived结果
    y = train_np[:, 0]
    #X 即为特征属性
    X = train_np[:, 1:]
    print(len(X), len(y))
    #fit到模型中
    clf = LogisticRegression(C=1.0, penalty='l1', tol=1e-6)
    clf.fit(X, y)
    print(X.shape)


    """
        对测试集做相同的转换
    """
    pf_test = pd.read_csv(test_file)
    pf_test.loc[(pf_test.Fare.isnull()), 'Fare'] = 0

    tmp_pf_test = pf_test[['Age', 'Fare', 'Parch', 'SibSp', 'Pclass']]
    null_age = tmp_pf_test[pf_test.Age.isnull()].as_matrix()
    #填补空白数据
    X_predict = null_age[:, 1:]
    predict_test_ages = rfr.predict(X_predict)
    pf_test.loc[(pf_test.Age.isnull()), 'Age'] = predict_test_ages

    pf_test = set_cabin_type(pf_test)
    dummies_Cabin = pd.get_dummies(pf_test['Cabin'], prefix='Cabin')
    dummies_Embarke = pd.get_dummies(pf_test['Embarked'], prefix='Embarked')
    dummies_Sex = pd.get_dummies(pf_test['Sex'], prefix='Sex')
    dummies_Pclass = pd.get_dummies(pf_test['Pclass'], prefix='Pclass')

    pf_test = pd.concat([pf_test, dummies_Cabin, dummies_Embarke, dummies_Sex, dummies_Pclass], axis=1)
    pf_test.drop(['Pclass', 'Name', 'Sex', 'Ticket', 'Cabin', 'Embarked'], axis=1, inplace=True)
    pf_test['Age_scaled'] = scaler.fit_transform(pf_test['Age'].values.reshape(-1, 1), age_scale_param)
    pf_test['Fare_scaled'] = scaler.fit_transform(pf_test['Fare'].values.reshape(-1, 1), fare_scale_param)

    pf_test_features = pf_test.filter(regex='Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    pf_test_matrix = pf_test_features.as_matrix()
    predictions = clf.predict(pf_test_matrix)
    result = pd.DataFrame({'PassengerId':pf_test['PassengerId'].as_matrix(), 'Survived':predictions.astype(np.int32)})

    result_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logistic_regression_predictions.csv')
    result.to_csv(result_file, index=False)

    predictions_file = pd.read_csv(result_file)
    print(predictions_file.head())

    """
        预测之后需要判断模型所处状态（欠拟合或过拟合）
            如果测试集合上，表现不佳，则可能欠拟合，也可能过拟合
        对过拟合和欠拟合处理：
            过拟合：
                1、做一个feature selection，挑出较好的feature的subset来做training
                2、提供更多的数据，弥补原始数据的bias问题，学习到的model会更加准确
            欠拟合：
                1、需要更多的feature
                2、需要更复杂的模型来提高准确度
        learning curve 可以帮我们判定模型所处的状态
            样本数为横坐标
            训练和交叉验证集上的错误率为纵坐标
            可以把错误率替换成准确率（得分），得到另一种形式的learning curve（sklearn里面是这么做的）
    """
    #Deprecated since version 0.18: This module will be removed in 0.20.
    #from sklearn.learning_curve import learning_curve
    from sklearn.model_selection import learning_curve
    #用sklearn的learning_curve得到training_score和cv_score
    def plot_learn_curve(estimator, title, X, y, ylim=None, cv=None, n_jobs=1, train_sizes=np.linspace(0.05, 1.0, 20), verbose=0, plot=True):
        """
            画出data在模型上的learning curve
        参数详解：
            estimator：分类器
            title：表格标题
            X：输入的feature，numpy类型
            y：输入的target vector
            ylim：tuple格式的(ymin,ymax)，设定图像中纵坐标最低点和最高点
            cv：做cross-validation的时候，数据分成的份数，其中一份作为cv集，其余n-1份作为训练集
            n-jobs：并行的任务数
        """
        train_sizes, train_scores, test_scores = learning_curve(estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes, verbose=verbose)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)

        if plot:
            plt.figure()
            plt.title(title)
            if ylim is not None:
                plt.ylim(*ylim)
            plt.xlabel('训练样本数')
            plt.ylabel('得分')
            plt.gca().invert_yaxis()
            plt.grid()

            plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1, color='b')
            plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.1, color='r')

            plt.plot(train_sizes, train_scores_mean, 'o-', color='b', label='训练集上得分')
            plt.plot(train_sizes, test_scores_mean, 'o-', color='r', label='交叉验证集上得分')

            plt.legend(loc='best')
            plt.draw()
            plt.gca().invert_yaxis()
            plt.show()
        mid_point = ((train_scores_mean[-1] + train_scores_std[-1]) + (test_scores_mean[-1] - test_scores_std[-1])) / 2
        diff = (train_scores_mean[-1] + train_scores_std[-1]) - (test_scores_mean[-1] - test_scores_std[-1])
        return mid_point, diff

    """
    结论：
        从曲线看，我们的model，并不处于overfitting的状态(overfitting的表现是训练集上得分高，交叉验证集上很低，中间的的gap比较大)
        因此我们可以做些feature engineering的工作，产生出一些新的特征或者组合特征到模型中

        优化baseline系统：
            1、比如说Name和Ticket两个属性被我们完整舍弃了
            2、比如年龄的拟合未必靠谱
            3、按照日常的经验，老人和小孩儿可能得到的照顾会多一些，那么，年龄作为一个连续值，给一个固定系数，体现不出受照顾的实际情况，
              因此，我们把年龄离散化，按区段分类别属性会更合适一些

            怎么才能知道哪些属性可以继续深挖的呢？？？？
                做交叉验证！！！！！！！！

            查看模型中各个参数的相关系数：
                pd.DataFrame({"columns":list(train_df.columns)[1:], "coef":list(clf.coef_.T)})

    """
    plot_learn_curve(clf, '学习曲线', X, y, plot=False)

    """
        查看模型的系数，因为系数和它们最终的判定能力强弱是正相关的
        模型系数分析：
                    	   coef	       columns
                0	[-0.344189431858]	SibSp
                1	[-0.104924350555]	Parch
                2	[0.0]	            Cabin_No
                3	[0.902071479485]	Cabin_Yes
                4	[0.0]	            Embarked_C
                5	[0.0]	            Embarked_Q
                6	[-0.417226462259]	Embarked_S
                7	[1.95649520339]	    Sex_female
                8	[-0.677484871046]	Sex_male
                9	[0.341226064445]	Pclass_1
                10	[0.0]	            Pclass_2
                11	[-1.19410912948]	Pclass_3
                12	[-0.523774279397]	Age_scaled
                13	[0.0844279740271]	Fare_scaled
            Sex属性：如果是female会极大提高最后的获救概率，而male会很大程度拉低这个概率
            Pclass属性：1等仓获救的概率比较大，3等仓会极大拉低获救概率
            Cabin属性：有Cabin会提高获救概率（事实上，最开始的记录里面有无Cabin记录的Survived的，即使有Cabin的乘客，也有一部分遇难了，估计这个属性挖掘不够）
            Age属性：age是一个负相关属性，意味着年龄越小，越有获救的优先权（感觉有点不合理）
            S登港口：极大的会拉低获救的概率，另外两个几乎没啥作用（这个与实际感觉有点不符，因为之前的统计没有这个明显的特征，这个特征可能有问题，可以考虑删除）
            船票Fare：有小幅度的正相关（不是说这个特征作用不大，可能是我们细化的不够，比如可以离散化，在分到各个乘客等级上？）
    """
    res = pd.DataFrame({'columns':list(train_df.columns)[1:], 'coef':list(clf.coef_.T)})
    #print(res)

    #from sklearn.cross_validation import train_test_split, cross_val_score
    from sklearn.model_selection import cross_validate, cross_val_score, train_test_split

    #先看一下打分情况
    clf = LogisticRegression(C=1.0, penalty='l1', tol=1e-6)
    cross_train_data = df.filter(regex='Survived|Age_.*|SibSp|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    X = cross_train_data.as_matrix()[:, 1::]
    y = cross_train_data.as_matrix()[:, 0]
    cross_res = cross_val_score(clf, X, y, cv=5)
    #print(cross_res)

    #分割数据
    split_train,split_cv,y_train,y_cv = train_test_split(X, y, test_size=0.3, random_state=int(time.time()))
    #cross_train_data = split_train.filter(regex='Survived|Age_.*|SibSp|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    #生成模型
    clf = LogisticRegression(C=1.0, penalty='l1', tol=1e-6)
    clf.fit(split_train, y_train)

    #对cross validation数据进行预测
    #cv_df = split_cv.filter(regex='Survived|Age_.*|SibSp|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*')
    predictions = clf.predict(split_cv)

    #bad_class = pf_train.loc[pf_train['PassengerId'].isin(split_cv[predictions!=y_cv]['PassengerId'].values)]
    #bad_class = split_cv[predictions!=y_cv]
    #print(bad_class)
    """
        找出预测错误的case，分析数据
        去除预测错误的case 看原始dataframe数据  进行对比
        	PassengerId	Survived	Pclass	Name	Sex	Age	SibSp	Parch	Ticket	Fare	Cabin	Embarked
            15	0	3	Vestrom, Miss. Hulda Amanda Adolfina	female	14.00	0	0	350406	7.8542	NaN	S
            50	0	3	Arnold-Franchi, Mrs. Josef (Josefine Franchi)	female	18.00	1	0	349237	17.8000	NaN	S
            56	1	1	Woolner, Mr. Hugh	male	NaN	0	0	19947	35.5000	C52	S
            66	1	3	Moubarek, Master. Gerios	male	NaN	1	1	2661	15.2458	NaN	C
            69	1	3	Andersson, Miss. Erna Alexandra	female	17.00	4	2	3101281	7.9250	NaN	S
            86	1	3	Backstrom, Mrs. Karl Alfred (Maria Mathilda Gu...	female	33.00	3	0	3101278	15.8500	NaN	S
            114	0	3	Jussila, Miss. Katriina	female	20.00	1	0	4136	9.8250	NaN	S
        分析：
            Age属性：Age属性不使用现在的拟合方式，而是根据[Mr] [Mrs] [Miss]等平均值进行填充
                    Age不做成一个连续属性，而是使用一个步长进行离散化
            Age细化：增加一个child字段，age<=12，设为1，其余为0（观察数据发现小朋友的优先程度太高）
            Cabin属性：对于有记录的Cabin属性，将其分为前面的字母部分（可能是位置和船层之类的信息）和后面的数字（可能是房间号，观测数据发现，好像后面的数字越大获救概率越大）
            Pclass和Sex属性太重要了，可以尝试用他们组成一个组合属性，这也是另外一种程度的优化
            如果名字里面有Mrs字段，而Parch>1的，可能是一个母亲，应该获救的概率会很高，因此可以多加一个Mother字段，符合条件为1，其余为0
            登船港口：可以先考虑去掉（Q和C没有权值，S权重异常，所以不好判断到底哪个有关系或者是噪声）
            把堂兄/堂妹和Parch还有自己个数加在一起组成一个Family_size字段，考虑大家族对最后结果的影响
            Name属性：可以做一些简单的处理，比如名字中有带某些字眼('Capt', 'Don','Major','Sir')可以统一到一个title
            其余还有很多可以挖掘的数据
    """
    name_data_train = pf_train[pf_train['Name'].str.contains('Major')]
    #print(name_data_train)

    #合并sex 和 Pclass，增加一个字段
    pf_train['Sex_Pclass'] = data_train.Sex + '_' + data_train.Pclass.map(str)

    """
        优化特征后，在进行一次数据处理和预测，查看最后预测的分数

    注意：
        一般做到后期，需要进行模型优化的方法就是模型融合
        大概意思：比如分类问题，当我们手头上有一堆在同一份数据集上训练得到的分类器（比如logistic regression，SVM，KNN，random forest，神经网络）,
            我们让他们分别去做判定，然后对结果做投票统计，票数最多的结果为最后结果

        特点：模型融合可以比较好地缓解训练过程中产生的过拟合问题，从而提升结果的准确度

        分析：我们现在只用了logistic regression，如果我们想利用融合思想提高我们的模型，该如何操作？
            如果模型没得选，那只有在数据上动手脚。如果模型出现过拟合现象，一定是在我们的训练上出现拟合过度造成的。
            数据切分，我们没有任何一份数据集是全的，即使出现过拟合，也是在子训练集上过拟合，而不是在全体数据集，可能最最后结果有帮助
            这就是常用的Bagging
    """
    from sklearn.ensemble import BaggingRegressor
    bagging_train_data = df.filter(regex='Survived|Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass.*|Mother|Child|Family|Title')
    bagging_train_np = bagging_train_data.as_matrix()

    #y为survived结果
    bagging_y = bagging_train_np[:, 0]
    #X为特征属性
    bagging_X = bagging_train_np[:, 1::]

    #fit 到BaggingRegression中
    b_clf = LogisticRegression(C=1.0, penalty='l1', tol=1e-6)
    bagging_clf = BaggingRegressor(b_clf, n_estimators=10, max_samples=0.8, max_features=1.0, bootstrap=True, bootstrap_features=False, n_jobs=-1)
    bagging_clf.fit(bagging_X, bagging_y)

    bagging_test = pf_test.filter(regex='Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass.*|Mother|Child|Family|Title')
    bagging_predictions = bagging_clf.predict(bagging_test)
    bagging_result = pd.DataFrame({'PassengerId':pf_test['PassengerId'].as_matrix(), 'Survived':bagging_predictions.astype(np.int32)})
    bagging_result_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bagging_result.csv')
    bagging_result.to_csv(bagging_result_file, index=False)
    print(bagging_result.head())

    # 使用一下其他的分类器
    from pandas import DataFrame
    from patsy import dmatrices
    from operator import itemgetter
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score, train_test_split, StratifiedShuffleSplit, StratifiedKFold
    from sklearn.pipeline import Pipeline
    #from sklearn.grid_search import GridSearchCV
    from sklearn.model_selection import GridSearchCV
    from sklearn import preprocessing
    from sklearn.metrics import classification_report
    from sklearn.externals import joblib
    import string
    import json

    #输出得分
    def report(grid_score, n_top=3):
        top_scores = sorted(grid_score, key=itemgetter(1), reverse=True)[:n_top]
        for i,score in enumerate(top_scores):
            print('Model with rank:{0}'.format(i+1))
            print('Mean validation score: {0:.3f} (std: {1:.3f})'.format(score.mean_validation_score, np.std(score.cv_validation_score)))
            print('Parameters: {0}'.format(score.parameters))

    #清理和处理
    def substrings_in_string(big_string, substrings):
        for subs in substrings:
            if big_string.find(subs) != -1:
            #if string.find(big_string, subs) != -1:
                return subs
        print(big_string)
        return np.nan

    #处理缺失值
    def clean_and_munge_data(df):
        df.Fare = df.Fare.map(lambda x:np.nan if x==0 else x)
        #处理名字 生成Title字段
        title_list = ['Mrs', 'Mr', 'Master', 'Miss', 'Major', 'Rev','Dr', 'Ms', 'Mlle','Col', 'Capt', 'Mme', 'Countess','Don', 'Jonkheer']

        df['Title'] = df['Name'].map(lambda x: substrings_in_string(x, title_list))

        #处理特殊的称呼，全处理成mr,mrs,miss,master
        def replace_titles(x):
            title = x['Title']
            if title in ['Mr','Don', 'Major', 'Capt', 'Jonkheer', 'Rev', 'Col']:
                return 'Mr'
            elif title in ['Master']:
                return 'Master'
            elif title in ['Countess', 'Mme','Mrs']:
                return 'Mrs'
            elif title in ['Mlle', 'Ms','Miss']:
                return 'Miss'
            elif title =='Dr':
                if x['Sex']=='Male':
                    return 'Mr'
                else:
                    return 'Mrs'
            elif title =='':
                if x['Sex']=='Male':
                    return 'Master'
                else:
                    return 'Miss'
            else:
                return title

        df['Title'] = df.apply(replace_titles, axis=1)

        #查看家族是否够大
        df['Family_size'] = df['SibSp'] + df['Parch']
        df['Family'] = df['SibSp'] * df['Parch']

        df.loc[(df.Fare.isnull())&(df.Pclass==1), 'Fare'] = np.median(df[df['Pclass']==1]['Fare'].dropna())
        df.loc[(df.Fare.isnull())&(df.Pclass==2), 'Fare'] = np.median(df[df['Pclass']==2]['Fare'].dropna())
        df.loc[(df.Fare.isnull())&(df.Pclass==3), 'Fare'] = np.median(df[df['Pclass']==3]['Fare'].dropna())

        #df = df[['Sex','Age']].dropna()
        #df['Sex'].fillna('male').astype(str)
        df['Gender'] = df['Sex'].map({'female':0, 'male':1}).astype(np.int32)
        df['AgeFill'] = df['Age']

        mean_ages = np.zeros(4)
        mean_ages[0] = np.average(df[df['Title']=='Miss']['Age'].dropna())
        mean_ages[1] = np.average(df[df['Title']=='Mrs']['Age'].dropna())
        mean_ages[2] = np.average(df[df['Title']=='Mr']['Age'].dropna())
        mean_ages[3] = np.average(df[df['Title']=='Master']['Age'].dropna())

        df.loc[(df.Age.isnull())&(df.Title=='Miss'), 'AgeFill'] = mean_ages[0]
        df.loc[(df.Age.isnull())&(df.Title=='Mrs'), 'AgeFill'] = mean_ages[1]
        df.loc[(df.Age.isnull())&(df.Title=='Mr'), 'AgeFill'] = mean_ages[2]
        df.loc[(df.Age.isnull())&(df.Title=='Master'), 'AgeFill'] = mean_ages[3]

        df['AgeCat'] = df['AgeFill']
        df.loc[(df.AgeFill<=10), 'AgeCat'] = 'child'
        df.loc[(df.AgeFill>=60), 'AgeCat'] = 'aged'
        df.loc[((df.AgeFill>10) & (df.AgeFill<=30)), 'AgeCat'] = 'adult'
        df.loc[(df.AgeFill>30)&(df.AgeFill<60), 'AgeCat'] = 'senior'

        df.Embarked = df.Embarked.fillna('S')
        df.loc[df.Cabin.isnull()==True, 'Cabin'] = 0.5
        df.loc[df.Cabin.isnull()==False, 'Cabin'] = 1.5
        df['Fare_Per_Person'] = df['Fare']/(df['Family_size']+1)

        #age times class
        df['AgeClass'] = df['AgeFill']*df['Pclass']
        df['ClassFare'] = df['Pclass']*df['Fare_Per_Person']

        df['HighLow'] = df['Pclass']
        df.loc[(df.Fare_Per_Person<8), 'HighLow'] = 'Low'
        df.loc[(df.Fare_Per_Person>=8), 'HighLow'] = 'High'

        p_label_encode = preprocessing.LabelEncoder()
        p_onehot_encode = preprocessing.OneHotEncoder()
        p_label_encode.fit(df['Sex'])
        x_sex = p_label_encode.transform(df['Sex'])
        df['Sex'] = x_sex.astype(np.float)

        p_label_encode.fit(df['Ticket'])
        x_ticket = p_label_encode.transform(df['Ticket'])
        df['Ticket'] = x_ticket.astype(np.float)

        p_label_encode.fit(df['Title'])
        x_title = p_label_encode.transform(df['Title'])
        df['Title'] = x_title.astype(np.float)

        p_label_encode.fit(df['HighLow'])
        x_hl = p_label_encode.transform(df['HighLow'])
        df['HighLow'] = x_hl.astype(np.float)

        #p_label_encode.fit(df['AgeCat'])
        #x_age = p_label_encode.transform(df['AgeCat'])
        x_age = p_label_encode.fit_transform(df['AgeCat'])
        df['AgeCat'] = x_age.astype(np.float)

        x_emb = p_label_encode.fit_transform(df['Embarked'])
        df['Embarked'] = x_emb.astype(np.float)

        df = df.drop(['PassengerId', 'Name', 'Age', 'Cabin'], axis=1)

        return df

    df = clean_and_munge_data(pf_train)
    # formula
    formula_ml='Survived~Pclass+C(Title)+Sex+C(AgeCat)+Fare_Per_Person+Fare+Family_size'
    y_train,x_train = dmatrices(formula_ml, data=pf_train, return_type='dataframe')
    y_train = np.asarray(y_train).ravel()
    print(y_train.shape, x_train.shape)

    #分割测试和训练集
    X_train,X_test,Y_train,Y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=int(time.time()))
    #初始化分类器
    forest_clf = RandomForestClassifier(n_estimators=500, criterion="entropy", max_depth=5, min_samples_split=2, min_samples_leaf=1,
                        max_features="auto", bootstrap=False, oob_score=False, n_jobs=1, random_state=int(time.time()), verbose=0)

    ### grid search 找到最好的参数
    # 可以从 print('estimator.get_params().keys() ', forest_clf.get_params().keys()) 获取需要哪些参数
    param_grid = {
            'clf__n_estimators':[1000,2000,3000,4000,5000],
            'clf__max_depth':[5,6,7,8,9,10]
        }
    pipeline = Pipeline([('clf', forest_clf)])
    # 参考 https://stackoverflow.com/questions/34889110/random-forest-with-gridsearchcv-error-on-param-grid
    # print('pipeline.get_params().keys() ', pipeline.get_params().keys()) 获取param_grid的参数
    strati_cv = StratifiedShuffleSplit(n_splits=10, test_size=0.2, train_size=None, random_state=int(time.time()))
    grid_search = GridSearchCV(pipeline, param_grid=param_grid, verbose=3, scoring='accuracy', cv=strati_cv).fit(X_train, Y_train)
    #对结果打分
    print('Best score: {0:.3f}'.format(grid_search.best_score_))
    print('Best estimator: {0}'.format(grid_search.best_estimator_))
    print('Best grid score: {0}'.format(grid_search.grid_scores_))

    print('----- grid search end ---------')
    print('on all train set')
    scores = cross_val_score(grid_search.best_estimator_, x_train, y_train, cv=3, scoring='accuracy')
    print(scores.mean(), scores)
    print('on test set')
    scores = cross_val_score(grid_search.best_estimator_, X_test, Y_test, cv=3, scoring='accuracy')
    print(scores.mean(), scores)

    #对结果打分
    res = classification_report(Y_train, grid_search.best_estimator_.predict(X_train))
    print(res)
    print('test data')
    res = classification_report(X_test, grid_search.best_estimator_.predict(X_test))
    print(res)

    model_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'model_rf.pkl')
    joblib.dump(grid_search.best_estimator_, model_file)



if __name__ == '__main__':
    train_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'train.csv')
    test_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.csv')
    titanic(train_file_name, test_file_name)













#
