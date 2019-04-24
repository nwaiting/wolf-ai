#coding=utf-8

import os
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


def statistic_excel():
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
        x_labels = error_main.value_counts().index.tolist()
        y_values = error_main.value_counts().tolist()
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
        x_labels = error_big_sub_class["故障所属子系统"].value_counts().index.tolist()
        y_values = error_big_sub_class["故障所属子系统"].value_counts().tolist()
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

        to_write_df = pd.DataFrame({"主系统":main_err_list,"无故障天数":main_err_no_err_time})
        to_write_df.to_excel(writer, index=False, sheet_name='主系统平均无故障天数')

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

        to_write_df = pd.DataFrame({"主系统":main_err_list,"平均维修时间":main_err_repair_time})
        to_write_df.to_excel(writer, index=False, sheet_name='主系统故障平均维修时间')


    # 主系统故障处理方式分析
    if error_main_repair_type is not None:
        fig = plt.figure()
        ax1 = plt.gca()
        repair_list = error_main_repair_type.groupby(by=["故障处理方式"]).size().reset_index(name="Size")
        repair_type_num_list = repair_list["Size"].values.tolist()
        repair_type_list = repair_list["故障处理方式"].values.tolist()
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
        for i in main_err_list:
            one_list_item = repair_list_union[repair_list_union["故障所属主系统"]==i]
            one_list = one_list_item.Size.values.tolist()
            handle_list = one_list_item["故障处理方式"].values.tolist()
            new_one_list = [0 for i in list(range(len(repair_type_list)))]

            for i in list(range(len(handle_list))):
                for j in list(range(len(repair_type_list))):
                    if repair_type_list[j] == handle_list[i]:
                        new_one_list[j] = one_list[i]

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
        ax1.bar(x_index, new_car_err_size)
        plt.xticks(x_index, car_types, fontsize=8)
        plt.title("各车辆故障数-占比", fontsize=20)
        def to_percent(temp, position):
            return '%1.0f'%(temp) + '%'
        ax1.yaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.grid(axis="y")
        savefig(full_save_fig_path("各车辆故障数-占比.jpg"), format='jpg', dpi=save_pig_dpi)


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

    writer.save()


if __name__ == '__main__':
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    statistic_excel()
    os.system("pause")
