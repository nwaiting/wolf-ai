from tkinter.messagebox import showinfo
import tkinter as tk
from tkinter import ttk, Frame, RAISED, VERTICAL, NS, HORIZONTAL, EW
import sqlite3
import pandas as pd
import os


class App(object):
    def __init__(self):
        self.window_main_page = tk.Tk()
        self.add_data_page = None
        self.add_student_no = None
        self.add_student_name = None
        self.add_student_phone = None
        self.add_student_english = None
        self.add_student_phy = None
        self.add_student_math = None
        self.add_student_computer = None
        self.db_connect_path = 'students_info.db'
        self.csv_data_file = 'students_info.csv'
        self.db_connect = None
        self.db_init()
        self.info_page = None

        self.students_info_dict = {}
        self.insert_data_list = []
        self.lv = None

        self.user_datas_info = None
        self.account_datas = None

        self.before_update_data = None
        self.before_update_data_index = None

    def run(self):
        self.window_main_page.mainloop()

    def hide(self):
        self.window_main_page.withdraw()

    def load_datas(self):
        if os.path.exists(self.csv_data_file):
            pd_datas = pd.read_csv(self.csv_data_file)
            for item in pd_datas.values:
                pass
        res = self.db_load_data()
        if res:
            for i in range(1, self.lv.end_row() + 1):
                self.lv.delete_row(i)
            self.insert_data_list = []

            for item in res:
                self.lv.add_row(True, item)
                self.insert_data_list.append(item[0])

    def db_delete_by_st_no(self, no):
        sql = f"delete from students_info where st_no={no}"
        self.db_execute(sql, ())

    def db_load_data(self):
        sql = "select st_no,st_name,st_phone,st_en,st_phy,st_math,st_compyter from students_info"
        res = self.db_execute(sql, ())
        return res if res else []

    def db_reconnect(self):
        try:
            self.db_connect.close()
        except:
            pass
        try:
            self.db_connect = sqlite3.connect(self.db_connect_path)
        except:
            pass

    def db_init(self):
        self.db_connect = sqlite3.connect(self.db_connect_path)
        sql = '''CREATE TABLE  IF NOT EXISTS students_info
               (id integer PRIMARY KEY     autoincrement,
               st_no           TEXT    NOT NULL,
               st_name           TEXT    NOT NULL,
               st_phone           TEXT    NOT NULL,
               st_en            INT     NOT NULL,
               st_phy            INT     NOT NULL,
               st_math            INT     NOT NULL,
               st_compyter            INT     NOT NULL);
               '''
        args = ()
        c = self.db_connect.cursor()
        try:
            c.execute(sql, args)
            self.db_connect.commit()
        except Exception as e:
            print("err {}".format(e))
            self.db_reconnect()

    # 保存数据到sqlite
    def db_save(self,datas):
        c = self.db_connect.cursor()
        try:
            for data in datas:
                sql = f"insert into students_info(id,st_no,st_name,st_phone,st_en,st_phy,st_math,st_compyter) " \
                    f"VALUES(NUll, {data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]},{data[6]})"
                c.execute(sql, ())
            self.db_connect.commit()
        except Exception as e:
            print("==== {}".format(e))
            self.db_reconnect()

    # sql 执行
    def db_execute(self, sql, args):
        c = self.db_connect.cursor()
        try:
            res = c.execute(sql, args)
            self.db_connect.commit()
            return res
        except Exception as e:
            print('err ======== {}'.format(e))
            self.db_reconnect()

    # 主页面
    def main_page(self):
        # 确认存储时的相应函数
        def add_save_data():
            # 获取数据
            add_student_no = self.add_student_no.get()
            add_student_name = self.add_student_name.get()
            add_student_phone = self.add_student_phone.get()
            add_student_english = self.add_student_english.get()
            add_student_phy = self.add_student_phy.get()
            add_student_math = self.add_student_math.get()
            add_student_computer = self.add_student_computer.get()
            if not add_student_no or not add_student_name or not add_student_phone:
                return

            if add_student_no in self.students_info_dict:
                showinfo("提示", '{} 信息已存在，请确认重新输入'.format(add_student_no))
                return

            datas = []
            datas.append((add_student_no,add_student_name,add_student_phone,add_student_english,add_student_phy,
                          add_student_math,add_student_computer))
            self.db_save(datas)
            self.students_info_dict[add_student_no] = {
                "st_no": add_student_no,
                "st_name": add_student_name,
                "st_phone": add_student_phone,
                "st_en": add_student_english,
                "st_phy": add_student_phy,
                "st_math": add_student_math,
                "st_computer": add_student_computer
            }
            self.insert_data_list.append(add_student_no)
            self.lv.add_row(True, [add_student_no,add_student_name,add_student_phone,add_student_english,add_student_phy,
                          add_student_math,add_student_computer])
            self.add_data_page.destroy()

        def add_cancel():
            self.add_data_page.destroy()

        def update_data():
            select_index = int(self.lv.get_index_select())
            sql = f"select st_no,st_name,st_phone,st_en,st_phy,st_math,st_compyter from students_info where st_no={self.insert_data_list[select_index - 1]}"
            res = self.db_execute(sql, ())
            data = [item for item in res]
            if data:
                data = data[0]
                self.before_update_data_index = select_index
                self.before_update_data = data[:]
                self.info_page_update = tk.Toplevel(self.window_main_page)
                self.info_page_update.geometry('300x300')
                self.info_page_update.title('修改')

                row1 = tk.Frame(self.info_page_update)
                row1.pack(fill="x")
                tk.Label(row1, text='学号：', width=8).pack(side=tk.LEFT)
                self.s1 = tk.StringVar()
                self.s1.set(data[0])
                tk.Entry(row1, textvariable=self.s1, width=20, state='readonly').pack(side=tk.LEFT)

                row2 = tk.Frame(self.info_page_update)
                row2.pack(fill="x")
                tk.Label(row2, text='姓名：', width=8).pack(side=tk.LEFT)
                self.s2 = tk.StringVar()
                self.s2.set(data[1])
                tk.Entry(row2, textvariable=self.s2, width=20).pack(side=tk.LEFT)

                row3 = tk.Frame(self.info_page_update)
                row3.pack(fill="x")
                tk.Label(row3, text='手机号：', width=8).pack(side=tk.LEFT)
                self.s3 = tk.StringVar()
                self.s3.set(data[2])
                tk.Entry(row3, textvariable=self.s3, width=20).pack(side=tk.LEFT)

                row4 = tk.Frame(self.info_page_update)
                row4.pack(fill="x")
                tk.Label(row4, text='英语：', width=8).pack(side=tk.LEFT)
                self.s4 = tk.StringVar()
                self.s4.set(data[3])
                tk.Entry(row4, textvariable=self.s4, width=20).pack(side=tk.LEFT)

                row5 = tk.Frame(self.info_page_update)
                row5.pack(fill="x")
                tk.Label(row5, text='数学：', width=8).pack(side=tk.LEFT)
                self.s5 = tk.StringVar()
                self.s5.set(data[4])
                tk.Entry(row5, textvariable=self.s5, width=20).pack(side=tk.LEFT)

                row6 = tk.Frame(self.info_page_update)
                row6.pack(fill="x")
                tk.Label(row6, text='物理：', width=8).pack(side=tk.LEFT)
                self.s6 = tk.StringVar()
                self.s6.set(data[5])
                tk.Entry(row6, textvariable=self.s6, width=20).pack(side=tk.LEFT)

                row7 = tk.Frame(self.info_page_update)
                row7.pack(fill="x")
                tk.Label(row7, text='计算机二级：', width=8).pack(side=tk.LEFT)
                self.s7 = tk.StringVar()
                self.s7.set(data[6])
                tk.Entry(row7, textvariable=self.s7, width=20).pack(side=tk.LEFT)

                # 确定
                bt_confirm_sign_up = tk.Button(self.info_page_update, text='确定', command=update_data_ok, width=10)
                bt_confirm_sign_up.place(x=60, y=180)
                # 取消
                bt_cancel_sign_up = tk.Button(self.info_page_update, text='取消', command=update_cancel, width=10)
                bt_cancel_sign_up.place(x=160, y=180)

        def update_data_ok():
            if self.before_update_data:
                if self.before_update_data[0] != self.s1.get():
                    showinfo("提示", '不能修改学号')
                    self.info_page_update.destroy()
                    return
                new_data_item = [self.s1.get(),self.s2.get(),self.s3.get(),self.s4.get(),
                                               self.s5.get(),self.s6.get(),self.s7.get()]
                if self.before_update_data != new_data_item:
                    self.insert_data_list.pop(self.before_update_data_index-1)
                    self.lv.delete_row(self.before_update_data_index)

                    sql = f"update students_info set st_name={new_data_item[1]},st_phone={new_data_item[2]},st_en={new_data_item[3]}," \
                        f"st_phy={new_data_item[4]},st_math={new_data_item[5]},st_compyter={new_data_item[6]} where st_no={new_data_item[0]}"
                    self.db_execute(sql, ())

                    self.insert_data_list.append(new_data_item[0])
                    self.lv.add_row(True, new_data_item)
                    self.info_page_update.destroy()

        def update_cancel():
            self.info_page_update.destroy()

        def update_label(v):
            if self.s3_button_index % 2 == 1:
                self.s3.set("*"*len(self.item_data_info.get('pwd')))
            else:
                self.s3.set(self.item_data_info.get('pwd'))
            self.s3_button_index += 1

        def query_data_ok():
            sql = ''
            if self.student_query_no.get():
                sql = f"select st_no,st_name,st_phone,st_en,st_phy,st_math,st_compyter from students_info where st_no={self.student_query_no.get()}"
            elif self.student_query_name.get():
                sql = f"select st_no,st_name,st_phone,st_en,st_phy,st_math,st_compyter from students_info where st_name={self.student_query_name.get()}"
            elif self.student_query_phone.get():
                sql = f"select st_no,st_name,st_phone,st_en,st_phy,st_math,st_compyter from students_info where st_phone={self.student_query_phone.get()}"
            if sql:
                res = self.db_execute(sql, ())
                datas = [data for data in res]
                if datas:
                    for i in range(1, self.lv.end_row()+1):
                        self.lv.delete_row(i)
                        self.insert_data_list = []
                    for item in datas:
                        self.lv.add_row(True, item)
                        self.insert_data_list.append(item[0])
                else:
                    showinfo("提示", '查询信息已不存在')

            self.info_page.destroy()

        def query_cancel():
            self.info_page.destroy()

        def query_data():
            self.info_page = tk.Toplevel(self.window_main_page)
            self.info_page.geometry('300x300')
            self.info_page.title('学生信息查询')

            row1 = tk.Frame(self.info_page)
            row1.pack(fill="x")
            tk.Label(row1, text='学号：', width=8).pack(side=tk.LEFT)
            self.student_query_no = tk.StringVar()
            tk.Entry(row1, textvariable=self.student_query_no, width=20).pack(side=tk.LEFT)

            row2 = tk.Frame(self.info_page)
            row2.pack(fill="x")
            tk.Label(row2, text='姓名：', width=8).pack(side=tk.LEFT)
            self.student_query_name = tk.StringVar()
            tk.Entry(row2, textvariable=self.student_query_name, width=20).pack(side=tk.LEFT)

            row3 = tk.Frame(self.info_page)
            row3.pack(fill="x")
            tk.Label(row3, text='手机号：', width=8).pack(side=tk.LEFT)
            self.student_query_phone = tk.StringVar()
            tk.Entry(row3, textvariable=self.student_query_phone, width=20).pack(side=tk.LEFT)

            # 确定
            bt_confirm_sign_up = tk.Button(self.info_page, text='确定', command=query_data_ok, width=10)
            bt_confirm_sign_up.place(x=60, y=180)
            # 取消
            bt_cancel_sign_up = tk.Button(self.info_page, text='取消', command=query_cancel, width=10)
            bt_cancel_sign_up.place(x=160, y=180)

        def reset_show():
            self.load_datas()

        def del_data():
            select_index = int(self.lv.get_index_select())
            delete_no = self.insert_data_list[select_index - 1]
            self.insert_data_list.pop(select_index - 1)

            self.lv.delete_row(int(self.lv.get_index_select()))
            self.db_delete_by_st_no(delete_no)

        def add_item_data():
            self.add_data_page = tk.Toplevel(self.window_main_page)
            self.add_data_page.geometry('400x300')
            self.add_data_page.title('添加学生信息')

            # 学号
            self.add_student_no = tk.StringVar()
            tk.Label(self.add_data_page, text='学号：').place(x=10, y=10)
            tk.Entry(self.add_data_page, textvariable=self.add_student_no, width=20).place(x=130, y=10)
            # 姓名
            self.add_student_name = tk.StringVar()
            tk.Label(self.add_data_page, text='姓名：').place(x=10, y=30)
            tk.Entry(self.add_data_page, textvariable=self.add_student_name, width=20).place(x=130, y=30)
            # 手机
            self.add_student_phone = tk.StringVar()
            tk.Label(self.add_data_page, text='手机 ：').place(x=10, y=50)
            tk.Entry(self.add_data_page, textvariable=self.add_student_phone, width=20).place(x=130, y=50)

            # 英语
            self.add_student_english = tk.StringVar()
            tk.Label(self.add_data_page, text='英语：').place(x=10, y=70)
            tk.Entry(self.add_data_page, textvariable=self.add_student_english, width=20).place(x=130, y=70)
            # 数学
            self.add_student_math = tk.StringVar()
            tk.Label(self.add_data_page, text='数学：').place(x=10, y=90)
            tk.Entry(self.add_data_page, textvariable=self.add_student_math, width=20).place(x=130, y=90)
            # 物理
            self.add_student_phy = tk.StringVar()
            tk.Label(self.add_data_page, text='物理 ：').place(x=10, y=110)
            tk.Entry(self.add_data_page, textvariable=self.add_student_phy, width=20).place(x=130, y=110)
            # 计算机二级
            self.add_student_computer = tk.StringVar()
            tk.Label(self.add_data_page, text='计算机二级 ：').place(x=10, y=130)
            tk.Entry(self.add_data_page, textvariable=self.add_student_computer, width=20).place(x=130, y=130)

            # 确定
            bt_confirm_sign_up = tk.Button(self.add_data_page, text='确定', command=add_save_data, width=10)
            bt_confirm_sign_up.place(x=60, y=180)
            # 取消
            bt_cancel_sign_up = tk.Button(self.add_data_page, text='取消', command=add_cancel, width=10)
            bt_cancel_sign_up.place(x=160, y=180)

        self.lv = ListView(self.window_main_page, x=130, y=40, width=1000, height=600)
        self.lv.add_column('学号', 100)
        self.lv.add_column('姓名', 100)
        self.lv.add_column('手机', 100)
        self.lv.add_column('英语', 100)
        self.lv.add_column('数学', 100)
        self.lv.add_column('物理', 100)
        self.lv.add_column('计算机二级', 100)
        self.lv.create_listview()
        # 操作主界面
        self.window_main_page.geometry('1000x400')
        self.window_main_page.title('学生成绩分析系统')

        tk.Label(self.window_main_page, text='学生成绩信息：').place(x=10, y=40)

        # 查询按钮以及位置
        query_data_button = tk.Button(self.window_main_page, text='查询', command=query_data, width=10)
        query_data_button.place(x=10, y=90)

        # 修改按钮及位置
        update_data_button = tk.Button(self.window_main_page, text='修改', command=update_data, width=10)
        update_data_button.place(x=10, y=120)

        # 删除按钮及位置
        del_data_button = tk.Button(self.window_main_page, text='删除', command=del_data, width=10)
        del_data_button.place(x=10, y=150)

        # 添加按钮及位置
        add_data_button = tk.Button(self.window_main_page, text='添加', command=add_item_data, width=10)
        add_data_button.place(x=10, y=180)

        # 重置按钮及位置
        reset_button = tk.Button(self.window_main_page, text='重置', command=reset_show, width=10)
        reset_button.place(x=10, y=210)

        self.load_datas()

    # 退出的函数
    def usr_sign_quit(self):
        self.window.destroy()


class ListView(object):
    char_ct = ' '
    chat_cf = ' '

    def __init__(self, tk, x=0, y=0, height=400, width=600):
        self.tk = tk
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.rows_count = 0
        self.cols_count = 0
        self.head_tags = ['index']
        self.head_widths = [50]
        self.head_texts = ['']
        self.tree = None
        self.__created = False  # 控制表格创建后，停用部分方法
        self.__check_boxes = True  # 标识是否有复选框功能
        self.__show_index = True  # 标识是否显示行号

    def create_listview(self):
        """
        设置好列后，执行这个函数显示出控件
        """
        if self.__created:
            print('不能再次创建！')
        else:
            self.__created = True
            self.cols_count = len(self.head_tags) - 1  # 第一列用作索引了

            frame1 = Frame(self.tk, relief=RAISED)
            frame1.place(height=self.height, width=self.width, x=self.x, y=self.y)
            frame1.propagate(0)  # 使组件大小不变，此时width才起作用

            # 定义listview
            self.tree = ttk.Treeview(frame1, columns=self.head_tags, show='headings')
            self.tree.column(self.head_tags[0], width=self.head_widths[0], anchor='center')  # stretch=YES怎么用
            for i in range(1, len(self.head_tags)):
                self.tree.column(self.head_tags[i], width=self.head_widths[i], anchor='center')
                self.tree.heading(self.head_tags[i], text=self.head_texts[i])

            # 设置垂直滚动条
            vbar = ttk.Scrollbar(frame1, orient=VERTICAL, command=self.tree.yview)
            self.tree.configure(yscrollcommand=vbar.set)
            # self.tree.grid(row=0, column=0, sticky=NSEW)
            self.tree.grid(row=0, column=0)
            vbar.grid(row=0, column=1, sticky=NS)

            # 设置水平滚动条
            hbar = ttk.Scrollbar(frame1, orient=HORIZONTAL, command=self.tree.xview)
            self.tree.configure(xscrollcommand=hbar.set)
            hbar.grid(row=1, column=0, sticky=EW)

            # 绑定事件
            self.tree.bind('<ButtonRelease-1>', self.on_click)  # 绑定行单击事件

    def add_column(self, text='', width=100):
        """
        增加一列，应该在show()前面设定，后面就无效了
        :param text: 表头文字
        :param width: 列宽度
        """
        if self.__created:
            print('表格已经创建，在增加的列无效！')
        else:
            self.head_tags.append(len(self.head_tags))
            self.head_widths.append(width)
            self.head_texts.append(text)

    def add_row_char(self, check_char=char_ct, vals=''):
        """
        在最后增加一行
        """
        if self.__check_boxes:
            if check_char != ListView.char_ct:
                check_char = ListView.chat_cf
            index = '%s%d' % (check_char, self.rows_count + 1)
        else:
            index = self.rows_count + 1

        values = [index]
        for v in vals:
            values.append(v)
        self.tree.insert('', 'end', values=values)
        self.rows_count += 1

    def add_row(self, check_bl=True, vals=''):
        """
        在最后增加一行
        """
        check_char = self.check_bl2char(check_bl)
        self.add_row_char(check_char, vals)

    def set_check(self, state=True):
        """
        设置是否有复选功能
        """
        if self.__created:
            print('表格创建后，不能设置复选状态!')
        else:
            self.__check_boxes = state

    def set_width(self, col_num, width):
        """
        设置列宽
        :param col_num: 列号
        :param width: 宽度
        """
        self.tree.column("#%d" % col_num, width=width)  # 可以动态改变列宽

    def set_head_font(self, font='黑体', size=15):
        # 设置表头字体大小
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(font, size))

    def set_rows_height(self, height=30):
        """
        设置行高
        :param height: 行高
        """
        s = ttk.Style()
        s.configure('Treeview', rowheight=height)

    def set_rows_fontsize(self, font=15):
        """
        设置字号
        :param font: 字号
        """
        s = ttk.Style()
        s.configure('Treeview', font=(None, font))

    def set_rows_height_fontsize(self, height=30, font=15):
        """
        设置行高和字号
        :param height: 行高
        :param font: 字号
        """
        s = ttk.Style()
        s.configure('Treeview', rowheight=height, font=(None, font))

    def get_row(self, row_num):
        """
        获取一行的对象，供tree.item调用
        :param row_num:行号
        :return: 行对象
        """
        if row_num in range(1, self.rows_count + 1):
            items = self.tree.get_children()
            for it in items:
                index = self.get_index_by_item(it)
                if int(index) == int(row_num):
                    return it

    def get_row_values_by_item(self, item):
        """
        获取一行的值内容，包含行头部信息
        :param row_num: 行号
        :return: 元组,1为头部信息，1以后为表格信息
        """
        values = self.tree.item(item, 'values')
        return values

    def get_row_vals_head(self, row_num):
        """
        获取一行的值内容，包含行头部信息
        :param row_num: 行号
        :return: 元组,1为头部信息，1以后为表格信息
        """
        item = self.get_row(row_num)
        return self.get_row_values_by_item(item)

    def get_row_vals_by_item(self, item):
        """
        获取一行的表格内容
        :param item: 对象
        :return: 列表，索引从0开始
        """
        values = self.tree.item(item, 'values')
        vals = []
        for i in range(1, len(values)):
            vals.append(values[i])
        return vals

    def get_row_vals(self, row_num):
        """
        获取一行的表格内容
        :param row_num: 行号
        :return: 列表，索引从0开始
        """
        item = self.get_row(row_num)
        return self.get_row_vals_by_item(item)

    def get_row_head(self, row_num):
        """
        获取一行的表头内容，包含复选框和索引
        :param row_num: 行号
        :return: 字符串
        """
        row_vals = self.get_row_vals_head(row_num)
        return row_vals[1]

    def get_index_by_values(self, values):
        """
        获取一行的索引
        :param values: 行数据（包含行头部信息）
        :return: 索引（整数）
        """
        if self.__check_boxes:
            index = values[0][1:]
        else:
            index = values[0]
        return index

    def get_index_by_item(self, item):
        """
        获取一行的索引
        :param by_item: 行对象
        :return: 索引（整数）
        """
        values = self.tree.item(item, 'values')
        return self.get_index_by_values(values)

    def get_index(self, row_num):
        """
        获取一行的索引
        :param row_num: 行号
        :return: 索引（整数）
        """
        item = self.get_row(row_num)
        return self.get_index_by_item(item)

    def get_index_select(self):
        """
        获取选中行的行号
        :return: 行号
        """
        try:
            item = self.tree.selection()[0]  # 获取行对象
        except Exception:
            return 1
        return self.get_index_by_item(item)

    def get_cell_by_item(self, col_num, item):
        """
        获取指定单元格的值
        :param col_num: 列号
        :param item: 行对象
        :return: 值
        """
        if col_num in range(1, self.cols_count + 1):
            values = self.get_row_values_by_item(item)
            return values[col_num + 1]

    def get_cell(self, row_num, col_num):
        """
        获取指定单元格的值
        :param row_num: 行号
        :param col_num: 列号
        :return: 值
        """
        item = self.get_row(row_num)
        return self.get_cell_by_item(col_num, item)

    def get_cell_selectrow(self, col_num):
        """
        获取选中行中某一列的数据
        :param col_num: 列
        :return: 一个单元格的值
        """
        item = self.tree.selection()[0]  # 获取行对象
        return self.get_cell_by_item(col_num, item)

    def get_checkbl_by_values(self, values):
        """
        获取某一行的勾选状况
        :param values: 行数据（包含行头部信息）
        """
        if self.__check_boxes:
            check_str = values[0][0:1]
            if check_str == ListView.char_ct:
                return True
            else:
                return False

    def get_checkbl_by_item(self, item):
        """
        获取某一行的勾选状况
        :param item: 行对象
        """
        values = self.get_row_values_by_item(item)
        return self.get_checkbl_by_values(values)

    def get_check_bl(self, row_num):
        """
        获取某一行的勾选状况
        :param row_num: 行号
        """
        item = self.get_row(row_num)
        return self.get_checkbl_by_item(item)

    def get_checkchar_by_values(self, values):
        """
        获取某一行的勾选符号
        :param item: 行数据（包含行头部信息）
        """
        if self.__check_boxes:
            check_str = values[0][0:1]
        else:
            check_str = ''
        return check_str

    def get_checkchar_by_item(self, item):
        """
        获取某一行的勾选符号
        :param item: 行对象
        """
        values = self.get_row_values_by_item(item)
        return self.get_checkchar_by_values(values)

    def get_check_char(self, row_num):
        """
        获取某一行的勾选符号
        :param item: 行对象
        """
        item = self.get_row(row_num)
        return self.get_checkchar_by_item(item)

    def change_check_by_item(self, item, check_bl=True):
        """
        修改一行的复选状态
        :param item: 行对象
        :param check_bl:复选状态
        """
        if self.__check_boxes:
            check_char = self.check_bl2char(check_bl)
            index = self.get_index_by_item(item)
            value = '%s%s' % (check_char, index)
            col_str = '#%d' % 1
            self.tree.set(item, column=col_str, value=value)

    def change_check_by_item_char(self, item, check_char=char_ct):
        """
        修改一行的复选状态
        :param item: 行对象
        :param check_char:复选字符
        """
        if self.__check_boxes:
            index = self.get_index_by_item(item)
            value = '%s%s' % (check_char, index)
            col_str = '#%d' % 1
            self.tree.set(item, column=col_str, value=value)

    def exchange_check_by_item(self, item):
        """
        变换一行的复选状态
        """
        if self.__check_boxes:
            vals = self.get_row_values_by_item(item)
            check_str = vals[0][0:1]
            index = vals[0][1:]
            if check_str == ListView.char_ct:
                value = ListView.chat_cf + index
            else:
                value = ListView.char_ct + index
            col_str = '#%d' % 1
            self.tree.set(item, column=col_str, value=value)  # 修改单元格的值

    def exchange_check(self, row_num):
        """
        变换一行的复选状态
        """
        item = self.get_row(row_num)
        self.exchange_check_by_item(item)

    def change_check_on_select(self):
        """
        改变选中行的勾选状态
        """
        try:
            item = self.tree.selection()[0]  # 获取行对象
        except Exception:
            pass
        else:
            self.exchange_check_by_item(item)

    def change_head_by_item(self, item, check_char, index):
        """
        修改一行的头部信息
        :param item:
        :param check_char: 复选框符号
        :param index: 行号
        """
        value = '%s%s' % (check_char, index)
        col_str = '#%d' % 1
        self.tree.set(item, column=col_str, value=value)

    def change_head(self, row_num, check_char, index):
        """
        修改一行的头部信息
        :param item:
        :param check_char: 复选框符号
        :param index: 行号
        """
        item = self.get_row(row_num)
        value = '%s%s' % (check_char, index)
        col_str = '#%d' % 1
        self.tree.set(item, column=col_str, value=value)

    def change_row_by_vals_item(self, item, vals, check_char=char_ct):
        """
        修改一整行的值
        :param item: 行对象
        :param vals: 表格值列表（vals不包含行头部信息）
        """
        self.change_check_by_item_char(item, check_char)
        end_col = len(vals)
        if self.cols_count < len(vals):
            end_col = self.cols_count
        for i in range(0, end_col):
            col_str = '#%d' % (i + 2)
            self.tree.set(item, column=col_str, value=vals[i])

    def change_row_by_vals(self, row_num, vals, check_char=char_ct):
        """
        修改一整行的值
        :param row_num: 行号
        :param vals: 值列表
        """
        item = self.get_row(row_num)
        self.change_row_by_vals_item(item, vals, check_char)

    def change_row_check_values_by_item(self, item, values):
        """
        修改一整行的值
        :param item: 行对象
        :param values: 表格值列表（包含行头部信息）
        """
        end_col = len(values) - 1
        if self.cols_count < len(values) - 1:
            end_col = self.cols_count
        # 写入头部信息
        check_char = self.get_checkchar_by_values(values)
        index = self.get_index_by_item(item)
        self.change_head_by_item(item, check_char, index)
        # 写入行表格内容
        for i in range(0, end_col):
            col_str = '#%d' % (i + 2)
            self.tree.set(item, column=col_str, value=values[i + 1])

    def change_row_check_vals_by_item_char(self, item, check_char, vals):
        """
        修改一整行的值
        :param item: 行对象
        :param check_char:复选框符号
        :param vals: 表格值列表（不包含行头部信息）
        :return:
        """
        end_col = len(vals)
        if self.cols_count < len(vals):
            end_col = self.cols_count
        # 写入头部信息
        index = self.get_index_by_item(item)
        self.change_head_by_item(item, check_char, index)
        # 写入行表格内容
        for i in range(0, end_col):
            col_str = '#%d' % (i + 2)
            self.tree.set(item, column=col_str, value=vals[i])

    def change_row_all_by_item_char(
            self, item, check_char, index, vals):
        """
        修改一整行的值
        :param item: 行对象
        :param check_char: 复选框符号
        :param index: 行号
        :param vals: 表格值列表（不包含行头部信息）
        :return:
        """
        end_col = len(vals)
        if self.cols_count < len(vals):
            end_col = self.cols_count
        # 写入头部信息
        self.change_head_by_item(item, check_char, index)
        # 写入行表格内容
        for i in range(0, end_col):
            col_str = '#%d' % (i + 2)
            self.tree.set(item, column=col_str, value=vals[i])

    def change_row_all_by_item_char_vals(
            self, item, check_char, index, vals):
        """
        修改一整行的值
        :param item: 行对象
        :param check_char: 复选框符号
        :param index: 行号
        :param vals: 表格值列表（不包含行头部信息）
        """
        end_col = len(vals)
        if self.cols_count < len(vals):
            end_col = self.cols_count
        # 写入头部信息
        self.change_head_by_item(item, check_char, index)
        # 写入行表格内容
        for i in range(0, end_col):
            col_str = '#%d' % (i + 2)
            self.tree.set(item, column=col_str, value=vals[i])

    def change_row_all_by_item_bl_vals(
            self, item, check_bl, index, vals):
        """
        修改一整行的值
        :param item: 行对象
        :param check_bl: 复选框状态
        :param index: 行号
        :param values: 表格值列表（包含行头部信息）
        """
        check_char = self.check_bl2char(check_bl)
        self.change_row_all_by_item_char_vals(item, check_char, index, vals)

    def change_row_all_by_item_char_values(
            self, item, check_char, index, values):
        """
        修改一整行的值
        :param item: 行对象
        :param check_char: 复选框符号
        :param index: 行号
        :param values: 表格值列表（包含行头部信息）
        """
        end_col = len(values) - 1
        if self.cols_count < len(values) - 1:
            end_col = self.cols_count
        # 写入头部信息
        self.change_head_by_item(item, check_char, index)
        # 写入行表格内容
        for i in range(0, end_col):
            col_str = '#%d' % (i + 2)
            self.tree.set(item, column=col_str, value=values[i + 1])

    def change_row_all_by_item_bl_values(
            self, item, check_bl, index, values):
        """
        修改一整行的值
        :param item: 行对象
        :param check_bl: 复选框状态
        :param index: 行号
        :param values: 表格值列表（包含行头部信息）
        """
        check_char = self.check_bl2char(check_bl)
        self.change_row_all_by_item_char_values(item, check_char, index, values)

    def change_row_all_by_item_bl(
            self, item, check_bl, index, vals):
        """
        修改一整行的值
        :param item: 行对象
        :param check_bl: 复选框状态
        :param index: 行号
        :param vals: 表格值列表（不包含行头部信息）
        :return:
        """
        check_char = self.check_bl2char(check_bl)
        self.change_row_all_by_item_char(item, check_char, index, vals)

    def change_row_check_vals(self, row_num, values):
        """
        修改一整行的值
        :param row_num: 行号
        :param values: 表格值列表（包含行头部信息）
        """
        item = self.get_row(row_num)
        self.change_row_check_values_by_item(item, values)

    def change_cell_by_item(self, item, col_num, value):
        """
        修改单个单元格的值
        :param item: 行对象
        :param col_num: 列号
        :param value: 值
        """
        if col_num in range(1, self.cols_count + 1):
            col_str = '#%d' % (col_num + 1)
            self.tree.set(item, column=col_str, value=value)

    def change_cell(self, row_num, col_num, value):
        """
        修改单个单元格的值
        :param row_num: 行号
        :param col_num: 列号
        :param value: 值
        """
        item = self.get_row(row_num)
        self.change_cell_by_item(item, col_num, value)

    def check_bl2char(self, bl=True):
        """
        返回复选框符号
        :param bl: True代表已选，False未选中
        :return: 复选框
        """
        if bl:
            return ListView.char_ct
        else:
            return ListView.chat_cf

    def check_char2bl(self, char=char_ct):
        """
        返回复选框符号
        :param char: ☑代表已选
        :return: 复选框
        """
        if char == ListView.char_ct:
            return True
        else:
            return False

    def check_all(self):
        """
        将所有行勾选
        """
        if self.__check_boxes:
            items = self.tree.get_children()
            for it in items:
                vals = self.tree.item(it, 'values')
                index = vals[0][1:]
                value = '☑%s' % index
                col_str = '#%d' % 1
                self.tree.set(it, column=col_str, value=value)  # 修改单元格的值

    def check_all_not(self):
        """
        取消所有行勾选
        """
        if self.__check_boxes:
            items = self.tree.get_children()
            for it in items:
                vals = self.tree.item(it, 'values')
                index = vals[0][1:]
                value = '□%s' % index
                col_str = '#%d' % 1
                self.tree.set(it, column=col_str, value=value)  # 修改单元格的值

    def check_all_un(self):
        """
        将所有行的复选取反
        """
        if self.__check_boxes:
            items = self.tree.get_children()
            for it in items:
                vals = self.tree.item(it, 'values')
                check_str = vals[0][0:1]
                index = vals[0][1:]
                if check_str == ListView.char_ct:
                    value = ListView.chat_cf + index
                else:
                    value = ListView.char_ct + index
                col_str = '#%d' % 1
                self.tree.set(it, column=col_str, value=value)  # 修改单元格的值

    def clear_row_by_item(self, item):
        """
        清除一行的内容
        :param item: 行对象
        """
        self.change_check_by_item_char(item, ListView.chat_cf)
        vals = []
        for i in range(0, self.cols_count):
            vals.append('')

        for i in range(0, self.cols_count):
            col_str = '#%d' % (i + 2)
            self.tree.set(item, column=col_str, value=vals[i])

    def clear_row(self, row_num):
        """
        清除一行的内容,不是删除整行
        :param row_num: 行号
        """
        item = self.get_row(row_num)
        self.clear_row_by_item(item)

    def clear_cell_by_item(self, item, col_num):
        """
        清空单个单元格的值
        :param item: 行对象
        :param col_num: 列号
        """
        if col_num in range(1, self.cols_count + 1):
            col_str = '#%d' % (col_num + 1)
            self.tree.set(item, column=col_str, value='')

    def clear_cell(self, row_num, col_num):
        """
        清空单个单元格的值
        :param row_num: 行号
        :param col_num: 列号
        """
        item = self.get_row(row_num)
        self.clear_cell_by_item(item, col_num)

    def clear_col(self, col_num):
        """
        清空一整列数据
        :param col_num: 列号
        """
        if col_num in range(1, self.cols_count + 1):
            col_str = '#%d' % (col_num + 1)
            items = self.tree.get_children()
            for item in items:
                self.tree.set(item, column=col_str, value='')

    def delete_row(self, row_num):
        """
        删除整行，包括数据和复选框
        :param row_num: 行号
        """
        items = self.tree.get_children()
        if row_num < self.rows_count:
            # 第一步，清空需要删除行的数据
            self.clear_row_by_item(items[row_num - 1])
            # 第二步，将目标行以后的数据全部上移
            for i in range(row_num, self.rows_count):
                check_char_temp = self.get_checkchar_by_item(items[i])
                vals_temp = self.get_row_vals_by_item(items[i])
                self.change_row_check_vals_by_item_char(
                    items[i - 1], check_char_temp, vals_temp)
        # 第三步，删除最后一行
        self.tree.delete(items[self.rows_count - 1])
        self.rows_count -= 1

    def end_row(self):
        """
        最后一行的行号
        """
        return len(self.tree.get_children())

    def inset_row(self, row_num, vals, check_char=char_ct):
        """
        在指定行前插入行
        :param row_num:在该行号前插入
        :param vals: 行的内容
        :param check_char: 复选符号
        """
        if row_num > self.rows_count:  # 加在最后
            self.add_row_char(check_char, vals)
        else:
            # 在最后增加一个空白行
            self.add_row_char()
            # 循环移动插入行后面的所有行
            items = self.tree.get_children()
            for i in range(len(items) - 1, row_num - 1, -1):
                check_char_temp = self.get_checkchar_by_item(items[i - 1])
                vals_temp = self.get_row_vals_by_item(items[i - 1])
                self.change_row_check_vals_by_item_char(
                    items[i], check_char_temp, vals_temp)
            # 将新内容插入到指定行号中
            self.clear_row_by_item(items[row_num - 1])
            self.change_row_check_vals_by_item_char(
                items[row_num - 1], check_char, vals)

    def inset_row_bl(self, row_num, vals, check_bl=True):
        """
        在指定行前插入行
        :param row_num:在该行号前插入
        :param vals: 行的内容
        :param check_bl: 复选状态
        """
        check_char = self.check_bl2char(check_bl)
        self.inset_row(row_num, vals, check_char)

    def copy_row(self, target_num, to_num):
        """
        将一行复制到另外一行
        :param row_num1: 行号1
        :param row_num2: 行号2
        """
        target_item = self.get_row(target_num)
        target_check_str = self.get_checkchar_by_item(target_item)
        target_vals = self.get_row_vals_by_item(target_item)
        to_item = self.get_row(to_num)
        to_index = self.get_index_by_item(to_item)
        self.change_row_all_by_item_char_vals(
            to_item, target_check_str, to_index, target_vals)

    def exchange_row(self, row_num1, row_num2):
        """
        交换两行的数据和复选状态
        :param row_num1: 行号1
        :param row_num2: 行号2
        """
        item1 = self.get_row(row_num1)
        item2 = self.get_row(row_num2)
        self.exchange_row_by_item(item1, item2)

    def exchange_row_by_item(self, item1, item2):
        """
        交换两行的数据和复选状态
        :param item1: 行对象
        :param item2: 行对象
        """
        values1 = self.get_row_values_by_item(item1)
        values2 = self.get_row_values_by_item(item2)

        check_char1 = self.get_checkchar_by_values(values1)
        check_char2 = self.get_checkchar_by_values(values2)
        index1 = self.get_index_by_values(values1)
        index2 = self.get_index_by_values(values2)

        self.change_row_all_by_item_char_values(item1, check_char2, index1, values2)
        self.change_row_all_by_item_char_values(item2, check_char1, index2, values1)

    def on_click(self, event):
        """
        行单击事件
        """
        self.change_check_on_select()


if __name__ == '__main__':
    app = App()
    app.main_page()
    app.run()

