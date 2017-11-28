#coding=utf8
import tkSimpleDialog as dl
import tkMessageBox as messagebox
from Tkinter import *

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
print xls_text.get()
xls = Entry(r, textvariable = xls_text)
xls_text.set(" ")
xls.pack()

def on_click():
    s = xls_text.get()
    print s
    messagebox.showinfo(title='aaa', message = str(s))

Button(r, text="press", command = on_click).pack()

r.mainloop()
