#coding=utf-8

import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

"""
    用电预测建模前的数据特征预处理：
        比如按照地区区域对数据进行切分
        按照天气进行切分
        建立地区-天气的映射

        一个论文中记录到预测电价的特征选择：时间维度上的特征
            是否是工作日
            一年当中的第几天（代表不同的季节、节假日等）
            一个月中的第几天
            一年的第几个星期
            一天当中第几个小时
            一年当中第几个月
            前一天用电量
            前两天的用电量
            与前一天的差值

        每个特征的重要程度，然后在根据重要的特征进行组合

        需要对特征进行筛选，因为有些特征如果过拟合或者带有噪声，会影响到特征的最终表达

    对于类似电力这种连续值的预测：
        比较常使用RandomForestRegressor或者GradientBoostingRegressor

    regression算法：
        GBM(Gradient Boosting Machine) kaggle比赛中使用的
        Random Forest  kaggle比赛中使用的

        如果使用nn的deep learning的方法的话（或者使用linear模型）
        1、需要对类别型的特征做编码，
        2、需要对连续值进行幅度缩放

    基于tree的方法使用较多的有：
    1、GBRT（拟合效果非常好，容易fitting过拟合，串行）
    2、Random Forest（对过拟合控制的更好，并行）

    但是在一般的比赛中，不推荐使用sklearn的库，效率很低
    如果使用GBR模型的话，xgboost或者lightGBM性能会比较高

    gridsearchcv：
        网格候选交叉验证，会给出一批候选的超参数
        然后在训练集上5-folds， 在进行5折的交叉验证，选择最好的超参数

    数据补充：
        比如类似温度值，可以使用平均值、中位数或者knn去补充缺省值、线性内插


    建模：
        训练集和测试集合，交叉验证（完成本地评估效果， 完成超参数的选择）
        调参


    天池的电力预测：
        周一到周日的七天，需要做哑变量的变换
        每一年的第几天等都需要做哑变量（需要进行one-hot独热变量编码）

        与之前的kaggle上面不同的是，kaggle上面的数据预测后一天数据可以利用前一天数据，tianchi的预测9月份的每一天数据时不能用到前面的数据

"""

"""
    天池的预测电力的数据
"""
def func1(power_file, weather_file):
    pf = pd.read_csv(power_file)
    #print(pf.head())

    pf['record_date'] = pd.to_datetime(pf['record_date'])
    #print(pf.head())

    base_pf = pf[['record_date', 'power_consumption']].groupby(by='record_date').agg('sum')
    base_pf = base_pf.reset_index()
    #print(base_pf.head())

    pf_test = base_pf[(base_pf.record_date>='2016-08-01')&(base_pf.record_date<='2016-08-30')]
    #8月份的用电量进行平移填充
    pf_test['record_date'] = pd.DataFrame(pf_test['record_date'] + pd.Timedelta('31 days'))
    #print(pf_test.head())

    base_pf = pd.concat([base_pf, pf_test]).sort_values(['record_date'])
    base_pf['dow'] = base_pf['record_date'].apply(lambda x:x.dayofweek)
    base_pf['doy'] = base_pf['record_date'].apply(lambda x:x.dayofyear)
    base_pf['day'] = base_pf['record_date'].apply(lambda x:x.day)
    base_pf['month'] = base_pf['record_date'].apply(lambda x:x.month)
    base_pf['year'] = base_pf['record_date'].apply(lambda x:x.year)

    def map_season(month):
        month_dict = {1:1,2:1,3:2,4:2,5:3,6:3,7:3,8:3,9:3,10:4,11:4,12:1}
        return month_dict[month]
    base_pf['season'] = base_pf['month'].apply(lambda x:map_season(x))
    #print(base_pf.head())

    #求统计特征，每一个月的用电量的平均mean和方差std
    base_pf_stats = base_pf[['power_consumption','year','month']].groupby(by=['year', 'month']).agg(['mean', 'std'])
    #print(base_pf_stats.head())

    #针对上面的结果在csv中的格式 拉平对其
    base_pf_stats.columns = base_pf_stats.columns.droplevel(0)
    base_pf_stats = base_pf_stats.reset_index()
    #print(base_pf_stats.head())

    #平移 每一个预测的时候需要用到上一个月的，或者上上个月的数据
    base_pf_stats['1_m_mean'] = base_pf_stats['mean'].shift(1)
    base_pf_stats['2_m_mean'] = base_pf_stats['mean'].shift(2)  #两个月之前的平移两次
    base_pf_stats['1_m_std'] = base_pf_stats['std'].shift(1)
    base_pf_stats['2_m_std'] = base_pf_stats['std'].shift(2)
    #print(base_pf_stats.head())

    #合并
    data_pf = pd.merge(base_pf, base_pf_stats[['year','month','1_m_mean','2_m_mean','1_m_std','2_m_std']], how='inner', on=['year','month'])
    #去除2_m_mean 为空的行
    data_pf = data_pf[~pd.isnull(data_pf['2_m_mean'])]
    #print(data_pf.head())

    #notebook打开没有编码格式，使用gbk打开
    weather_file_info = pd.read_csv(weather_file, encoding='gbk')
    #print(weather_file_info.head())

    weather_file_info['record_date'] = pd.to_datetime(weather_file_info['record_date'])
    weather_file_info['day'] = weather_file_info['record_date'].apply(lambda x:x.day)
    weather_file_info['month'] = weather_file_info['record_date'].apply(lambda x:x.month)
    weather_file_info['year'] = weather_file_info['record_date'].apply(lambda x:x.year)
    #print(weather_file_info.head())

    #继续做特征 describe 会生成很多统计特征
    weather_file_max_info_month = weather_file_info[['year','month','t_max']].groupby(by=['year','month']).describe()
    weather_file_max_info_month.columns = weather_file_max_info_month.columns.droplevel(0)
    weather_file_max_info_month = weather_file_max_info_month.reset_index()
    weather_file_max_info_month.drop('count', axis=1, inplace=True)
    weather_file_max_info_month.columns = ['year','month','max_tmp_mean','max_tmp_std','max_tmp_min','max_tmp_25%','max_tmp_50%','max_tmp_75%','max_tmp_max']
    #print(weather_file_max_info_month.head())

    new_weather_file_max_info_month = weather_file_max_info_month[(weather_file_max_info_month.year==2016)&(weather_file_max_info_month.month==8)]
    new_weather_file_max_info_month['month'] = 9
    weather_file_max_info_month = pd.concat([weather_file_max_info_month, new_weather_file_max_info_month])
    #print(weather_file_max_info_month.head())

    month_1_columns = [tmp+'_1month' for tmp in ['max_tmp_mean','max_tmp_std','max_tmp_min','max_tmp_25%','max_tmp_50%','max_tmp_75%','max_tmp_max']]
    weather_file_max_info_month[month_1_columns] = weather_file_max_info_month[['max_tmp_mean','max_tmp_std','max_tmp_min','max_tmp_25%','max_tmp_50%','max_tmp_75%','max_tmp_max']]
    month_2_columns = [tmp+'_2month' for tmp in ['max_tmp_mean','max_tmp_std','max_tmp_min','max_tmp_25%','max_tmp_50%','max_tmp_75%','max_tmp_max']]
    weather_file_max_info_month[month_2_columns] = weather_file_max_info_month[['max_tmp_mean','max_tmp_std','max_tmp_min','max_tmp_25%','max_tmp_50%','max_tmp_75%','max_tmp_max']]
    print(weather_file_max_info_month.head())

    weather_file_min_info_month = weather_file_info[['year','month','t_min']].groupby(by=['year','month']).describe()
    weather_file_min_info_month.columns = weather_file_min_info_month.columns.droplevel(0)
    weather_file_min_info_month = weather_file_min_info_month.reset_index()
    weather_file_min_info_month.drop('count', axis=1, inplace=True)
    weather_file_min_info_month.columns = ['year','month','min_tmp_mean','min_tmp_std','min_tmp_min','min_tmp_25%','min_tmp_50%','min_tmp_75%','min_tmp_max']
    #print(weather_file_min_info_month.head())

    new_weather_file_min_info_month = weather_file_min_info_month[(weather_file_min_info_month.year==2016)&(weather_file_min_info_month.month==8)]
    new_weather_file_min_info_month['month'] = 9
    weather_file_min_info_month = pd.concat([weather_file_min_info_month, new_weather_file_min_info_month])
    month_1_columns = [tmp+'_1month' for tmp in ['min_tmp_mean','min_tmp_std','min_tmp_min','min_tmp_25%','min_tmp_50%','min_tmp_75%','min_tmp_max']]
    weather_file_min_info_month[month_1_columns] = weather_file_min_info_month[['min_tmp_mean','min_tmp_std','min_tmp_min','min_tmp_25%','min_tmp_50%','min_tmp_75%','min_tmp_max']]
    month_2_columns = [tmp+'_2month' for tmp in ['min_tmp_mean','min_tmp_std','min_tmp_min','min_tmp_25%','min_tmp_50%','min_tmp_75%','min_tmp_max']]
    weather_file_min_info_month[month_2_columns] = weather_file_min_info_month[['min_tmp_mean','min_tmp_std','min_tmp_min','min_tmp_25%','min_tmp_50%','min_tmp_75%','min_tmp_max']]
    #print(weather_file_min_info_month.head())

    #print('----------------------------')
    #weather_file_info = pd.concat([weather_file_min_info_month[['year','month']], weather_file_max_info_month.loc[:,'max_tmp_mean_1month']])
    weather_file_info = pd.concat([weather_file_min_info_month[['year','month']], weather_file_max_info_month])
    print(weather_file_info.head())
    #weather_file_info = weather_file_info[pd.notnull(weather_file_info.min_tmp_mean_2month)]
    #print(weather_file_info.head())

    final_train_data = final_df[~((final_df.year==2016)&(final_df.month==9))].drop('power_consumption', 1)
    final_test_data = final_df[((final_df.year==2016)&(final_df.month==9))].drop('power_consumption', 1)
    train_target = final_df[~((final_df.year==2016)&(final_df.month==9))][['power_consumption']]

    train_lgb = final_train_data.copy()
    train_lgb[['dow','doy','day','month','year','season']] = train_lgb[['dow','doy','day','month','year','season']].astype(str)
    test_lgb = final_test_data.coopy()
    test_lgb[['dow','doy','day','month','year','season']] = test_lgb[['dow','doy','day','month','year','season']].astype(str)
    final_df.to_csv('result.csv', index=False)
    X_lgb = train_lgb.values
    y_lgb = train_target.values.reshape(train_target.values.shape[0],)


    #使用的是lightgbm
    from lightgbm import LGBMRegressor
    from sklearn.metrics import mean_squared_error
    from sklearn.model_selection import GridSearchCV
    estimator = LGBMRegressor(colsample_bytree=0.8, subsample=0.9, subsample_freq=5)
    pagram_grid = {
            'learning_rate':[0.01,0.02,0.05,0.1],
            'n_estimators':[1000,2000,3000,4000,5000], #树的数量
            'num_leaves':[128,1024] #树的深度 7,10
        }
    fit_params = {'categorical_feature':[0,1,2,3,4,5]}
    #网格搜索教程验证
    gbm = GridSearchCV(estimator, param_grid, fit_params=fit_params, n_jobs=5, refit=True)
    gbm.fit(X_lgb, y_lgb)
    print('-------------results------------')
    print(gbm.cv_results_)
    print('best parameters found by grid search are:', gbm.best_params_)

if __name__ == '__main__':
    """
    """
    power_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Tianchi_power.csv')
    weather_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'weather.csv')
    func1(power_file_name, weather_file_name)
