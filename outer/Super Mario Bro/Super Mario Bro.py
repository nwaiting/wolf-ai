# -*- coding: utf-8 -*-
import sys
sys.path.append("scripts")
sys.path.append("ball")
import game,ball
from consts import *
from tkinter import *
from tkinter.messagebox import *
from time import sleep

def onClick():
    label.forget()
    value = game.main(root)
    if value:
        f = open("save", 'r')
        score, coin = list(map(int, f.readline().split()))
        score, coin = max(score, value[0]), max(coin, value[1])
        f = open("save", 'w')
        f.write("%d %d" %(score, coin))
        f.close()
        label.pack()
        displayRecord(score)
        
def onPlay():
    label.forget()
    if ball.main(root):
        root.geometry("%dx%d" %(WIDTH,HEIGHT))
        label.pack()

def onQuit():
    alpha = 1
    while alpha > 0:
        sleep(INTERVAL)
        alpha -= 0.05
        root.attributes("-alpha", alpha)
    root.destroy()

def displayRecord(score):
    record["text"] = "TOP - %06d" %score

def main():
    global root, label, img, record
    root = Tk()
    root.geometry("%dx%d" %(WIDTH, HEIGHT))
    root.title("Super Mario Bro")
    root.iconbitmap("icon.ico")
    img = PhotoImage(file = "assets/images/menu.gif")
    label = Label(root, width = WIDTH, height = HEIGHT, image=img)
    label.pack()
    try:
        Button(label, text = "START GAME", relief = FLAT,
               command = onClick, bg = BG["bright"], fg = "#ffffff",
               font = ("Fixedsys", 24, "bold")).\
               place(relx = 0.5, rely = 0.7, anchor = S)
        Button(label, text = "MORE", relief = FLAT,
               command = onPlay, bg = BG["bright"], fg = "#ffffff",
               font = ("Fixedsys", 24, "bold")).\
               place(relx = 0.8, rely = 0.7, anchor = S)
        Button(label, text = "END GAME", relief = FLAT, 
               command = onQuit, bg = BG["bright"], fg = "#ffffff",
               font = ("Fixedsys", 24, "bold")).\
               place(relx = 0.5, rely = 0.8, anchor = S)
        record = Label(label, text = "", bg = BG["bright"],  fg = "#ffffff",
                       font = ("Fixedsys", 18, "bold"))
    except:
        showwarning("Error","字体文件Fixedsys缺失，请安装font.fnt")
        root.destroy()
        return
    record.place(relx = 0.5, rely = 0.85, anchor = S)
    displayRecord(int(open("save", 'r').readline().split()[0]))
    root.mainloop()

main()
