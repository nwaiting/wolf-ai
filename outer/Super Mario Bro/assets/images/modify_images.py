#coding=utf-8
from PIL import Image
import os
def rename(names,newNames):
    for name,newName in zip(names,newNames):
        Image.open(name).save(newName)
        os.remove(name)
def flip(names):
    for name in names:
        Image.open(name).transpose(Image.FLIP_LEFT_RIGHT).save(name[:-4]+"_f.gif")
        
##def main():
##    names = ['','','','','','r0','r1','r2','u','j','d','s','c0','c1']
##    img = Image.open("mario_bros.gif")
##    for i in range(5,14):
##        new = img.crop((i*16,18*16,(i+1)*16,20*16)).resize((32,64))
##        new.save("new/hero_r%sl.gif" %(names[i]))
##        new.transpose(Image.FLIP_LEFT_RIGHT).save("new/hero_l%sl.gif" %(names[i]))
##main()
def main():
    img = Image.open("tile_set.gif")
    for i in range(1):
        new = img.crop((i*16,48,(i+1)*16,64)).resize((32,32))
        new.save("new/wall.gif")
main()
