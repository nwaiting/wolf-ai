import hashlib
from tkinter.messagebox import showinfo
import tkinter as tk
from tkinter import ttk, Frame, RAISED, VERTICAL, NS, HORIZONTAL, EW
import socket


class MyNetWork(object):
    def __init__(self, host='127.0.0.1', port=58888):
        self._host = host
        self._port = port
        self._s = None

    def connect(self):
        if not self._s:
            self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._s.connect((self._host, self._port))

    def recv(self):
        msg = self._s.recv(1024)
        return msg

    def send(self, msg):
        return self._s.send(msg.encode('utf-8'))

class ListView(object):
    char_ct = ' '  # 复选框选中标识符
    chat_cf = ' '  # 复选框未选中标识符

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


class App(object):
    def __init__(self):
        self.window = tk.Tk()
        self.user_datas_info = {}
        self.account_datas = None
        self.window_main_page = None
        self.lv = None
        self.insert_data_list = []
        self.tmp_data = None
        self.tmp_index = None
        self.tmp_pwd = None
        self.entry_usr_pwd = None
        self.add_user_name = None
        self.add_nick_name = None
        self.add_user_pwd = None

        self.addr_str = None
        self.net_work = MyNetWork()
        self.all_stock_infos = {}
        self.has_stock = {}
        self.current_hand_stock = None

    def init(self):
        """
        初始化
        """
        self.window.title('股票交易系统')
        self.window.geometry('450x300')
        # 画布放置图片
        canvas = tk.Canvas(self.window, height=300, width=500)
        canvas.pack(side='top')

        # 显示地址
        tk.Label(self.window, text='地址:').place(x=100, y=30)
        # 地址输入框
        self.addr_str = tk.StringVar()
        self.addr_str.set("127.0.0.1:58888")
        entry_addr_str = tk.Entry(self.window, textvariable=self.addr_str, state=tk.DISABLED)
        entry_addr_str.place(x=160, y=30)

        # 标签 用户名密码
        tk.Label(self.window, text='用户名:').place(x=100, y=80)
        tk.Label(self.window, text='密码:').place(x=100, y=120)
        # 用户名输入框
        self.var_usr_name = tk.StringVar()
        entry_usr_name = tk.Entry(self.window, textvariable=self.var_usr_name)
        entry_usr_name.place(x=160, y=80)
        # 密码输入框
        self.var_usr_pwd = tk.StringVar()
        self.var_usr_pwd_index = 0
        self.entry_usr_pwd = tk.Entry(self.window, textvariable=self.var_usr_pwd, show='*')
        self.entry_usr_pwd.place(x=160, y=120)
        # 登录 按钮
        bt_login = tk.Button(self.window, text='登录', command=self.usr_log_in, width=10)
        bt_login.place(x=100, y=190)

        # 注册 按钮
        bt_register = tk.Button(self.window, text='注册', command=self.usr_register, width=10)
        bt_register.place(x=220, y=190)

    def run(self):
        self.window.mainloop()

    def hide(self):
        self.window.withdraw()

    def save_user_data(self):
        with open('user_datas.pl', 'wb') as usr_file:
            for k,v in self.user_datas_info.items():
                usr_file.write(("{} {} {}\n".format(v.get("username"), v.get("nickname"),  self.crypt.encrypt(v.get("pwd")))).encode('utf-8'))

    # 注册
    def usr_register(self):
        self.net_work.connect()
        usr_name = self.var_usr_name.get()
        usr_pwd = self.var_usr_pwd.get()
        if not usr_name or not usr_pwd:
            tk.messagebox.showinfo(title='系统提示', message='账号或者密码为空')
            return
        self.net_work.send("1-{}-{}".format(usr_name, usr_pwd))
        data = self.net_work.recv()
        if data:
            tk.messagebox.showinfo(title='系统提示', message='注册成功')

    # 登录函数
    def usr_log_in(self):
        def parse_stock(self, d):
            tmp_data_items = d.split('-')
            for item in tmp_data_items:
                tmp_map_item = item.split(',')
                tmp_dict = {}
                for i in range(1, len(tmp_map_item), 2):
                    tmp_dict[tmp_map_item[i]] = tmp_map_item[i+1]
                if tmp_map_item[0]:
                    self.all_stock_infos[tmp_map_item[0]] = tmp_dict
        def parse_has_stock(self, d):
            tmp_data_items = d.split('-')
            for item in tmp_data_items:
                if item:
                    tmp_map_item = item.split(',')
                    self.has_stock[tmp_map_item[0]] = int(tmp_map_item[1])
        self.net_work.connect()
        # 输入框获取用户名密码
        usr_name = self.var_usr_name.get()
        usr_pwd = self.var_usr_pwd.get()
        self.net_work.send("2-{}-{}".format(usr_name, usr_pwd))
        data = self.net_work.recv()
        data = data.decode('utf-8')
        if data.startswith('err'):
            tk.messagebox.showinfo(title='系统提示', message='用户名或者密码错误，登录失败')
            return

        parse_stock(self, data)
        print("self.all_stock_infos={}".format(self.all_stock_infos))
        buy_data = self.net_work.recv()
        buy_data = buy_data.decode('utf-8')
        if buy_data and not buy_data.startswith('has no'):
            parse_has_stock(self, buy_data)

        # 解析数据，然后刷新表格
        self.hide()
        self.main_page()
        self.lv = ListView(self.window_main_page, x=130, y=40, width=800, height=600)
        self.lv.add_column('股票代码', 100)
        self.lv.create_listview()
        self.update_text_box_data()

    def update_text_box_data(self):
        for k,v in self.all_stock_infos.items():
            row = [k]
            self.lv.add_row(True, row)
            self.insert_data_list.append(k)

    # 登录成功主页面
    def main_page(self):
        def sell_page_ok():
            # 4-600016-1000-9.6
            if self.has_stock[self.current_hand_stock] < int(self.sell_number.get()):
                tk.messagebox.showinfo(title='系统提示',
                                       message='卖出数量大于持有数量，卖出失败!!!')
                return
            if self.sell_number.get():
                self.net_work.send("{}-{}-{}-{}".format(4, self.current_hand_stock, self.sell_number.get(),
                                                        self.all_stock_infos[self.current_hand_stock]['sell01']))
                data = self.net_work.recv()
                if data:
                    data = data.decode('utf-8')
                    if data.startswith('success'):
                        self.has_stock[self.current_hand_stock] = self.has_stock.get(self.current_hand_stock, 0) - int(self.sell_number.get())
                        data_items = data.split('-')
                        tk.messagebox.showinfo(title='系统提示', message='卖出{}股{}成功，价格为{}'.format(self.sell_number.get(),
                                                                                              self.current_hand_stock,
                                                                                              data_items[1]))
                    else:
                        tk.messagebox.showinfo(title='系统提示', message='卖出失败')
            sell_page_cancel()

        def sell_page_cancel():
            self.sell_page.destroy()

        def sell_data():
            # 卖出
            select_index = int(self.lv.get_index_select())
            data_info = self.has_stock.get(self.insert_data_list[select_index-1], 0)

            self.current_hand_stock = self.insert_data_list[select_index-1]

            self.sell_page = tk.Toplevel(self.window_main_page)
            self.sell_page.geometry('300x300')
            self.sell_page.title('卖出')

            # 当前持有
            tk.Label(self.sell_page, text='当前持有:').place(x=10, y=50)
            # 当前持有
            entry_has_stock_var = tk.StringVar()
            entry_has_stock_var.set(data_info)
            entry_has_stock = tk.Entry(self.sell_page, textvariable=entry_has_stock_var, state=tk.DISABLED)
            entry_has_stock.place(x=80, y=50)

            # 买入数量
            tk.Label(self.sell_page, text='卖出数量:').place(x=10, y=80)
            # 买入输入框
            self.sell_number = tk.StringVar()
            entry_buy_number = tk.Entry(self.sell_page, textvariable=self.sell_number)
            entry_buy_number.place(x=80, y=80)

            # 确认
            bt_buy_page_ok = tk.Button(self.sell_page, text='确认', command=sell_page_ok, width=10)
            bt_buy_page_ok.place(x=40, y=150)

            # 取消
            bt_buy_page_cancel = tk.Button(self.sell_page, text='取消', command=sell_page_cancel, width=10)
            bt_buy_page_cancel.place(x=150, y=150)

        def buy_page_ok():
            # 3-600016-1000-9.6
            if self.buy_number.get():
                self.net_work.send("{}-{}-{}-{}".format(3, self.current_hand_stock, self.buy_number.get(),
                                                        self.all_stock_infos[self.current_hand_stock]['buy01']))
                data = self.net_work.recv()
                if data:
                    data = data.decode('utf-8')
                    if data.startswith('success'):
                        self.has_stock[self.current_hand_stock] = self.has_stock.get(self.current_hand_stock, 0) + int(self.buy_number.get())
                        data_items = data.split('-')
                        tk.messagebox.showinfo(title='系统提示', message='买入{}股{}成功，买入价格 {}'.format(
                            self.buy_number.get(), self.current_hand_stock, data_items[1]))
                    else:
                        tk.messagebox.showinfo(title='系统提示', message='买入失败')
            buy_page_cancel()

        def buy_page_cancel():
            self.buy_page.destroy()

        def buy_data():
            # 买入
            select_index = int(self.lv.get_index_select())
            data_info = self.has_stock.get(self.insert_data_list[select_index-1], 0)

            self.current_hand_stock = self.insert_data_list[select_index-1]

            self.buy_page = tk.Toplevel(self.window_main_page)
            self.buy_page.geometry('300x300')
            self.buy_page.title('买入')

            # 当前持有
            tk.Label(self.buy_page, text='当前持有:').place(x=10, y=50)
            # 当前持有
            entry_has_stock_var = tk.StringVar()
            entry_has_stock_var.set(data_info)
            entry_has_stock = tk.Entry(self.buy_page, textvariable=entry_has_stock_var, state=tk.DISABLED)
            entry_has_stock.place(x=80, y=50)

            # 买入数量
            tk.Label(self.buy_page, text='买入数量:').place(x=10, y=80)
            # 买入输入框
            self.buy_number = tk.StringVar()
            entry_buy_number = tk.Entry(self.buy_page, textvariable=self.buy_number)
            entry_buy_number.place(x=80, y=80)

            # 确认
            bt_buy_page_ok = tk.Button(self.buy_page, text='确认', command=buy_page_ok, width=10)
            bt_buy_page_ok.place(x=40, y=150)

            # 取消
            bt_buy_page_cancel = tk.Button(self.buy_page, text='取消', command=buy_page_cancel, width=10)
            bt_buy_page_cancel.place(x=150, y=150)

        def query_data():
            select_index = int(self.lv.get_index_select())
            self.item_data_info = self.all_stock_infos.get(self.insert_data_list[select_index-1], {})
            if self.item_data_info:
                self.info_page = tk.Toplevel(self.window_main_page)
                self.info_page.geometry('300x300')
                self.info_page.title('基本信息')

                row1 = tk.Frame(self.info_page)
                row1.pack(fill="x")
                tk.Label(row1, text='买1：', width=8).pack(side=tk.LEFT)
                self.s1 = tk.StringVar()
                self.s1.set(self.item_data_info.get('buy01'))
                tk.Entry(row1, textvariable=self.s1, width=20, state=tk.DISABLED).pack(side=tk.LEFT)

                row2 = tk.Frame(self.info_page)
                row2.pack(fill="x")
                tk.Label(row2, text='买2：', width=8).pack(side=tk.LEFT)
                self.s2 = tk.StringVar()
                self.s2.set(self.item_data_info.get('buy02'))
                tk.Entry(row2, textvariable=self.s2, width=20, state=tk.DISABLED).pack(side=tk.LEFT)

                row3 = tk.Frame(self.info_page)
                row3.pack(fill="x")
                tk.Label(row3, text='买3：', width=8).pack(side=tk.LEFT)
                self.s3_button_index = 1
                self.s3 = tk.StringVar()
                self.s3.set(self.item_data_info.get('buy03'))
                self.box3 = tk.Entry(row3, textvariable=self.s3, width=20, state=tk.DISABLED)
                self.box3.pack(side=tk.LEFT)

                row4 = tk.Frame(self.info_page)
                row4.pack(fill="x")
                tk.Label(row4, text='买4：', width=8).pack(side=tk.LEFT)
                self.s3_button_index = 1
                self.s4 = tk.StringVar()
                self.s4.set(self.item_data_info.get('buy04'))
                self.box4 = tk.Entry(row4, textvariable=self.s4, width=20, state=tk.DISABLED)
                self.box4.pack(side=tk.LEFT)

                row5 = tk.Frame(self.info_page)
                row5.pack(fill="x")
                tk.Label(row5, text='买5：', width=8).pack(side=tk.LEFT)
                self.s3_button_index = 1
                self.s5 = tk.StringVar()
                self.s5.set(self.item_data_info.get('buy05'))
                self.box5 = tk.Entry(row5, textvariable=self.s5, width=20, state=tk.DISABLED)
                self.box5.pack(side=tk.LEFT)

                row6 = tk.Frame(self.info_page)
                row6.pack(fill="x")
                tk.Label(row6, text='卖1：', width=8).pack(side=tk.LEFT)
                self.s6 = tk.StringVar()
                self.s6.set(self.item_data_info.get('sell01'))
                tk.Entry(row6, textvariable=self.s6, width=20, state=tk.DISABLED).pack(side=tk.LEFT)

                row7 = tk.Frame(self.info_page)
                row7.pack(fill="x")
                tk.Label(row7, text='卖2：', width=8).pack(side=tk.LEFT)
                self.s7 = tk.StringVar()
                self.s7.set(self.item_data_info.get('sell02'))
                tk.Entry(row7, textvariable=self.s7, width=20, state=tk.DISABLED).pack(side=tk.LEFT)

                row8 = tk.Frame(self.info_page)
                row8.pack(fill="x")
                tk.Label(row8, text='卖3：', width=8).pack(side=tk.LEFT)
                self.s8 = tk.StringVar()
                self.s8.set(self.item_data_info.get('sell03'))
                tk.Entry(row8, textvariable=self.s8, width=20, state=tk.DISABLED).pack(side=tk.LEFT)

                row9 = tk.Frame(self.info_page)
                row9.pack(fill="x")
                tk.Label(row9, text='卖4：', width=8).pack(side=tk.LEFT)
                self.s9 = tk.StringVar()
                self.s9.set(self.item_data_info.get('sell04'))
                tk.Entry(row9, textvariable=self.s9, width=20, state=tk.DISABLED).pack(side=tk.LEFT)

                row10 = tk.Frame(self.info_page)
                row10.pack(fill="x")
                tk.Label(row10, text='卖5：', width=8).pack(side=tk.LEFT)
                self.s10 = tk.StringVar()
                self.s10.set(self.item_data_info.get('sell05'))
                tk.Entry(row10, textvariable=self.s10, width=20, state=tk.DISABLED).pack(side=tk.LEFT)

                row11 = tk.Frame(self.info_page)
                row11.pack(fill="x")
                tk.Label(row11, text='持有：', width=8).pack(side=tk.LEFT)
                self.s11 = tk.StringVar()
                self.s11.set(self.has_stock.get(self.insert_data_list[select_index-1], 0))
                tk.Entry(row11, textvariable=self.s11, width=20, state=tk.DISABLED).pack(side=tk.LEFT)

        # 操作主界面
        self.window_main_page = tk.Toplevel(self.window)
        self.window_main_page.geometry('500x400')
        self.window_main_page.title('主页面')
        tk.Label(self.window_main_page, text='股票信息：').place(x=10, y=40)

        # 查询按钮以及位置
        query_data_button = tk.Button(self.window_main_page, text='查询', command=query_data, width=10)
        query_data_button.place(x=10, y=90)

        # 卖出按钮及位置
        sell_data_button = tk.Button(self.window_main_page, text='卖出', command=sell_data, width=10)
        sell_data_button.place(x=10, y=120)

        # 买入按钮及位置
        buy_data_button = tk.Button(self.window_main_page, text='买入', command=buy_data, width=10)
        buy_data_button.place(x=10, y=150)

    # 退出的函数
    def usr_sign_quit(self):
        self.window.destroy()


if __name__ == '__main__':
    app = App()
    app.init()
    app.run()

