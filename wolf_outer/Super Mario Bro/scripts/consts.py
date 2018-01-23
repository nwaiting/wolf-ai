# -*- coding: utf-8 -*-
WIDTH = 512         #屏幕宽度
HEIGHT = 480        #屏幕高度
SIZE = 32           #单位方格边长
BOUNCE = 13.6       #主角跳跃时的初速度 10
SMALL_BOUNCE = 9    #主角踩到怪物时弹起的初速度 8
SPEED = 5           #主角移动的最大速度 4
FALL_SPEED = 20     #下落的最大速度
ITEM_SPEED = 3      #道具移动的速度
ENEMY_SPEED = 1.6   #怪物移动的速度
ACCEL = 15.0        #主角加速到最大速度所需时间（浮点型） 10.0
JUMP_TIME = 8       #主角长跳的最大时间 10
HERO_RATE = 12      #主角移速与帧速的比率
ENEMY_RATE = 10     #怪物移速与帧速的比率
COMBO_TIME = 15     #主角连续得分的时间 20
FLOWER_WIDTH = 10   #花宽度减小的判定范围
FLOWER_HEIGHT = 20  #花高度减小的判定范围
INVIN_TIME = 45     #主角变小后短暂的无敌时间 60
INTERVAL = 0.03     #画面更新速率 0.03
G = 2               #重力加速度 1
INIT_POS = -100     #图片创建的位置

MAP = "./maps/map1-1"

AUDIO = "./assets/audios/"
BGM = "Bgm.wav"
DIE = "Player Down.wav"
LOSE = "Game Over.wav"
WIN = "Course Clear.wav"
CLIMB = "Pull.wav"
JUMP = ["Jump.wav","Big Jump.wav"]
GET_COIN = "Coin.wav"
APP_LARGE = "Large.wav"
GET_LARGE = "Grow.wav"
TREAD = "Tread.wav"
EMPTY = "Empty.wav"

IMAGE = "./assets/images/"
COIN = ["coin_0.gif","coin_1.gif","coin_2.gif","coin_3.gif"]
ITEM = ["item_0.gif","item_1.gif","item_2.gif","item_3.gif"]
LARGE = ["large_0.gif","large_1.gif"]
WALL = ["wall.gif","ground.gif"]
BLOCK = ["block.gif","blockt.gif","blockn.gif","blockx.gif"]
TUBE = [["tube_v0.gif","tube_v1.gif","tube_v2.gif"],
        ["tube_h0.gif","tube_h1.gif","tube_h2.gif"]]
MUSHROOM = ["mushroom_r0.gif","mushroom_r1.gif",
            "mushroom_r0.gif","mushroom_r1.gif",
            "mushroom_t.gif","mushroom_d.gif",]
TORTOISE = ["tortoise_lr0.gif","tortoise_lr1.gif",
            "tortoise_rr0.gif","tortoise_rr1.gif",
            "tortoise_h.gif","tortoise_d.gif",]
RED_TORTOISE = ["red_tortoise_lr0.gif","red_tortoise_lr1.gif",
                "red_tortoise_rr0.gif","red_tortoise_rr1.gif",
                "red_tortoise_h.gif","red_tortoise_d.gif",]
FLOWER = ["flower_0.gif","flower_1.gif"]
FROG = ["frog_lr0.gif","frog_lr1.gif",
        "frog_rr0.gif","frog_rr1.gif",
        "frog_lj.gif","frog_rj.gif"]
HERO = ["hero_ls.gif","hero_lj.gif",
        "hero_lr0.gif","hero_lr1.gif","hero_lr2.gif","hero_lr1.gif",
        "hero_lc0.gif","hero_lc1.gif","hero_d.gif",
        "hero_rs.gif","hero_rj.gif",
        "hero_rr0.gif","hero_rr1.gif","hero_rr2.gif","hero_rr1.gif",
        "hero_rc0.gif","hero_rc1.gif","hero_d.gif",
        "hero_lsl.gif","hero_ljl.gif",
        "hero_lr0l.gif","hero_lr1l.gif","hero_lr2l.gif","hero_lr1l.gif",
        "hero_lc0l.gif","hero_lc1l.gif","hero_ldl.gif",
        "hero_rsl.gif","hero_rjl.gif",
        "hero_rr0l.gif","hero_rr1l.gif","hero_rr2l.gif","hero_rr1l.gif",
        "hero_rc0l.gif","hero_rc1l.gif","hero_rdl.gif"]
FLAG = ["pole.gif","flag_l.gif","flag_r.gif"]
PIECES = ["piece_0.gif","piece_1.gif"]
CASTLE = "castle.gif"
CAS_FLAG = "castle_flag.gif"
CLOUD = ["cloud_0.gif","cloud_1.gif","cloud_2.gif"]
MOUNT = ["mount_0.gif","mount_1.gif","bush_0.gif","bush_1.gif","bush_2.gif"]
CLOUD_POS = ((278,86,0),(626,50,0),(882,82,2),(1170,50,1),(1808,86,0))
MOUNT_POS = ((2,0),(13,4),(17,1),(24,2),(42.5,3),(50,0))
SYM = ["icon_0.gif","icon_1.gif","icon_2.gif","icon_1.gif"]
BG = {"bright":"#6b8cff","dark":"#000000"}
