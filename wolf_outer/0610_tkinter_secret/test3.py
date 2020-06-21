#! /usr/env/python

import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext


class TextEditor:

    def __init__(self, title="Just another Text Editor", width=100, height=60):
        """Initialises the TextEditor Class
        Return nothing"""
        self.root = tkinter.Tk(className=title)
        self.textPad = scrolledtext.ScrolledText(self.root, width=width, height=height)
        self.currentFile = ""
        self.errorMessage = ""
        self.errorNumber = 0

    def setError(self, number=None, message=None):
        if (number == None or message == None):
            print("You have error in your Error Setting"
                  "code!")  # for debug ;)
        self.errorNumber = number
        self.errorMessage = message

    def getLastError(self):
        ret = {'number': self.errorNumber, 'message': self.errorMessage}
        return ret

    def open_command(self, path=None):
        if (self.compareFileWithCurrentText(self.currentFile) == False):
            if (self.saveBeforeContinue() == False):
                return  # no open command invoked
        self.textPad.delete('1.0', END)
        if path != None:
            pass
            f = open(path, 'rb')
            self.textPad.insert('1.0', f.read())
            return
        file = tkinter.filedialog.askopenfile(parent=self.root, mode='rb', title='Select File to open')
        if file != None:
            self.currentFile = file.name
            print(self.currentFile, " opened")
            contents = file.read()
            self.textPad.insert('1.0', contents)
            file.close()

    def new_command(self):
        if (self.compareFileWithCurrentText(self.currentFile) == False):
            if (self.saveBeforeContinue() == False):
                return  # no new command invoked
        pass  # clear textPad
        self.textPad.insert('1.0', '')
        pass  # set currentFile = none
        pass  # and open that.

    def saveBeforeContinue(self):
        guide = tkinter.messagebox.askyesnocancel("Save Before Continue?",
                                                  "Do you want to save the file b"
                                                  "efore continuing?")
        if (guide == True):
            file = tkinter.filedialog.asksaveasfile()
            if file != None:
                data = self.textPad.get('1.0', END)
                file.write(data)
                file.close()
            return True
        elif (guide == None):
            return False
        else:
            return True

    def save_command(self):
        file = tkinter.filedialog.asksaveasfile()
        if file != None:
            self.currentFile = file.name
            data = self.textPad.get('1.0', END)
            data = self.stripNewLineAtTheEnd(data)
            file.write(data)
            file.close()

    def exit_command(self):
        if tkinter.messagebox.askokcancel("Really Quit!", "Are you sure, you'll leave us now?"):
            self.root.destroy()

    def about_command(self):
        label = tkinter.messagebox.showinfo("About we", "Just another text editor for ye!")

    def dummy(self):
        tkinter.messagebox.showinfo("Currently, This feature is not supported!")

    def compareFileWithCurrentText(self, file1=None):
        if (file1 == None):
            self.setError(number=1, message="Insuffiecient Argument")
            return
        try:
            f_h1 = open(file1)
        except:
            print("Cannot open previous file")
            if (self.textPad.get('1.0', END) == "\n"):  # checks if it it empty or not!
                return True  # no need to save
            print("File Contains some text. Possibly ask to save")
            return False  # no need to save
        t_d2 = self.textPad.get('1.0', END)
        t_d2 = self.stripNewLineAtTheEnd(t_d2)  # get gets extra newline
        f_d1 = f_h1.read()
        if (t_d2 == f_d1):
            # no need to save
            print("File Identical")
            return True  # means identical
        else:
            print("File not identical")
            # you must save now
            return False  # means Not-identical

    def stripNewlineAtTheEnd(self, string):
        if (string[:-1] == '\n'):
            return string[:-1]
        else:
            return string

    def mainloop(self):
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.new_command)
        self.filemenu.add_command(label="Open....", command=self.open_command)
        self.filemenu.add_command(label="Save", command=self.save_command)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit_command)
        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=self.about_command)
        self.textPad.pack(side="left", fill="both", expand=True)
        self.root.mainloop()


texteditor = TextEditor()
texteditor.mainloop()