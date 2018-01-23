#coding=utf-8

import random, time, pygame, sys
from pygame.locals import *


#设置屏幕刷新率
FPS = 25
# 设置窗口宽度
WINDOWWIDTH = 640
# 设置窗口高度
WINDOWHEIGHT = 480
# 方格大小
BOXSIZE = 20
# 放置俄罗斯方块窗口的大小
BOARDWIDTH = 10
BOARDHEIGHT = 20
# 代表空的形状
BLANK = '.'
# 若一直按下方向左键或右键那么每0.15秒方块才会继续移动
MOVESIDEWAYSFREQ = 0.15
# 向下的频率
MOVEDOWNFREQ = 0.1
# x方向的边距
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
# 距离窗口顶部的边距
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

# 定义颜色
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)
BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY

COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)

# 断言 每一个颜色都应该对应有亮色
assert len(COLORS) == len(LIGHTCOLORS)

# 模板的宽高
TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

# 形状_S（S旋转有2种）
S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

# 形状_Z（Z旋转有2种）
Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

# 形状_I（I旋转有2种）
I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

# 形状_O（O旋转只有一个）
O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

# 形状_J（J旋转有4种）
J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

# 形状_L（L旋转有4种）
L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

# 形状_T（T旋转有4种）
T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

# 定义一个数据结构存储对应的形状
PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

# 绘制提示信息，下一个Piece
def drawNextPiece(piece):
    # 绘制"Next"文本
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # 绘制NextPiece
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)

# 绘制各种形状Piece（S,Z,I,O,J,L,T）
def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # 若pixelx、pixely没有被指定，则使用piece数据结构中存储的位置
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # 绘制组成Piece的每个Box
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

# 绘制游戏分数、等级信息
def drawStatus(score, level):
    # 绘制分数文本
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # 绘制等级文本
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)

# 绘制Board
def drawBoard(board):
    # 绘制Board边框
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)
    # 绘制Board背景
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # 绘制Board中的Box
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

# 绘制Box
def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # 使用Board的坐标绘制单个Box（一个Piece含有4个Box），若像素坐标pixelx、pixely被指定，则直接使用像素坐标（用于NextPiece区域）
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

# 根据Board的坐标转化成像素坐标
def convertToPixelCoords(boxx, boxy):
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

# 运行游戏
def runGame():

    # 在游戏开始前初始化变量
    # 获得一个空的board
    board = getBlankBoard()

    # 最后向下移动的时刻
    lastMoveDownTime = time.time()

    # 最后侧向移动的时刻
    lastMoveSidewaysTime = time.time()

    # 最后的下降时间
    lastFallTime = time.time()

    # 是否可以  向下，向左，向右
    # 注意:这里没有向上可用
    movingDown = False
    movingLeft = False
    movingRight = False

    # 分数
    score = 0

    # 根据分数计算等级和下降的频率
    level, fallFreq = calculateLevelAndFallFreq(score)

    # 获得新的形状（当前的形状）
    fallingPiece = getNewPiece()

    # 获得下一个形状
    nextPiece = getNewPiece()

    # 游戏循环体
    while True:

        # 当前没有下降的形状
        if fallingPiece == None:
            # 重新获得新的形状和下一个形状
            fallingPiece = nextPiece
            nextPiece = getNewPiece()

            # 重置最后下降的时间
            lastFallTime = time.time()

            # 判断界面上是否还有空位（方块是否到顶），没有则结束游戏
            if not isValidPosition(board, fallingPiece):
                return

        # 检查是否有退出事件
        checkForQuit()

        # 事件处理循环
        for event in pygame.event.get():
            # KEYUP事件处理
            if event.type == KEYUP:
                # 用户按P键暂停
                if (event.key == K_p):
                    DISPLAYSURF.fill(BGCOLOR)
                    #停止音乐
                    pygame.mixer.music.stop()

                    # 显示暂停界面，直到按任意键继续
                    showTextScreen('Paused')

                    #因实验楼中暂时无法播放音频，故将此段代码注释，同学们可以在自己的电脑上尝试播放
                    # 继续循环音乐
                    #pygame.mixer.music.play(-1, 0.0)

                    # 重置各种时间
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False

            # KEYDOWN事件处理
            elif event.type == KEYDOWN:

                # 左右移动piece
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # UP或W键 旋转piece (在有空间旋转的前提下)
                # 正向旋转
                elif (event.key == K_UP or event.key == K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                # Q键，反向旋转
                elif (event.key == K_q):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                # DOWN或S键 使piece下降得更快
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # 空格键，直接下降到最下面且可用的地方
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        # 根据记录的用户输入方向的变量来移动piece
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # 自动下降piece
        if time.time() - lastFallTime > fallFreq:
            if not isValidPosition(board, fallingPiece, adjY=1):
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # 绘制屏幕上的所有东西
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

# 根据分数来计算等级和下落的频率
def calculateLevelAndFallFreq(score):

    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

# 检查每一行，移除完成填满的一行，将这一行上面的所有的都下降一行，返回完成填满的总行数
def removeCompleteLines(board):
    numLinesRemoved = 0
    # 从-1开始从下往上检查每一行
    y = BOARDHEIGHT - 1
    while y >= 0:
        if isCompleteLine(board, y):
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
        else:
            y -= 1
    return numLinesRemoved

# 判断当前的这行是否被全部填满
def isCompleteLine(board, y):
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True

# Piece在当前的Board里是否是一个合法可用的位置
def isValidPosition(board, piece, adjX=0, adjY=0):
    # 若Piece在Board内并且无碰撞，则返回True
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

# Board边界
def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

# 将一个Piece添加到Board中
def addToBoard(board, piece):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']

# 随机获得一个新的Piece（形状，方向，颜色）
def getNewPiece():
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2), # x居中
                'y': -2, # y在屏幕的上方，小于0
                'color': random.randint(0, len(COLORS)-1)}
    return newPiece

# 清空Board
def getBlankBoard():
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

# 显示开始、暂停、结束画面
def showTextScreen(text):
    # 这个函数用于在屏幕中央显示大文本，直到按下任意键
    # 绘制文字阴影
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # 绘制文字
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # 绘制额外的"Press a key to play."文字
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

# 创建文本绘制对象
def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

# 检查是否有按键被按下
def checkForKeyPress():
    # 通过事件队列寻找KEYUP事件
    # 从事件队列删除KEYDOWN事件
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

# 检查是否有退出事件
def checkForQuit():

    # 获得所有QUIT事件
    for event in pygame.event.get(QUIT):
        # 若存在任何QUIT事件，则终止
        terminate()
    # 获得所有KEYUP事件
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            # 若KEYUP事件是Esc键，则终止
            terminate()
        # 把其他的KEYUP事件对象放回来
        pygame.event.post(event)

# 退出
def terminate():
    pygame.quit()
    sys.exit()

def main():
    # 定义全局变量
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    # 初始化pygame
    pygame.init()
    # 获得pygame时钟
    FPSCLOCK = pygame.time.Clock()
    # 设置窗口
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # 设置基础的字体
    BASICFONT = pygame.font.Font('./outer/snake/arial.ttf', 18)
    # 设置大字体
    BIGFONT = pygame.font.Font('./outer/snake/arial.ttf', 100)
    # 窗口标题
    pygame.display.set_caption('Tetris')
    # 显示开始画面
    showTextScreen('Tetris')

    # 游戏主循环
    while True:

    #因实验楼中暂时无法播放音频，故将此段代码注释，同学们可以在自己的电脑上尝试播放
            # 二选一随机播放背景音乐
    #        if random.randint(0, 1) == 0:
    #            pygame.mixer.music.load('resources/tetrisb.mid')
    #        else:
    #            pygame.mixer.music.load('resources/tetrisc.mid')
    #        pygame.mixer.music.play(-1, 0.0)

        # 运行游戏
        runGame()
        # 退出游戏后，结束播放音乐
        pygame.mixer.music.stop()
        # 显示结束画面
        showTextScreen('Game Over')

if __name__ == "__main__":
    main()
