#coding=utf-8

import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from matplotlib.ticker import FuncFormatter
from matplotlib.font_manager import FontProperties
"""
    matp_statistic_20190413.zip
"""


config_excel_path = "D:\opensource\scrapy-work\wolf_outer\matp_statistic"
#config_excel_path = "C:\\Users\\jiexu\\Desktop\\matp_statistic_20190413"

write_contents_main = """
建议设置：
    根据数量统计结果找出中间值 ，其他数据逐次与中间值对比，高于中间值的项目纳入建议【1】；低于中间值的项目纳入建议【2】，根据建议分类补全预测信息。

（）系统名/车号  ---占比和  ==数量

   主系统故障/ 子系统故障 ：
建议【1】主系统中（{0}）故障率较高，约占总故障的{1}。子系统中（{2}）出现故障较多，约占总故障的{3}。请新造设计师分析（{4}）故障率高的原因，及时处理故障。
预测：主系统（{5}）将在未来仍保持较高的故障率，请检修方加大关注力度，提高检查次数，重点关注（{6}）等子系统可能出现的问题与潜在风险，避免不必要的事故发生。（{7}）等主系统故障次数少，可适当减少检查次数，延长检查间隔期，避免人力物力资源浪费。

"""
write_contents_have_no_error =  """
   主系统平均无故障时间 ：
建议【1】（{0}）平均无故障时间较短，小于({1})天，请加大检查力度。
建议【2】（{2}）平均无故障时间较长，大于({3})天。可以减少检查次数。
预测：（{4}）的长时间无故障情况将会一直保持下去，可适当延长检查间隔，节约资源。同时可适当增加（{5}）的检查次数，减少事故隐患。

"""
write_contents_repair = """
   主系统故障平均维修：
建议【1】（{0}）平均维修时间最长，为{1}小时。有{2}起故障维修时间达到4个小时以上。请新造检修负责人分析故障维修时间达到4小时以上的故障原因。
建议【2】（{3}）平均维修时间最短，为{4}小时。
预测：（{5}）作为维修时间最长的系统，同时它也是故障率最高的系统之一，请检修负责人加大检修力度，发现问题及时处理，避免不必要的损失，同时也请重点分析系统的不足及潜在的安全隐患，争取减少故障率，提高安全性，节约人力物力。

"""
write_contents_main_handle = """
   主系统故障处理方式：
运营期间发生的共({0})件故障，共有四类处理方式，分别为，现场处理{1}件，备件更换{2}件，待处理{3}件，其他{4}件。
（{5}）仅发生({6})起故障均只采用了现场处理方式。【1】（{7}）采取现场处理方式较多，分别占其总故障数的{8}。（{9}）采取备件更换的方式较多，分别占其总故障数的{10}。
预测：（{11}）多采取现场处理方式的情况取决于其自身系统的构成和故障程度，在未来一段时间内将长期保持这样的情况，请现场检修人员重点检查这些系统，减轻整体工作量，减少安全隐患。

"""
write_contents_errors = """
    车辆故障：
建议【1】（{0}）故障率较高，约占总故障率的{1}.请售后现场重点关注故障率排名靠前的（{2}），请新造设计分析其故障产生的原因。
预测：（{3}）的高故障率可能与其自身结构和系统设计有关，这需要大量检查工作，因此在未来的一段时间内该型号车辆都不会有所变化，故障率会一直保持较高的水平，请检修人员加大检查力度，缩短对该车的检查间隔，增加检查项目，减少隐患。

"""
write_contents_have_no_error_time = """
     车辆平均无故障时间：
建议【2】（{0}）车平均无故障时间较短，为({1})天。
建议【1】（{2}）车平均无故障时间较长，为({3})天。请缩短检查间隔
预测：各型号车辆平均无故障时间都比较长，根据车辆的整体设计和检验标准，可判断该情况会保持很长一段时间。检修人员可适当延长所有车辆的检修间隔，将更多注意力放在故障多发的项目上。
"""


def get_excel_files():
    all_excel_files = []
    for i in os.listdir(config_excel_path):
        full_path = os.path.join(config_excel_path, i)
        if os.path.isfile(full_path) and full_path.endswith(".xlsx"):
            all_excel_files.append(full_path)
    return all_excel_files


def full_save_fig_path(file_name):
    path_parent = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pig")
    if not os.path.exists(path_parent):
        os.makedirs(path_parent)
    return os.path.join(path_parent, file_name)

def writer_analysis_results(contents="", result_file="analysis_results.txt", is_rewrite=False):
    file_name = full_save_fig_path(result_file)
    if is_rewrite:
        with open(file_name, "wb") as f:
            pass
    else:
        with open(file_name, "ab") as f:
            f.write((contents.encode("utf-8")))

def statistic_excel():
    writer_analysis_results(is_rewrite=True)
    all_files = get_excel_files()
    error_main = None
    errors_union = None
    error_big_sub_class = None
    error_main_no_err_time = None
    error_main_repair_time = None
    error_main_repair_type = None
    car_err_num = None
    car_no_err_day = None
    save_pig_dpi = 200

    for i in all_files:
        df = pd.read_excel(i)
        error_main_tmp = df["故障所属主系统"]
        errors_union_tmp = pd.concat((df["故障所属主系统"], df["故障处理方式"]), axis=1)
        error_big_sub_class_tmp = pd.concat((df["故障所属主系统"], df["故障所属子系统"]), axis=1)
        error_main_no_err_time_tmp = pd.concat((df["故障所属主系统"], df["系统平均无故障时间（天）"]), axis=1)
        error_main_repair_time_tmp = pd.concat((df["故障所属主系统"], df["故障平均维修时间（时）"]), axis=1)
        error_main_repair_type_tmp = pd.concat((df["故障所属主系统"], df["故障处理方式"]), axis=1)
        car_err_num_tmp = pd.concat((df["列车号"], df["故障所属主系统"]), axis=1)
        car_no_err_day_tmp = pd.concat((df["列车号"], df["系统平均无故障时间（天）"]), axis=1)


        if error_main is None:
            error_main = error_main_tmp
            errors_union = errors_union_tmp
            error_big_sub_class = error_big_sub_class_tmp
            error_main_no_err_time = error_main_no_err_time_tmp
            error_main_repair_time = error_main_repair_time_tmp
            error_main_repair_type = error_main_repair_type_tmp
            car_err_num = car_err_num_tmp
            car_no_err_day = car_no_err_day_tmp
        else:
            error_main = pd.concat((error_main, error_main_tmp), axis=0)
            errors_union = pd.concat((errors_union, errors_union_tmp), axis=0)
            error_big_sub_class = pd.concat((error_big_sub_class, error_big_sub_class_tmp), axis=0)
            error_main_no_err_time = pd.concat((error_main_no_err_time, error_main_no_err_time_tmp), axis=0)
            error_main_repair_time = pd.concat((error_main_repair_time, error_main_repair_time_tmp), axis=0)
            error_main_repair_type = pd.concat((error_main_repair_type, error_main_repair_type_tmp), axis=0)
            car_err_num = pd.concat((car_err_num, car_err_num_tmp), axis=0)
            car_no_err_day = pd.concat((car_no_err_day, car_no_err_day_tmp), axis=0)

    writer = pd.ExcelWriter(full_save_fig_path("统计表.xlsx"))

    # 各主系统故障数（统计表），各主系统故障占比
    if error_main is not None:
        fig = plt.figure()
        ax1 = plt.gca()
        error_main_results = error_main.value_counts()
        x_labels = error_main_results.index.tolist()
        y_values = error_main_results.tolist()
        y_values_median = np.median(y_values)
        y_values_sum = sum(y_values)
        params_0 = x_labels[0]
        params_1 = round((y_values[0] * 100.0) / y_values_sum, 0)
        params_1 = "{0}%".format(params_1)
        params_5 = "{0}".format(x_labels[0])
        params_7 = "{0}".format(x_labels[-1])

        x_index = list(range(len(x_labels)))
        ax1.bar(x_index, y_values)
        plt.title("各系统故障数统计图", fontsize=20)
        new_x_labels = [i[:-2] if i.endswith("系统") else i for i in x_labels]
        plt.xticks(x_index, new_x_labels, rotation=30)
        plt.grid(axis='y')
        savefig(full_save_fig_path("各主系统故障数-统计表.jpg"), format='jpg', dpi=save_pig_dpi)

        to_write_df = pd.DataFrame({"主系统":x_labels,"故障数":y_values})
        to_write_df.to_excel(writer, index=False, sheet_name='主系统统计表')

        fig = plt.figure()
        ax1 = plt.gca()
        list_sum = np.sum(y_values)
        new_y_values = [int(round(i/list_sum*100, 0)) for i in y_values]
        x_index = list(range(len(x_labels)))
        ax1.bar(x_index, new_y_values)
        plt.title("各主系统故障占比统计图", fontsize=20)
        new_x_labels = [i[:-2] if i.endswith("系统") else i for i in x_labels]
        plt.xticks(x_index, new_x_labels, rotation=30)
        def to_percent(temp, position):
            return '%1.0f'%(temp) + '%'
        ax1.yaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.grid(axis='y')
        savefig(full_save_fig_path("各主系统故障占比-统计表.jpg"), format='jpg', dpi=save_pig_dpi)

    # 各子系统故障数（统计表），各子系统故障占比
    if error_big_sub_class is not None:
        fig = plt.figure()
        ax1 = plt.gca()
        error_big_sub_class_results = error_big_sub_class["故障所属子系统"].value_counts()
        x_labels = error_big_sub_class_results.index.tolist()
        y_values = error_big_sub_class_results.tolist()
        y_values_sum = sum(y_values)
        params_2 = x_labels[0]
        params_3 = round((y_values[0] * 100.0)/y_values_sum, 0)
        params_3 = "{0}%".format(params_3)
        params_4 = "{0}、{1}".format(x_labels[0],x_labels[1])
        params_6 = "{0}".format(x_labels[0])
        x_index = list(range(len(y_values)))
        ax1.bar(x_index, y_values)
        plt.title("运营期间系统各子系统故障数", fontsize=20)
        plt.xticks(x_index, x_labels, rotation=10, fontsize=4)
        plt.grid(axis='y')
        savefig(full_save_fig_path("各子系统故障数.jpg"), format='jpg', dpi=save_pig_dpi)

        to_write_df = pd.DataFrame({"子系统":x_labels,"故障数":y_values})
        to_write_df.to_excel(writer, index=False, sheet_name='子系统故障表')

        new_error_big_sub_class = error_big_sub_class.groupby(by=["故障所属主系统","故障所属子系统"]).size().reset_index(name="Size")
        main_err_list = new_error_big_sub_class["故障所属主系统"].unique()
        sub_err_list = new_error_big_sub_class["故障所属子系统"].unique()
        new_data = []
        for i in main_err_list:
            one_list_item = new_error_big_sub_class[new_error_big_sub_class["故障所属主系统"]==i]
            #print("one_list=",one_list)
            one_list = one_list_item.Size.values.tolist()
            have_sub_list = one_list_item["故障所属子系统"].values.tolist()
            new_one_list = [0 for i in list(range(len(sub_err_list)))]

            for i in list(range(len(have_sub_list))):
                for j in list(range(len(sub_err_list))):
                    if sub_err_list[j] == have_sub_list[i]:
                        new_one_list[j] = one_list[i]

            sum_list = np.sum(new_one_list)
            new_one_list = [int(round(j / sum_list * 100, 0)) for j in new_one_list]
            new_data.append(new_one_list)

            new_one_list_median = np.median(new_one_list)

        new_main_err_list = [i[:-2] if i.endswith("系统") else i for i in main_err_list]
        new_data_plot = pd.DataFrame(new_data, columns=sub_err_list, index=new_main_err_list)
        new_data_plot.plot(kind="bar",grid=True,stacked=True)
        plt.title("运营期间各子系统故障占比", fontsize=20)
        plt.xticks(rotation=10, fontsize=3)
        plt.gca().tick_params(axis='both', labelsize=8)
        def to_percent(temp, position):
            return '%1.0f'%(temp) + '%'
        ax1.yaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.grid(axis='x')
        myfont = FontProperties(size=5)
        plt.legend(prop=myfont)
        savefig(full_save_fig_path("各子系统故障占比.jpg"), format='jpg', dpi=save_pig_dpi)
        new_write_contents_main = write_contents_main.format(params_0,params_1,params_2,params_3,params_4,params_5,params_6,params_7)
        writer_analysis_results(new_write_contents_main)

    """
    if errors_union is not None:
        errors_new_union = errors_union.groupby(by=["故障所属主系统","故障处理方式"]).size().reset_index(name="Size")
        #errors_new_union = errors_new_union.sort_values(by=["故障所属主系统","故障处理方式"])
        main_err_list = errors_new_union["故障所属主系统"].unique()
        handle_err_list = errors_new_union["故障处理方式"].unique()
        new_data = []
        for i in main_err_list:
            one_list = errors_new_union[errors_new_union["故障所属主系统"]==i].Size
            one_list = one_list.values.tolist()
            one_list += [0]*(len(handle_err_list)-len(one_list))
            new_data.append(one_list)
        new_data_plot = pd.DataFrame(new_data, columns=handle_err_list, index=main_err_list)

        new_data_plot.plot(kind="bar",grid=True,stacked=True)
        plt.title("运营期间系统各子系统故障数", fontsize=20)
        plt.xticks(rotation=10)
        plt.grid(axis='x')
        savefig(full_save_fig_path("各子系统故障数.jpg"), format='jpg', dpi=save_pig_dpi)

        new_new_data = new_data[:]
        for i in list(range(len(new_new_data))):
            sum_value = np.sum(new_new_data[i])
            new_new_data[i] = [int(round(j / sum_value * 100, 0)) for j in new_new_data[i]]
        new_data_plot = pd.DataFrame(new_new_data, columns=handle_err_list, index=main_err_list)

        new_data_plot.plot(kind="bar",grid=True,stacked=True)
        plt.title("运营期间各子系统故障占比", fontsize=20)
        plt.xticks(rotation=10)
        plt.gca().tick_params(axis='both', labelsize=8)
        def to_percent(temp, position):
            return '%1.0f'%(temp) + '%'
        ax1.yaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.grid(axis='x')
        savefig(full_save_fig_path("各子系统故障占比.jpg"), format='jpg', dpi=save_pig_dpi)
    """

    # 各主系统平均无故障天数（统计表）
    if error_main_no_err_time is not None:
        fig = plt.figure()
        ax1 = plt.gca()
        main_err_list = error_main_no_err_time["故障所属主系统"].unique().tolist()
        main_err_no_err_time = []
        for i in main_err_list:
            try:
                no_err_list = error_main_no_err_time[error_main_no_err_time["故障所属主系统"]==i]["系统平均无故障时间（天）"]
                no_err_list = no_err_list.values.tolist()
                no_err_list = [int(i) for i in no_err_list]
                list_mean = np.rint(np.mean(no_err_list))
                main_err_no_err_time.append(list_mean)
            except Exception as e:
                print("error !!! {0} {1}".format(i, e))
                main_err_no_err_time.append(0)
        x_index = list(range(len(main_err_no_err_time)))
        ax1.bar(x_index, main_err_no_err_time)
        plt.title("各主系统平均无故障天数", fontsize=20)
        new_main_err_list = [i[:-2] if i.endswith("系统") else i for i in main_err_list]
        plt.xticks(x_index, new_main_err_list, rotation=45)
        plt.grid(axis='y')
        savefig(full_save_fig_path("各主系统平均无故障天数.jpg"), format='jpg', dpi=save_pig_dpi)
        #plt.show()

        sorted_main_err_no_err_time = list(zip(main_err_list,main_err_no_err_time))
        sorted_main_err_no_err_time.sort(key=lambda x:x[1])
        sorted_main_err_no_err_time_min_index = 0
        for i in range(len(sorted_main_err_no_err_time)):
            if sorted_main_err_no_err_time[i][1] > 0:
                sorted_main_err_no_err_time_min_index = i
                break
        params_0 = "{0}".format(sorted_main_err_no_err_time[sorted_main_err_no_err_time_min_index][0])
        params_1 = math.ceil(sorted_main_err_no_err_time[sorted_main_err_no_err_time_min_index][1])
        params_2 = "{0}".format(sorted_main_err_no_err_time[-1][0])
        params_3 = math.ceil(sorted_main_err_no_err_time[-1][1])
        params_4 = "{0}".format(sorted_main_err_no_err_time[sorted_main_err_no_err_time_min_index][0])
        params_5 = "{0}".format(sorted_main_err_no_err_time[sorted_main_err_no_err_time_min_index][0])

        to_write_df = pd.DataFrame({"主系统":main_err_list,"无故障天数":main_err_no_err_time})
        to_write_df.to_excel(writer, index=False, sheet_name='主系统平均无故障天数')

        new_write_contents_have_no_error = write_contents_have_no_error.format(params_0, params_1, params_2, params_3, params_4, params_5)
        writer_analysis_results(new_write_contents_have_no_error)

    # 主系统故障平均维修时间分析
    if error_main_repair_time is not None:
        fig = plt.figure()
        ax1 = plt.gca()
        main_err_list = error_main_repair_time["故障所属主系统"].unique().tolist()
        main_err_repair_time = []

        for i in main_err_list:
            try:
                repair_list = error_main_repair_time[error_main_repair_time["故障所属主系统"]==i]["故障平均维修时间（时）"]
                repair_list = repair_list.values.tolist()
                repair_list = [int(i) for i in repair_list]
                list_mean = np.rint(np.mean(repair_list))
                main_err_repair_time.append(list_mean)
            except Exception as e:
                print("error !!! {0} {1}".format(i, e))
                main_err_repair_time.append(0)
        x_index = list(range(len(main_err_repair_time)))
        ax1.bar(x_index, main_err_repair_time)
        plt.title("主系统故障平均维修时间分析（时）", fontsize=20)
        new_main_err_list = [i[:-2] if i.endswith("系统") else i for i in main_err_list]
        plt.xticks(x_index, new_main_err_list, rotation=45)
        plt.grid(axis='y')
        savefig(full_save_fig_path("主系统故障平均维修时间分析.jpg"), format='jpg', dpi=save_pig_dpi)
        #plt.show()

        new_main_err_repair_time = list(zip(main_err_list, main_err_repair_time))
        new_main_err_repair_time.sort(key=lambda x:x[1])
        new_main_err_repair_time_index = 0
        new_main_err_repair_time_bigger_then_4 = 0
        for i in range(len(new_main_err_repair_time)):
            if new_main_err_repair_time[i][1] > 0:
                new_main_err_repair_time_index = i
            if new_main_err_repair_time[i][1] > 4:
                new_main_err_repair_time_bigger_then_4 += 1

        params_0 = "{0}".format(new_main_err_repair_time[-1][0])
        params_1 = math.ceil(new_main_err_repair_time[-1][1])
        params_2 = new_main_err_repair_time_bigger_then_4
        params_3 = "{0}".format(new_main_err_repair_time[new_main_err_repair_time_index][0])
        params_4 = math.ceil(new_main_err_repair_time[new_main_err_repair_time_index][1])
        params_5 = "{0}".format(new_main_err_repair_time[-1][0])

        to_write_df = pd.DataFrame({"主系统":main_err_list,"平均维修时间":main_err_repair_time})
        to_write_df.to_excel(writer, index=False, sheet_name='主系统故障平均维修时间')
        new_write_contents_repair = write_contents_repair.format(params_0,params_1,params_2,params_3,params_4,params_5)
        writer_analysis_results(new_write_contents_repair)

    # 主系统故障处理方式分析
    if error_main_repair_type is not None:
        fig = plt.figure()
        ax1 = plt.gca()

        params_0 = 0
        params_1 = 0
        params_2 = 0
        params_3 = 0
        params_4 = 0
        params_5 = 0
        params_6 = 0
        params_7 = 0
        params_8 = 0
        params_9 = 0
        params_10 = 0

        repair_list = error_main_repair_type.groupby(by=["故障处理方式"]).size().reset_index(name="Size")
        repair_type_num_list = repair_list["Size"].values.tolist()
        params_0 = sum(repair_type_num_list)
        repair_type_list = repair_list["故障处理方式"].values.tolist()
        for i in range(len(repair_type_list)):
            if repair_type_list[i] == "现场处理":
                params_1 = repair_type_num_list[i]
            elif repair_type_list[i] == "备件更换":
                params_2 = repair_type_num_list[i]
            elif repair_type_list[i] == "待处理":
                params_3 = repair_type_num_list[i]
            elif repair_type_list[i] == "其他":
                params_4 = repair_type_num_list[i]
        x_index = list(range(len(repair_type_num_list)))
        ax1.bar(x_index, repair_type_num_list)
        plt.xticks(x_index, repair_type_list, rotation=45)
        plt.grid(axis='y')
        plt.title("不同故障处理方式总数", fontsize=20)
        savefig(full_save_fig_path("不同故障处理方式总数-bar.jpg"), format='jpg', dpi=save_pig_dpi)
        #plt.show()

        to_write_df = pd.DataFrame({"故障类型":repair_type_list,"故障处理方式总数":repair_type_num_list})
        to_write_df.to_excel(writer, index=False, sheet_name='不同故障处理方式总数')

        fig = plt.figure()
        ax1 = plt.gca()
        ax1.pie(repair_type_num_list, labels=repair_type_list, autopct='%1.1f%%')
        plt.title("不同故障处理方式占比", fontsize=20)
        savefig(full_save_fig_path("不同故障处理方式占比-pie.jpg"), format='jpg', dpi=save_pig_dpi)
        #plt.show()

        repair_list_union = error_main_repair_type.groupby(by=["故障所属主系统","故障处理方式"]).size().reset_index(name="Size")
        main_err_list = repair_list_union["故障所属主系统"].unique()
        repair_type_list = repair_list_union["故障处理方式"].unique()
        new_data = []
        handle_type_scene = []
        handle_type_scene_sum = 0
        handle_type_change = []
        handle_type_change_sum = 0

        for m in main_err_list:
            one_list_item = repair_list_union[repair_list_union["故障所属主系统"]==m]
            one_list = one_list_item.Size.values.tolist()
            handle_list = one_list_item["故障处理方式"].values.tolist()
            new_one_list = [0 for i in list(range(len(repair_type_list)))]

            if len(handle_list) == 1 and handle_list[0] == "现场处理":
                params_5 = i
                params_6 = one_list[0]

            for i in list(range(len(handle_list))):
                flag_scene = False
                flag_change = False
                for j in list(range(len(repair_type_list))):
                    if repair_type_list[j] == handle_list[i]:
                        new_one_list[j] = one_list[i]
                    if handle_list[i] == "现场处理":
                        flag_scene = True
                        handle_type_scene.append((m, one_list[i]))
                        handle_type_scene_sum += one_list[i]
                    if handle_list[i] == "备件更换":
                        flag_change = True
                        handle_type_change.append((m, one_list[i]))
                        handle_type_change_sum += one_list[i]
                if not flag_scene:
                    handle_type_scene.append((m, 0))
                if not flag_change:
                    handle_type_change.append((m, 0))

            sum_list = np.sum(new_one_list)
            new_one_list = [int(round(i/sum_list*100, 0)) for i in new_one_list]
            new_data.append(new_one_list)
        new_main_err_list = [i[:-2] if i.endswith("系统") else i for i in main_err_list]
        new_data_plot = pd.DataFrame(new_data, columns=repair_type_list, index=new_main_err_list)
        new_data_plot.plot(kind="bar", grid=True,stacked=True)
        plt.title("各主系统不同故障处理方式占比", fontsize=20)
        plt.xticks(rotation=45,fontsize=8)
        def to_percent(temp, position):
            return '%1.0f'%(temp) + '%'
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.grid(axis='x')
        savefig(full_save_fig_path("不同故障处理方式总数占比.jpg"), format='jpg', dpi=save_pig_dpi)
        #plt.show()

        handle_type_scene.sort(key=lambda x:x[1])
        params_7 = handle_type_scene[-1][0]
        params_8 = "{0}%".format(round(handle_type_scene[-1][1]/handle_type_scene_sum, 2))
        handle_type_change.sort(key=lambda x:x[1])
        params_9 = handle_type_change[-1][0]
        params_10 = "{0}%".format(round(handle_type_change[-1][1]/handle_type_change_sum, 2))
        params_11 = params_7

        new_write_contents_main_handle = write_contents_main_handle.format(params_0, params_1, params_2, params_3, params_4, params_5, params_6, params_7, params_8, params_9, params_10, params_11)
        writer_analysis_results(new_write_contents_main_handle)

    # 车辆故障分析
    if car_err_num is not None:
        fig = plt.figure()
        ax1 = plt.gca()
        car_err_num_list = car_err_num.groupby(by=["列车号"]).size().reset_index(name="Size")
        car_err_size = car_err_num_list["Size"].values.tolist()
        car_types = car_err_num_list["列车号"].values.tolist()
        x_index = list(range(len(car_err_size)))
        ax1.bar(x_index, car_err_size)
        plt.xticks(x_index, car_types, fontsize=8)
        plt.title("各车辆故障数", fontsize=20)
        plt.grid(axis="y")
        savefig(full_save_fig_path("各车辆故障数.jpg"), format='jpg', dpi=save_pig_dpi)

        to_write_df = pd.DataFrame({"车辆类型":car_types,"故障数":car_err_size})
        to_write_df.to_excel(writer, index=False, sheet_name='各车辆故障表')

        fig = plt.figure()
        ax1 = plt.gca()
        list_sum = np.sum(car_err_size)
        new_car_err_size = [int(round(i/list_sum*100, 0)) for i in car_err_size]
        params_0 = "{0}".format(car_types[0])
        params_1 = round(car_err_size[0]/list_sum*100, 2)
        params_2 = "{0}、{1}、{2}".format(car_types[0],car_types[1],car_types[2])
        params_3 = "{0}、{1}".format(car_types[0],car_types[1])
        ax1.bar(x_index, new_car_err_size)
        plt.xticks(x_index, car_types, fontsize=8)
        plt.title("各车辆故障数-占比", fontsize=20)
        def to_percent(temp, position):
            return '%1.0f'%(temp) + '%'
        ax1.yaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.grid(axis="y")
        savefig(full_save_fig_path("各车辆故障数-占比.jpg"), format='jpg', dpi=save_pig_dpi)

        new_write_contents_errors = write_contents_errors.format(params_0,params_1,params_2,params_3)
        writer_analysis_results(new_write_contents_errors)


    # 车辆平均无故障时间分析
    if car_no_err_day is not None:
        fig = plt.figure()
        ax1 = plt.gca()
        car_types = car_no_err_day["列车号"].unique().tolist()
        car_types.sort()
        car_types_no_err = []
        for i in car_types:
            try:
                car_no_err = car_no_err_day[car_no_err_day["列车号"]==i]["系统平均无故障时间（天）"].values.tolist()
                no_err_mean = np.mean(car_no_err)
                car_types_no_err.append(no_err_mean)
            except Exception as e:
                print("error !!! {0} {1}".format(i,e))
                car_types_no_err.append(0)
        x_index = list(range(len(car_types_no_err)))
        ax1.bar(x_index, car_types_no_err)
        plt.xticks(x_index, car_types)
        plt.title("车辆平均无故障时间", fontsize=20)
        plt.grid(axis="y")
        savefig(full_save_fig_path("车辆平均无故障时间.jpg"), format='jpg', dpi=save_pig_dpi)

        new_car_types_no_err = list(zip(car_types, car_types_no_err))
        new_car_types_no_err.sort(key=lambda x:x[1])
        new_car_types_no_err_min_index = 0
        for i in range(len(new_car_types_no_err)):
            if new_car_types_no_err[i][1] > 0:
                new_car_types_no_err_min_index = i
                break
        params_0 = new_car_types_no_err[new_car_types_no_err_min_index][0]
        params_1 = math.ceil(new_car_types_no_err[new_car_types_no_err_min_index][1])
        params_2 = new_car_types_no_err[-1][0]
        params_3 = math.ceil(new_car_types_no_err[-1][1])

        new_write_contents_have_no_error_time = write_contents_have_no_error_time.format(params_0,params_1,params_2,params_3)
        writer_analysis_results(new_write_contents_have_no_error_time)

    writer.save()


if __name__ == '__main__':
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    statistic_excel()
    #os.system("pause")
