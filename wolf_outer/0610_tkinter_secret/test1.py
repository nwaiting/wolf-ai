from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfile
import threading
import time

'''from ctypes import *
sum = CDLL('/home/manjunath/libsum.so')  #UTF-8 to UNICODE
sum.our_function.argtypes = [c_int, c_char_p]
sum.our_function.restype = c_char_p
'''


def about():
    filewin = Toplevel(root)
    string = "This is a small text editor built using Tkinter a python which supports GUI programming\n"
    string += "This text editor unlike many others supports many functions like giving suggestions based on your previous data \n"
    string += "Small, easy to use and works like the future of text editors \n"
    button = Label(filewin, text=string)
    button.pack()


def open_file():
    global text, save_file_id
    open_file_loc = askopenfilename()
    open_file = open(open_file_loc, 'r')
    text.delete(1.0, END)
    text.insert(END, open_file.read())
    save_file_id = open_file_loc


def save_as_file():
    global text, save_file_id
    name = asksaveasfile(mode='w', defaultextension=".txt")
    text2save = str(text.get(0.0, END))
    name.write(text2save)
    name = str(name)[(str(name).find("name='") + 6):str(name).find("'", (str(name).find("name='") + 6))]
    save_file_id = name


def save_file():
    global text, save_file_id
    if save_file_id == "":
        save_as_file()
    else:
        with open(save_file_id, 'w') as f:
            f.write(text.get(0.0, END))


def New_file():
    text.delete(1.0, END)
    save_file_id = ' '


def find_destroy():
    text.tag_remove(keyword, 0.0, END)
    search_box.destroy()
    label1.destroy()
    button1.destroy()
    button2.destroy()


def find_button():
    global search_box, label1, button1, button2
    label1 = Label(text="						")
    label1.pack(side=LEFT)
    search_box = Text(root, height=1, width=20)
    search_box.pack(side=LEFT)
    button1 = Button(root, text="find", command=Find)
    button1.pack(side=LEFT)
    button2 = Button(root, text="X", command=find_destroy)
    button2.pack(side=LEFT)


def Find():
    global keyword
    keyword = search_box.get(0.0, END)
    text_box = text.get(0.0, END)
    text.tag_config(keyword, background='lightblue')
    i = j = i_p = 0
    row = 1
    n = 0
    while i < len(text_box):
        if (text_box[i] == keyword[j]):
            i_p = i - n
            while (text_box[i] == keyword[j]) and (j < len(keyword) - 1):
                j += 1
                i += 1
            i -= 1
            if j == len(keyword) - 1:
                i -= 1
        if j == len(keyword) - 1:
            pos_start = str(row) + "." + str(i_p)
            pos_end = '{}+{}c'.format(pos_start, len(keyword) - 1)
            # print(pos_start,pos_end)
            text.tag_add(keyword, pos_start, pos_end)

        if text_box[i] == '\n':
            n = i + 1
            row += 1
            i_p = 0
        j = 0
        i += 1


def replace_button():
    global search_box, button2, replace_box, label1, label2
    label1 = Label(text="Find")
    label1.pack(side=LEFT)
    search_box = Text(root, height=1, width=20)
    search_box.pack(side=LEFT)
    label2 = Label(text="	Replace")
    label2.pack(side=LEFT)
    replace_box = Text(root, height=1, width=20)
    replace_box.pack(side=LEFT)
    button2 = Button(root, text="Replace", command=Replace)
    button2.pack(side=LEFT)


def Replace():
    keyword = search_box.get(0.0, END)
    replace_word = replace_box.get(0.0, END)
    text_box = text.get(0.0, END)
    q = 0
    while q < len(text_box):
        i = j = i_p = n = 0
        row = 1
        while i < len(text_box):
            if (text_box[i] == keyword[j]):
                i_p = i - n
                while (text_box[i] == keyword[j]) and (j < len(keyword) - 1):
                    j += 1
                    i += 1
                i -= 1
                if j == len(keyword) - 1:
                    i -= 1
            if j == len(keyword) - 1:
                pos_start = str(row) + "." + str(i_p)
                pos_end = '{}+{}c'.format(pos_start, len(keyword) - 1)
                replace_start = '{}+{}c'.format(pos_start, len(replace_word) - 1)
                replace_end = '{}+{}c'.format(pos_start, len(replace_word))
                text.delete(pos_start, pos_end)
                text.insert(pos_start, replace_word)
                text.delete(replace_start, replace_end)
                break

            if text_box[i] == '\n':
                n = i + 1
                row += 1
                i_p = 0
            j = 0
            i += 1
        q += 1
        text_box = text.get(0.0, END)

    label1.destroy()
    label2.destroy()
    replace_box.destroy()
    button2.destroy()
    search_box.destroy()


def undo():
    global undo_list, text
    text = undo_list.pop()


def heapify(match_list, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    if l < n and match_list[i] < match_list[l]:
        largest = l

    if r < n and match_list[largest] < match_list[r]:
        largest = r

    # Change root, if needed
    if largest != i:
        match_list[i], match_list[largest] = match_list[largest], match_list[i]  # swap

        heapify(match_list, n, largest)


def heapSort(match_list):
    n = len(match_list)
    # Build a maxheap.
    for i in range(n, -1, -1):
        heapify(match_list, n, i)
    # One by one extract elements
    for i in range(n - 1, 0, -1):
        match_list[i], match_list[0] = match_list[0], match_list[i]  # swap
        heapify(match_list, i, 0)


def drop_suggest(*args):
    var_value = var.get()
    global Text
    txt = ''
    i = len(txt) - 1
    for i in text_list:
        txt += i + ' '
    txt += var.get()
    text.delete(0.0, END)
    text.insert(0.0, txt)
    w.destroy()


def suggest():
    global text, var, text_list, w
    text_list = text.get(0.0, END).split(" ")
    last_word = text_list.pop()
    last_word = last_word[:-1]
    fp = open("dictionary.txt", "a+")
    for i in text_list:
        fp.write(i + ' ')

    match_list = []
    fp.seek(0)
    for i in fp.read().split(" "):
        if '\n' in i:
            v = i.split("\n")
            for k in v:
                if k is not '':
                    match_list.append(k)
            continue
        if last_word in i:
            match_list.append(i)
    match_list = list(set(match_list))
    var = StringVar(root)
    if len(match_list) != 0:
        heapSort(match_list)
        var.set(match_list[0])
        var.trace('w', drop_suggest)
        w = OptionMenu(root, var, *match_list)
        w.pack()
    fp.close()


def drop_style(*args):
    txt = text.get(0.0, END)
    text.delete(0.0, END)
    text.configure(font=(var.get(), text_size))
    text.insert(0.0, txt)
    w.destroy()


def font_style():
    global text, var, w
    var = StringVar(root)
    var.set(text_style)
    match_list = ["Times New Roman", "Helvetica", "Ariel", "Courier", "Symbol"]
    var.trace('w', drop_style)
    w = OptionMenu(root, var, *match_list)
    w.pack()


def drop_size(*args):
    txt = text.get(0.0, END)
    text.delete(0.0, END)
    text.configure(font=(text_style, var.get()))
    text.insert(0.0, txt)
    w.destroy()


def font_size():
    global var, w
    var = StringVar(root)
    var.set(text_size)
    match_list = [8, 10, 11, 12, 14]
    var.trace('w', drop_size)
    w = OptionMenu(root, var, *match_list)
    w.pack()


root = Tk()
root.title("jotter")

text = Text(root, width=200, undo=True)
text_size = 11
text_style = "Times New Roman"
text.configure(font=(text_style, text_size))
text.pack()
save_file_id = ""

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=New_file)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", command=save_file)
filemenu.add_command(label="Save as...", command=save_as_file)
filemenu.add_command(label="Exit", command=root.quit)

Editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=Editmenu)
Editmenu.add_command(label="Font Style", command=font_style)
Editmenu.add_command(label="Font Size", command=font_size)

Searchmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Search", menu=Searchmenu)
Searchmenu.add_command(label="Suggest", command=suggest)
Searchmenu.add_command(label="Find", command=find_button)
Searchmenu.add_command(label="Find and Replace", command=replace_button)

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about)

root.config(menu=menubar)
root.mainloop()

'''def our_function(numbers):
  num_numbers = len(numbers)
  #array_type = c_char_p(numbers)
  #print(type(array_type))
  _result = sum.our_function(num_numbers,numbers)
  return(_result.value)
print(our_function("abc"))
'''