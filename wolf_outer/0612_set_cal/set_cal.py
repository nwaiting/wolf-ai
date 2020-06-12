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
        self.window.title('集合系统')
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


if __name__ == '__main__':
    app = App()
    app.init()
    app.run()

