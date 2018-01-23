#coding=utf8
#import tkSimpleDialog as dl
#import tkMessageBox as messagebox
from tkinter import *

#py2库名
#from Tkinter import *

def func0():
    """
    Tkinter
    py3以后更名为tkinter
    在使用时，经常要引入Tk常量库: form Tkconstants import *
    """

    r = Tk()
    li     = ['C','python','php','html','SQL','java']
    movie  = ['CSS','jQuery','Bootstrap']
    listb  = Listbox(r)
    listb2 = Listbox(r)
    for item in li:
        listb.insert(0,item)

    for item in movie:
        listb2.insert(0,item)

    listb.pack()
    listb2.pack()

    l1 = Label(r, text="xls:")
    l1.pack()
    xls_text = StringVar()
    print(xls_text.get())
    xls = Entry(r, textvariable = xls_text)
    xls_text.set(" ")
    xls.pack()

    def on_click():
        s = xls_text.get()
        print(s)
        messagebox.showinfo(title='aaa', message = str(s))

    Button(r, text="press", command = on_click).pack()

    r.mainloop()

def func1():
    def show_msg(*args):
        indexs = listbox1.curselection()
        index = int(indexs[0])
        listbox2.see(index)
        listbox2.select_set(index)

    root = Tk()
    root.title("listbox练习")
    #创建列表显示内容
    names = ("梅长苏","誉王","飞流","夏冬","霓凰郡主","蒙挚","萧景睿","谢玉")
    players = ("胡歌","黄维德","吴磊","张龄心","刘涛","陈龙","程皓枫","刘奕君")  # 刘奕君

    list1 = StringVar(value=names)
    list2 = StringVar(value=players)

    #创建两个Listbox，分别设置为单选、多选类型
    listbox1 = Listbox(root,height=len(names),listvariable=list1,selectmode="browse")
    listbox2 = Listbox(root,height=len(players),listvariable=list2,selectmode="extended")

    listbox1.grid(row=1,column=1,padx=(10,5),pady=10)
    listbox2.grid(row=1,column=2,padx=(5,10),pady=10)

    listbox1.select_set(4)
    # listbox2.select_set(1,5)

    #设置第二个表格的项目颜色等
    for i in range(len(players)):
        listbox2.itemconfig(i,fg="blue")
        if not i%2:
            listbox2.itemconfig(i,bg="#f0f0ff")

    #为第一个Listbox设置绑定事件
    listbox1.bind("<<ListboxSelect>>",show_msg)

    root.mainloop()

if __name__ == '__main__':
    func1()
