import tkinter as tk
import itertools


window = tk.Tk()
sets_list = []
results_list = []
input_sets = tk.StringVar()
show_sets = tk.StringVar()


def main_page():
    """
    初始化
    """
    window.title('集合演算工具')
    window.geometry('600x600')
    # 输入
    tk.Label(window, text='输入(英文状态):').place(x=10, y=50)
    # 输入框
    entry_input_sets = tk.Entry(window, textvariable=input_sets, width=60)
    entry_input_sets.place(x=100, y=50)
    # 运算方式
    tk.Label(window, text='运算方式:').place(x=10, y=100)
    # 并集按钮
    bt_1 = tk.Button(window, text='并集', command=cal_union, width=8)
    bt_1.place(x=100, y=100)
    # 交集按钮
    bt_2 = tk.Button(window, text='交集', command=cal_intersection, width=7)
    bt_2.place(x=180, y=100)
    # 相对补按钮
    bt_3 = tk.Button(window, text='相对补', command=cal_complement, width=7)
    bt_3.place(x=260, y=100)
    # 对称差按钮
    bt_4 = tk.Button(window, text='对称差', command=cal_symmetry_difference, width=7)
    bt_4.place(x=340, y=100)
    # 幂集求解按钮
    bt_4 = tk.Button(window, text='幂集求解', command=cal_power_set, width=7)
    bt_4.place(x=420, y=100)
    # 笛卡尔积按钮
    bt_4 = tk.Button(window, text='笛卡尔积', command=cal_cartesian_product, width=7)
    bt_4.place(x=500, y=100)

    # 结果
    tk.Label(window, text='结果:').place(x=10, y=170)
    # 显示框
    tk.Entry(window, textvariable=show_sets, width=60, state='readonly').place(x=100, y=170)

def show_tables(datas):
    if len(datas) > 1:
        show_sets.set(' '.join([str(i) for i in datas[0]]))
        for i in range(1, len(datas)):
            s = tk.StringVar()
            s.set(' '.join([str(j) for j in datas[i]]))
            tk.Entry(window, textvariable=s, width=60, state='readonly').place(x=100, y=170+i*20)
    else:
        show_sets.set(' '.join([str(i) for i in datas[0]]))

def parse_set_str():
    global sets_list
    in_str = input_sets.get().strip('\r\n ')
    in_str_items = in_str.split('-')
    sets_list = []
    for item in in_str_items:
        if item:
            item_items = item.split(',')
            sets_list.append([int(i) for i in item_items])

def cal_complement():
    # 补集
    global sets_list
    results_list = []
    parse_set_str()
    original_list = sets_list[0]
    for i in range(1, len(sets_list)):
        original_list = list(set(original_list).difference(sets_list[i]))
    results_list.append(original_list)
    show_tables(results_list)

def cal_union():
    # 并集按钮
    global sets_list
    results_list = []
    parse_set_str()
    original_list = sets_list[0]
    for i in range(1, len(sets_list)):
        original_list = list(set(original_list).union(sets_list[i]))
    results_list.append(original_list)
    show_tables(results_list)

def cal_intersection():
    # 交集
    results_list = []
    parse_set_str()
    original_list = sets_list[0]
    for i in range(1, len(sets_list)):
        original_list = list(set(original_list).intersection(sets_list[i]))
    results_list.append(original_list)
    show_tables(results_list)

def cal_symmetry_difference():
    # 对称差
    results_list = []
    parse_set_str()
    original_list = sets_list[0]
    for i in range(1, len(sets_list)):
        original_list = list(set(original_list).symmetric_difference(set(sets_list[i])))
    results_list.append(original_list)
    show_tables(results_list)

def cal_cartesian_product():
    # 笛卡尔积 多行显示
    results_list = []
    parse_set_str()
    show_tables(list(itertools.product(*sets_list)))

def cal_power_set():
    # 幂集求解 多行显示
    results_list = []
    parse_set_str()
    s = sets_list[0]
    tmp_list = []
    for r in range(len(s) + 1):
        tmp_list.append(itertools.combinations(set(s), r))
    res_list = itertools.chain.from_iterable(tmp_list)
    for i in res_list:
        results_list.append(i)
    show_tables(results_list)


main_page()
window.mainloop()

