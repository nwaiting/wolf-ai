import tkinter as tk
import itertools


class App(object):
    def __init__(self):
        self.window = tk.Tk()
        self.sets_list = []
        self.results_list = []
        self.input_sets = ''
        self.show_sets = tk.StringVar()

    def main_page(self):
        """
        初始化
        """
        self.window.title('集合演算工具')
        self.window.geometry('600x600')
        # 输入
        tk.Label(self.window, text='输入:').place(x=10, y=50)
        # 输入框
        self.input_sets = tk.StringVar()
        entry_input_sets = tk.Entry(self.window, textvariable=self.input_sets, width=60)
        entry_input_sets.place(x=100, y=50)
        # 运算方式
        tk.Label(self.window, text='运算方式:').place(x=10, y=100)
        # 并集按钮
        bt_1 = tk.Button(self.window, text='并集', command=self.cal_union, width=8)
        bt_1.place(x=100, y=100)
        # 交集按钮
        bt_2 = tk.Button(self.window, text='交集', command=self.cal_intersection, width=7)
        bt_2.place(x=180, y=100)
        # 相对补按钮
        bt_3 = tk.Button(self.window, text='相对补', command=self.cal_complement, width=7)
        bt_3.place(x=260, y=100)
        # 对称差按钮
        bt_4 = tk.Button(self.window, text='对称差', command=self.cal_symmetry_difference, width=7)
        bt_4.place(x=340, y=100)
        # 幂集求解按钮
        bt_4 = tk.Button(self.window, text='幂集求解', command=self.cal_power_set, width=7)
        bt_4.place(x=420, y=100)
        # 笛卡尔积按钮
        bt_4 = tk.Button(self.window, text='笛卡尔积', command=self.cal_cartesian_product, width=7)
        bt_4.place(x=500, y=100)

        # 结果
        tk.Label(self.window, text='结果:').place(x=10, y=170)
        # 显示框
        self.show_sets = tk.StringVar()
        tk.Entry(self.window, textvariable=self.show_sets, width=60, state='readonly').place(x=100, y=170)

    def show_tables(self, datas):
        if len(datas) > 1:
            self.show_sets.set(' '.join([str(i) for i in datas[0]]))
            for i in range(1, len(datas)):
                s = tk.StringVar()
                s.set(' '.join([str(j) for j in datas[i]]))
                tk.Entry(self.window, textvariable=s, width=60, state='readonly').place(x=100, y=170+i*20)
        else:
            self.show_sets.set(' '.join([str(i) for i in self.results_list]))

    def parse_set_str(self):
        in_str = self.input_sets.get().strip('\r\n ')
        in_str_items = in_str.split('-')
        self.sets_list = []
        for item in in_str_items:
            if item:
                item_items = item.split(',')
                self.sets_list.append([int(i) for i in item_items])

    def cal_complement(self):
        # 补集
        self.results_list = []
        self.parse_set_str()
        original_list = self.sets_list[0]
        for i in range(1, len(self.sets_list)):
            original_list = list(set(original_list).difference(self.sets_list[i]))
        self.results_list.append(original_list)
        self.show_tables(self.results_list)

    def cal_union(self):
        # 并集按钮
        self.results_list = []
        self.parse_set_str()
        original_list = self.sets_list[0]
        for i in range(1, len(self.sets_list)):
            original_list = list(set(original_list).union(self.sets_list[i]))
        self.results_list.append(original_list)
        self.show_tables(self.results_list)

    def cal_intersection(self):
        # 交集
        self.results_list = []
        self.parse_set_str()
        original_list = self.sets_list[0]
        for i in range(1, len(self.sets_list)):
            original_list = list(set(original_list).intersection(self.sets_list[i]))
        self.results_list.append(original_list)
        self.show_tables(self.results_list)

    def cal_symmetry_difference(self):
        # 对称差
        self.results_list = []
        self.parse_set_str()
        original_list = self.sets_list[0]
        for i in range(1, len(self.sets_list)):
            original_list = list(set(original_list).symmetric_difference(set(self.sets_list[i])))
        self.results_list.append(original_list)
        self.show_tables(self.results_list)

    def cal_cartesian_product(self):
        # 笛卡尔积 多行显示
        self.results_list = []
        self.parse_set_str()
        new_list = []
        for item in itertools.product(*self.sets_list):
            new_list.append(item)
        self.show_tables(new_list)

    def cal_power_set(self):
        # 幂集求解 多行显示
        self.results_list = []
        self.parse_set_str()
        s = self.sets_list[0]
        # for r in range(len(s) + 1):
        #     itertools.combinations(set(s), r)
        tmp_list = []
        for r in range(len(s) + 1):
            tmp_list.append(itertools.combinations(set(s), r))
        # res = itertools.combinations(set(s), r) for r in range(len(s) + 1)
        # res_list = itertools.chain.from_iterable(itertools.combinations(set(s), r) for r in range(len(s) + 1))
        res_list = itertools.chain.from_iterable(tmp_list)

        for i in res_list:
            self.results_list.append(i)
        self.show_tables(self.results_list)

    def run(self):
        self.window.mainloop()

    def quit(self):
        self.window.destroy()


if __name__ == '__main__':
    app = App()
    app.main_page()
    app.run()

