from tkinter.messagebox import showinfo
import tkinter as tk
from tkinter import ttk, Frame, RAISED, VERTICAL, NS, HORIZONTAL, EW
import pickle
import time
import hashlib
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class MyCrypt(object):
    """
        代码实现的思想：将加密文本处理以8*16位 这样的单位进行加密，每16个字节长度的数据加密成16个字节长度的密文。
            在下面代码中，为简化代码，密钥所生成的key和iv都用16位的密钥代替，实际上其实可以不一样，但位数能不能不一样就没试了。

        AES拥有很多模式，如CBC模式：通过密钥和salt（起扰乱作用）按固定算法（md5）产生key和iv。
            然后用key和iv（初始向量，加密第一块明文）加密（明文）和解密（密文）
    """
    def __init__(self):
        self.mode = AES.MODE_OFB
        self.key = 'aes_keysaes_keysaes_keys'  #密钥

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, msg):
        """
        加密
        """
        cryptor = AES.new(self.key.encode('utf-8'), self.mode, b'0000000000000000')
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(msg)
        if count % length != 0:
            add = length - (count % length)
        else:
            add = 0
        message = msg + ('\0' * add)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        ciphertext = cryptor.encrypt(message.encode('utf-8'))
        result = b2a_hex(ciphertext)
        return result.decode('utf-8')

    def decrypt(self, en_msg):
        """
        解密
        解密后，去掉补足的空格用strip() 去掉
        """
        cryptor = AES.new(self.key.encode('utf-8'), self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(en_msg))
        return plain_text.decode('utf-8').rstrip('\0')


class App(object):
    def __init__(self):
        self.window = tk.Tk()
        self.user_datas_info = None
        self.account_datas = None
        self.window_main_page = None
        self.lv = None
        self.insert_data_list = []
        self.tmp_data = None
        self.tmp_index = None
        self.crypt = MyCrypt()
        self.login_pwd = None
        self.tmp_pwd = None
        self.entry_usr_pwd = None
        self.add_user_name = None
        self.add_nick_name = None
        self.add_user_pwd = None

    def init(self):
        """
        初始化
        """
        self.window.title('密码存储查询系统')
        self.window.geometry('450x300')
        # 画布放置图片
        canvas = tk.Canvas(self.window, height=300, width=500)
        # imagefile = tk.PhotoImage(file='qm.png')
        image = canvas.create_image(0, 0, anchor='nw', image=None)
        canvas.pack(side='top')
        # 标签 用户名密码
        tk.Label(self.window, text='用户名:').place(x=100, y=100)
        tk.Label(self.window, text='密码:').place(x=100, y=140)
        # 用户名输入框
        self.var_usr_name = tk.StringVar()
        entry_usr_name = tk.Entry(self.window, textvariable=self.var_usr_name)
        entry_usr_name.place(x=160, y=100)
        # 密码输入框
        self.var_usr_pwd = tk.StringVar()
        self.var_usr_pwd_index = 0
        self.entry_usr_pwd = tk.Entry(self.window, textvariable=self.var_usr_pwd, show='*')
        self.entry_usr_pwd.place(x=160, y=140)
        # 登录 注册按钮
        bt_login = tk.Button(self.window, text='登录', command=self.usr_log_in, width=20)
        bt_login.place(x=140, y=190)

    def run(self):
        self.window.mainloop()

    def hide(self):
        self.window.withdraw()

    @staticmethod
    def cal_hash(s):
        md5 = hashlib.md5()
        md5.update(s.encode('utf8'))
        return md5.hexdigest()

    def add_user_data(self, username, nickname, pwd):
        key = self.cal_hash("{}{}{}".format(username, nickname, pwd))
        if key in self.user_datas_info:
            return
        self.user_datas_info[key] = {"username": username,
                                     "nickname": nickname,
                                     "pwd": pwd
                                    }
        self.save_user_data()
        self.insert_data_list.append(key)

    def save_user_data(self):
        with open('user_datas.pl', 'wb') as usr_file:
            for k,v in self.user_datas_info.items():
                usr_file.write(("{} {} {}\n".format(v.get("username"), v.get("nickname"),  self.crypt.encrypt(v.get("pwd")))).encode('utf-8'))
            # pickle.dump(self.user_datas_info, usr_file)

    # 登录函数
    def usr_log_in(self):
        # 输入框获取用户名密码
        usr_name = self.var_usr_name.get()
        usr_pwd = self.login_pwd or self.var_usr_pwd.get()
        # 判断用户名和密码是否匹配
        if usr_name in self.account_datas:
            if usr_pwd == self.account_datas[usr_name]:
                self.hide()
                self.main_page()
                self.lv = ListView(self.window_main_page, x=130, y=40, width=800, height=600)
                self.lv.add_column('账号', 100)
                self.lv.add_column('用户名', 100)
                self.lv.create_listview()
                self.update_text_box_data()
            else:
                tk.messagebox.showerror(message='密码错误')
        # 用户名密码不能为空
        elif usr_name == '' or usr_pwd == '':
            tk.messagebox.showerror(message='用户名或密码为空')

    def update_text_box_data(self):
        for k,v in self.user_datas_info.items():
            row = [v.get('nickname'), v.get('username')]
            self.lv.add_row(True, row)
            self.insert_data_list.append(k)

    # 登录成功主页面
    def main_page(self):
        # 确认存储时的相应函数
        def save_data():
            # 获取数据
            user_name_str = self.add_user_name.get()
            nick_name_str = self.add_nick_name.get()
            user_pwd_str = self.add_user_pwd.get()
            # user_pwd_str = self.tmp_pwd.get()

            if not user_name_str and not nick_name_str and not user_pwd_str:
                return

            # 检查是否已经有该信息
            item_key = self.cal_hash("{}{}{}".format(user_name_str, nick_name_str, user_pwd_str))
            if item_key in self.user_datas_info:
                if self.user_datas_info[item_key].get('nickname') == nick_name_str:
                    if self.user_datas_info[item_key].get('pwd') == user_pwd_str:
                        tk.messagebox.showinfo("提示", '该信息已存在')
                    else:
                        var_bool = tk.messagebox.askyesno(title='系统提示', message='用户和账号已经存在，是否需要更新密码')
                        if var_bool:
                            #更新密码
                            self.add_user_data(user_name_str, nick_name_str, user_pwd_str)
                        else:
                            #不更新密码，什么都不做
                            pass
            else:
                self.add_user_data(user_name_str, nick_name_str, user_pwd_str)
                self.lv.add_row(True, [nick_name_str, user_name_str])
            self.add_data_page.destroy()

        def pwd_page_ok():
            """
            销毁窗口
            :return:
            """
            self.pwd_page.destroy()
            save_data()

        def add_secret():
            """
            添加密码
            :return:
            """
            self.pwd_page = tk.Toplevel(self.window_main_page)
            self.pwd_page.geometry('250x200')
            self.pwd_page.title('添加密码')

            self.tmp_pwd = tk.StringVar()
            tk.Label(self.pwd_page, text='密码 ：').place(x=10, y=30)
            tk.Entry(self.pwd_page, textvariable=self.tmp_pwd, width=20).place(x=40, y=30)

            # 确定按钮
            pwd_confirm_ok = tk.Button(self.pwd_page, text='确定', command=pwd_page_ok, width=10)
            pwd_confirm_ok.place(x=80, y=130)

        def update_data():
            select_index = int(self.lv.get_index_select())
            data_info = self.user_datas_info.get(self.insert_data_list[select_index-1], {})
            self.tmp_data = data_info
            self.tmp_index = select_index
            if data_info:
                self.info_page = tk.Toplevel(self.window_main_page)
                self.info_page.geometry('300x300')
                self.info_page.title('修改')

                row1 = tk.Frame(self.info_page)
                row1.pack(fill="x")
                tk.Label(row1, text='用户名：', width=8).pack(side=tk.LEFT)
                self.s1 = tk.StringVar()
                self.s1.set(data_info.get('username'))
                tk.Entry(row1, textvariable=self.s1, width=20).pack(side=tk.LEFT)

                row2 = tk.Frame(self.info_page)
                row2.pack(fill="x")
                tk.Label(row2, text='账号名：', width=8).pack(side=tk.LEFT)
                self.s2 = tk.StringVar()
                self.s2.set(data_info.get('nickname'))
                tk.Entry(row2, textvariable=self.s2, width=20).pack(side=tk.LEFT)

                row3 = tk.Frame(self.info_page)
                row3.pack(fill="x")
                tk.Label(row3, text='密码：', width=8).pack(side=tk.LEFT)
                self.s3 = tk.StringVar()
                self.s3.set(data_info.get('pwd'))
                tk.Entry(row3, textvariable=self.s3, width=20).pack(side=tk.LEFT)

                row4 = tk.Frame(self.info_page)
                row4.pack(fill="x")
                tk.Button(row4, text="取消", command=update_cancel).pack(side=tk.RIGHT)
                tk.Button(row4, text="确定", command=update_ok).pack(side=tk.RIGHT)

        def update_ok():
            if self.tmp_data:
                if self.tmp_data.get('username') != self.s1.get() or \
                    self.tmp_data.get('nickname') != self.s2.get() or \
                        self.tmp_data.get('pwd') != self.s3.get():
                    self.user_datas_info.pop(self.insert_data_list[self.tmp_index - 1])
                    self.insert_data_list.pop(self.tmp_index - 1)

                    self.lv.delete_row(self.tmp_index)
                    self.save_user_data()

                    self.add_user_data(self.s1.get(), self.s2.get(), self.s3.get())
                    self.lv.add_row(True, [self.s2.get(), self.s1.get()])
                    self.info_page.destroy()

        def update_cancel():
            self.info_page.destroy()

        def update_label(v):
            if self.s3_button_index % 2 == 1:
                self.s3.set("*"*len(self.item_data_info.get('pwd')))
            else:
                self.s3.set(self.item_data_info.get('pwd'))
            self.s3_button_index += 1

        def query_data():
            select_index = int(self.lv.get_index_select())
            self.item_data_info = self.user_datas_info.get(self.insert_data_list[select_index-1], {})
            if self.item_data_info:
                self.info_page = tk.Toplevel(self.window_main_page)
                self.info_page.geometry('300x300')
                self.info_page.title('查询')

                row1 = tk.Frame(self.info_page)
                row1.pack(fill="x")
                tk.Label(row1, text='用户名：', width=8).pack(side=tk.LEFT)
                self.s1 = tk.StringVar()
                self.s1.set(self.item_data_info.get('username'))
                tk.Entry(row1, textvariable=self.s1, width=20, state=tk.DISABLED).pack(side=tk.LEFT)

                row2 = tk.Frame(self.info_page)
                row2.pack(fill="x")
                tk.Label(row2, text='账号名：', width=8).pack(side=tk.LEFT)
                self.s2 = tk.StringVar()
                self.s2.set(self.item_data_info.get('nickname'))
                tk.Entry(row2, textvariable=self.s2, width=20, state=tk.DISABLED).pack(side=tk.LEFT)

                row3 = tk.Frame(self.info_page)
                row3.pack(fill="x")
                tk.Label(row3, text='密码：', width=8).pack(side=tk.LEFT)
                self.s3_button_index = 1
                self.s3 = tk.StringVar()
                self.s3.set(self.item_data_info.get('pwd'))
                self.box3 = tk.Entry(row3, textvariable=self.s3, width=20, state=tk.DISABLED)
                self.box3.bind('<Button-1>', update_label)
                self.box3.pack(side=tk.LEFT)

        def del_data():
            select_index = int(self.lv.get_index_select())
            self.user_datas_info.pop(self.insert_data_list[select_index - 1])
            self.insert_data_list.pop(select_index - 1)

            self.lv.delete_row(int(self.lv.get_index_select()))
            self.save_user_data()

        def add_item_data():
            self.add_data_page = tk.Toplevel(self.window_main_page)
            self.add_data_page.geometry('400x300')
            self.add_data_page.title('添加')

            # 用户名变量及标签、输入框
            self.add_user_name = tk.StringVar()
            tk.Label(self.add_data_page, text='用户名：').place(x=10, y=10)
            tk.Entry(self.add_data_page, textvariable=self.add_user_name, width=20).place(x=130, y=10)
            # 账号名变量及标签、输入框
            self.add_nick_name = tk.StringVar()
            tk.Label(self.add_data_page, text='账号名：').place(x=10, y=50)
            tk.Entry(self.add_data_page, textvariable=self.add_nick_name, width=20).place(x=130, y=50)
            # 密码变量及标签、输入框
            self.add_user_pwd = tk.StringVar()
            tk.Label(self.add_data_page, text='密码 ：').place(x=10, y=90)
            tk.Entry(self.add_data_page, textvariable=self.add_user_pwd, width=20).place(x=130, y=90)

            # 存储按钮及位置
            bt_confirm_sign_up = tk.Button(self.add_data_page, text='存储', command=save_data, width=30)
            bt_confirm_sign_up.place(x=90, y=130)

        # 操作主界面
        self.window_main_page = tk.Toplevel(self.window)
        self.window_main_page.geometry('500x400')
        self.window_main_page.title('主页面')
        # # 用户名变量及标签、输入框
        # user_name = tk.StringVar()
        # tk.Label(self.window_main_page, text='用户名：').place(x=10, y=10)
        # tk.Entry(self.window_main_page, textvariable=user_name, width=20).place(x=130, y=10)
        # # 账号名变量及标签、输入框
        # nick_name = tk.StringVar()
        # tk.Label(self.window_main_page, text='账号名：').place(x=10, y=50)
        # tk.Entry(self.window_main_page, textvariable=nick_name, width=20).place(x=130, y=50)
        # # 密码变量及标签、输入框
        # user_pwd = tk.StringVar()
        # tk.Label(self.window_main_page, text='密码 ：').place(x=10, y=90)
        # tk.Entry(self.window_main_page, textvariable=user_pwd, show='*', width=20).place(x=130, y=90)
        #
        tk.Label(self.window_main_page, text='已存储账号信息：').place(x=10, y=40)

        # # 存储按钮及位置
        # bt_confirm_sign_up = tk.Button(self.window_main_page, text='添加密码并存储', command=save_data, width=30)
        # bt_confirm_sign_up.place(x=130, y=90)

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

    # 退出的函数
    def usr_sign_quit(self):
        self.window.destroy()


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


if __name__ == '__main__':
    app = App()
    app.init()
    app.run()

