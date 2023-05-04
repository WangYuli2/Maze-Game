import os.path
import pygame
import pygame as pg
import time
import random
import sys
import os
import tkinter.messagebox
import threading
import pygame.sprite
import cv2
import datetime
import numpy
from PIL import Image,ImageGrab
import tkinter.filedialog
import ScreenShotPyGameWindow
this_coin=0
this_lightning=0
pygame.mixer.init()
if not os.path.exists(os.getcwd()+"\\Maze_Game_conf_File\\ScreenShot"):
    os.makedirs(os.getcwd()+"\\Maze_Game_conf_File\\ScreenShot")
tkinter.messagebox.showinfo('重要提示','若代码出错，请删除此目录下的Maze_Game_conf_File文件夹重试即可。')
mapOfList=[]
for i in range(55,850-55,16):
    listA=[]
    for j in range(54,850-54,16):
        listA.append((i,j))
    mapOfList.append(listA)
# yes_=tkinter.messagebox.askyesno('习惯提示','是否在玩时显示“脚印”？')
yes_=True
# tkinter.messagebox.showinfo('操作提示','按↑↓←→/W-S-A-D（上下左右）操控角色（蓝色矩形），\n碰到红色终点后进入下一关，鼠标单击（左右键都可以）游戏屏幕即\n可显示/隐藏你走过的路线，按Q键/右上角×退出，按P键暂停游\n戏。')
sys.setrecursionlimit(100000)
get_level=0
pauses=0
pauses_time=[]
click_img=pygame.image.load('click.jpeg')
video = cv2.VideoCapture('show.mp4')
if not os.path.exists(os.getcwd()+'\\Maze_Game_conf_File'):
    get_lightning=0
    get_coin=0
    os.makedirs(os.getcwd()+'\\Maze_Game_conf_File')
if not os.path.exists(os.getcwd()+'\\Maze_Game_conf_File\\data.mgcf'):
    with open("Maze_Game_conf_File\\data.mgcf","w",encoding='utf-8') as f:
        f.write("")
else:
    if os.path.exists(os.getcwd()+"\\Maze_Game_conf_File\\data.mgcf"):
        with open("Maze_Game_conf_File\\data.mgcf","r",encoding='utf-8') as f:
            ff=f.readlines()
            if len(ff)!=0:
                get_coin=int(ff[0].rstrip("\n"))
                get_lightning=int(ff[1].rstrip("\n"))
            else:
                get_coin=0
                get_lightning=0
    else:
        get_coin=0
        get_lightning=0
MAZE_MAP = []
for i in range(800):
    MAZE_MAP.append([])
    for j in range(800):
        MAZE_MAP[i].append(0)
ListOfPlayInfo=[]
def update():
    if os.path.exists(os.getcwd()+"\\Maze_Game_conf_File\\data.mgcf"):
        with open("Maze_Game_conf_File\\data.mgcf","r",encoding='utf-8') as file:
            readlines=file.readlines()[2:]
        global ListOfPlayInfo
        num=0
        for i in range(len(readlines)):
            readlines[i]=readlines[i].rstrip("\n")
        while num<len(readlines):
            dict={}
            dict2={}
            list=[]
            name=readlines[num]
            num+=1
            dict2["Maze-Size"]=readlines[num]
            num+=1
            dict2["Level"]=readlines[num]
            num+=1
            dict2["Use-Times"]=readlines[num]
            num+=1
            dict2["Pause-Times"]=readlines[num]
            if dict2["Pause-Times"]!="0":
                for i in range(int(dict2["Pause-Times"])):
                    list.append(readlines[num+i+1])
            else:
                num+=1
            dict2["Pause-Time"]=list
            num+=1+int(dict2["Pause-Times"])
            dict2["Use-Steps"]=readlines[num]
            num+=1
            dict2["Get-Lightnings"]=readlines[num]
            num+=1
            dict2["Get-Coins"]=readlines[num]
            dict[name]=dict2
            num+=1
            dict2["New-Get-lightning"]=readlines[num]
            num+=1
            dict2["New-Get-Coins"]=readlines[num]
            num+=1
            dict2["Use-Money-Go"]=readlines[num]
            num+=1
            dict2["Get-Secret-Box"]=readlines[num]
            num+=1
            ListOfPlayInfo.append(dict)
    else:
        pass
def update_map():
    with open("Maze_Game_conf_File\\map.mgcf","r") as fileI:
        M=fileI.read()
    return eval(M)
def IMapMgCf():
    global screen
    with open("Maze_Game_conf_File\\map.mgcf","w") as fileIM:
        fileIM.write(str(pygame.PixelArray(screen)))
# video.set(CV_CAP_PROP_FOURCC, CV_FOURCC('M', 'J', 'P', 'G'))
# video.set(100000000, 1)
class Tile:
    def __init__(self, grid_size, screen_size, x, y):  # 主要是储存数据和绘制图形，与算法无关
        self.x, self.y = x, y
        self.connected = [0, 0, 0, 0]  # up,right,down,left 0 for not connected
        self.grid_size = grid_size
        self.tile_size = [(screen_size[0] - 100) / grid_size[0], (screen_size[1] - 100) / grid_size[1]]
        self.rectangle = (
        self.x * self.tile_size[0] + 50, self.y * self.tile_size[1] + 50, self.tile_size[0], self.tile_size[1])
        self.points = [[self.x * self.tile_size[0] + 50, self.y * self.tile_size[1] + 50],  # uppper left
                       [self.x * self.tile_size[0] + 50 + self.tile_size[0], self.y * self.tile_size[1] + 50],
                       # upper right
                       [self.x * self.tile_size[0] + 50 + self.tile_size[0],
                        self.y * self.tile_size[1] + 50 + self.tile_size[1]],  # lower right
                       [self.x * self.tile_size[0] + 50, self.y * self.tile_size[1] + 50 + self.tile_size[1]],
                       # lower left
                       ]
        self.visited = False

    def draw(self, color=(255, 255, 255)):  # x,y represents the tile coordinates
        # global maps
        pg.draw.rect(screen, color, self.rectangle)  # 绘制节点
        for i in range(4):  # 绘制四面墙壁
            if not self.connected[i]:
                pg.draw.line(screen, (0, 0, 0), (self.points[i]), (self.points[((i + 1) % 4)]), 5)
                # for j in range(self.points[i]):
                #     MAZE_MAP[self.points[i][0]-50][self.points[i][1]-50]=1
                '''接下来进行迷宫墙的保存'''

                # if self.points[i][0] == self.points[((i + 1) % 4)][0]:
                #     #X坐标没变，Y坐标变化，说明线是竖着的
                #     for j in range(int(self.points[i][0]),int(self.points[((i+1) % 4)][0])+1):
                #         for k in range(5):
                #             MAZE_MAP[j-50-1][int(self.points[((i+1) % 4)][1])-k-50-1]=1
                # else:
                #     #说明线是横着的
                #     for j in range(int(self.points[i][1]),int(self.points[((i+1) % 4)][1])+1):
                #         for k in range(5):
                #             MAZE_MAP[int(self.points[((i+1) % 4)][0])-k-50-1][j-50-1]=1
def maze_gen(path):
    global tile_covered  # 覆盖节点数量，当覆盖节点数量到达网格数量则停止
    x, y = path[-1]
    if x < 0 or x >= grid_size[0] or y < 0 or y >= grid_size[1]:  # 超出网格范围则退出
        return
    matrix[y][x].draw()
    if matrix[y][x].visited:  # 已访问节点则退出
        return
    elif tile_covered <= grid_size[0] * grid_size[1]:  # 覆盖节点数量未到达网格总数量
        tile_covered += 1
        matrix[y][x].visited = True
        path_choice = [0, 1, 2, 3]
        random.shuffle(path_choice)
        directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # up,right,down,left 0 for not connected

        for i in path_choice:
            x_, y_ = x + directions[i][0], y + directions[i][1]
            path.append([x_, y_])
            if maze_gen(path):
                matrix[y][x].connected[i] = 1  # walls of current node
                matrix[y_][x_].connected[(i + 2) % 4] = 1  # reverse the vector direction
                matrix[y][x].draw()
                matrix[y_][x_].draw()

            path.pop(-1)
        pg.display.update()

        return True

    else:
        return
note='按↑↓←→/W-S-A-D（上下左右）操控角色（蓝色矩形），碰到红色终点后进入下一关，鼠标单击'
note2='（左右键都可以）游戏屏幕即可显示/隐藏你走过的路线，按Q键/右上角×退出，按P键暂停游戏。'
note3='按↑↓←→/W-S-A-D（上下左右）操控角色（蓝色矩形），'
note4='碰到红色终点后进入下一关，鼠标单击（左右键都可以）游戏屏幕即'
note5='可显示/隐藏你走过的路线，按Q键/右上角×退出，按P键暂停游戏。'
screen_size = [900,900]
grid_size = [50, 50]
exit = [20, 20]
tile_covered = 0
steps=0
matrix = []
update()
def clear_data():
    with open("Maze_Game_conf_File\\data.mgcf",'w') as file:
        file.write("")
x=55
nowsss=0
y=54
secret_box=(0,0)
maps=[(55,54)]
can={'up':True,'right':True,'left':True,'down':True}
screen = pg.display.set_mode(screen_size,pygame.RESIZABLE)
pygame.display.set_icon(pygame.image.load("logo.png"))
pygame.display.set_caption('Maze Game\'s window, version 1.0.2')
pygame.mixer.music.load(os.getcwd()+"\\music\\菊次郎的夏天.mp3")
pygame.mixer.music.play(-1)
repeat=150,100
pygame.key.set_repeat(repeat[0],repeat[1])
screenShot=False
ScreenShot_Time=0
screen_shot_list=[]
secret=True
J=pygame.image.load("J.png")
def run():
    global matrix,exit,tile_covered,screenShot,ScreenShot_Time,screen_shot_list,secret
    screenShot=False
    ScreenShot_Time=0
    screen_shot_list=[]
    secret=True
    matrix=[]
    exit=[20,20]
    tile_covered=0
    for y in range(grid_size[1]):  # 创建二维矩阵，x,y代表坐标
        temp = []
        for x in range(grid_size[0]):
            tile = Tile(grid_size, screen_size, x, y)
            temp.append(tile)
        matrix.append(temp)
    path = [[0, 0]]
    where = random.randint(1, 3)
    global rect1
    if where == 1:
        rect1 = pygame.Rect(900 - 65, 900 - 65, 9, 9)
    elif where == 2:
        rect1 = pygame.Rect(54, 900 - 65, 9, 9)
    else:
        rect1 = pygame.Rect(900 - 65, 54, 9, 9)
    screen.fill((255, 255, 255))
    maze_gen(path)
    pg.display.update()
    day=int(time.strftime('%w',time.localtime()))
    if day == 1:
        day="一"
    elif day == 2:
        day="二"
    elif day == 3:
        day="三"
    elif day == 4:
        day="四"
    elif day == 5:
        day="五"
    elif day == 6:
        day="六"
    elif day == 7:
        day="日"
    nowss = time.strftime('%Z %Y-%m-%d 星期{} %H:%M:%S'.format(day), time.localtime())
    global nowsss
    nowsss=nowss
    try:
        with open("Maze_Game_conf_File\\data.mgcf",'a', encoding="utf-8") as file:
            file.write("")
    except:
        with open("Maze_Game_conf_File\\Mazedata.mgcf",'w',encoding='utf-8') as file:
            file.write("")
    font_surface2 = font2.render(note,True,'orange')
    font_surface3 = font2.render(note2,True,'orange')
    screen.blit(font_surface2,(75-18+48,860))
    screen.blit(font_surface3,(75-18+48,875))
    global coin_blits,lightning_blits,secret_box
    coin_blits = []
    lightning_blits = (0, 0)
    for i in range(100):
        choices = random.choice(random.choice(mapOfList))
        coin_blits.append(choices)
        screen.blit(pygame.transform.scale(image_coin,(9,9)), choices)
    while lightning_blits == (0, 0) or lightning_blits in coin_blits:
        lightning_blits = random.choice(random.choice(mapOfList))
    screen.blit(pygame.transform.scale(image_lightning,(11,11)), lightning_blits)
    while secret_box == (0,0) or secret_box == lightning_blits or secret_box in coin_blits:
        secret_box = random.choice(random.choice(mapOfList))
rect1=0
pg.init()
def has_color(aSurface,aRect,aColor):
    pixel=pygame.PixelArray(aSurface)               #锁定aSurface,将各点颜色保存在2维数组
    aPixel=pixel[aRect.x:aRect.x+aRect.width+15,aRect.y:aRect.y+aRect.height+15]  #得到数组切片
    global can
    if aColor in aPixel:
        if aColor in pixel[aRect.x-15:aRect.x+aRect.width,aRect.y:aRect.y+aRect.height]:
            can['left']=False
        else:
            can['left']=True
        if aColor in pixel[aRect.x:aRect.x+aRect.width+15,aRect.y:aRect.y+aRect.height]:
            can['right']=False
        else:
            can['right']=True
        if aColor in pixel[aRect.x:aRect.x+aRect.width,aRect.y-15:aRect.y+aRect.height]:
            can['up'] = False
        else:
            can['up']=True
        if aColor in pixel[aRect.x:aRect.x+aRect.width,aRect.y:aRect.y+aRect.height+15]:
            can['down'] = False
        else:
            can['down']=True
    else:
        can['left']=True
        can['right']=True
        can['up']=True
        can['down']=True
    del pixel           #解锁aSurface并删除数组
font_name = pygame.font.match_font('fangsong')  # 2.获得字体文件
font = pygame.font.Font(font_name, 20)
# font_name3 = pygame.font.match_font('胖娃体.ttf')  # 2.获得字体文件
# font3 = pygame.font.Font(font_name3, 40)
# font_name4 = pygame.font.match_font('胖娃体.ttf')  # 2.获得字体文件
# font4 = pygame.font.Font(font_name4, 70)
font_name2 = pygame.font.match_font('kaiti')  # 2.获得字体文件
font2 = pygame.font.Font(font_name2, 15)
font_name8 = pygame.font.match_font('kaiti')  # 2.获得字体文件
font8 = pygame.font.Font(font_name8, 50)
font5 = pygame.font.Font(font_name2, 70)
font6 = pygame.font.Font(font_name2, 40)
font7 = pygame.font.Font(font_name2, 30)
# img_play=pygame.image.load('play.jpeg').convert_alpha()
level=1
color=(175,175,175)
m2=0
h2=0
add=False
# def show_pic(screen):
#     #TODO show pic
#     s = f"（{screen_shot_list[0]}）" if screen_shot_list[0] > 1 else ""
#     if len(screen_shot_list) == 1:
#         print(1)
#         xxx = pygame.image.load(os.getcwd() + f"\\Maze_Game_conf_File\\ScreenShot\\Maze_Game_Screen_Shot{s}.png")
#         # xx2=pygame.transform.scale(xxx,(0,0))
#         screen.blit(xxx, (290, 570))
#         # xxx=pygame.image.load(os.getcwd()+f"\\Maze_Game_conf_File\\ScreenShot\\Maze_Game_Screen_Shot{s}.png")
#         # # xx2=pygame.transform.scale(xxx,(250,250))
#         # screen.blit(xxx,(290,570))#TODO 为什么我是要screen.blit(xxx)，却显示是screen.blit("lightning.png",(x,y))呢？
#         print(os.getcwd() + f"\\Maze_Game_conf_File\\ScreenShot\\Maze_Game_Screen_Shot{s}.png")
#     elif len(screen_shot_list) == 2:
#         screen.blit(pygame.transform.scale(
#             pygame.image.load(os.getcwd() + f"\\Maze_Game_conf_File\\ScreenShot\\Maze_Game_Screen_Shot{s}.png"),
#             (250, 250)),
#                     (175, 570))
#         screen.blit(pygame.transform.scale(pygame.image.load(
#             os.getcwd() + f"\\Maze_Game_conf_File\\ScreenShot\\Maze_Game_Screen_Shot（{str(int(s[1:-1]) + 1)}）.png"),
#                                            (250, 250)),
#                     (725, 570))
#     else:
#         screen.blit(pygame.transform.scale(
#             pygame.image.load(os.getcwd() + f"\\Maze_Game_conf_File\\ScreenShot\\Maze_Game_Screen_Shot{s}.png"),
#             (250, 250)),
#                     (55, 570))
#         screen.blit(pygame.transform.scale(pygame.image.load(
#             os.getcwd() + f"\\Maze_Game_conf_File\\ScreenShot\\Maze_Game_Screen_Shot（{str(int(s[1:-1]) + 1)}）.png"),
#                                            (250, 250)),
#                     (325, 570))
#         screen.blit(pygame.transform.scale(pygame.image.load(
#             os.getcwd() + f"\\Maze_Game_conf_File\\ScreenShot\\Maze_Game_Screen_Shot（{str(int(s[1:-1]) + 2)}）.png"),
#                                            (250, 250)),
#                     (595, 570))
#     screen.blit(font7.render(f"共{ScreenShot_Time}张截屏，", True, (0, 0, 0)), (540, 780))
sec=-1
pause=False
pause_time=0
write_s=0
add_m=False
downs=True
def draw_button(screen,pos,w,h,line_color,color,line_width):
    r=int(h/2)
    pygame.draw.circle(screen,line_color,(pos[0]+r,pos[1]+r),r,line_width)
    pygame.draw.circle(screen,line_color,(pos[0]+w-r,pos[1]+r),r,line_width)
    pygame.draw.rect(screen,color,(pos[0]+r+1,pos[1]+1,w-(r*2),(r-1)*2),0)
    pygame.draw.line(screen,line_color,(pos[0]+r,pos[1]+2),(pos[0]+w-r,pos[1]+2),line_width)
    pygame.draw.line(screen,line_color,(pos[0]+r,pos[1]+r*2),(pos[0]+w-r,pos[1]+r*2),line_width)

def do_this():
    t=time.localtime()
    global h1,m1,s1,downs
    h1,m1,s1=t.tm_hour,t.tm_min,t.tm_sec
    downs=False
whiles_x,whiles_y=240,50
whiles_rect_x,whiles_rect_y=300,500
whiles_rect_x2,whiles_rect_y2=300,570
whiles_x2,whiles_y2=240,50
whiles_rect_x3,whiles_rect_y3=300,640
whiles_x3,whiles_y3=240,50
whiles_rect_x4,whiles_rect_y4=300,715
whiles_x4,whiles_y4=240,50
whiles_click=True
FPSClock = pygame.time.Clock()
is_big=False
image_coin=pygame.image.load("coin.jpeg")
image_coin=pygame.transform.scale(image_coin,(40,40)).convert()
image_coin.set_colorkey((255,255,255))
image_lightning = pygame.image.load("lightning.png")
image_lightning.set_colorkey((255,255,255))
image_lightning=pygame.transform.scale(image_lightning,(40,40))
logo=pygame.image.load('logo.png')
coin_blits=[]
lightning_blits=(0,0)
for i in range(100):
    choices=random.choice(random.choice(mapOfList))
    coin_blits.append(choices)
    screen.blit(image_coin, choices)
while lightning_blits==(0,0) or lightning_blits in coin_blits:
    lightning_blits=random.choice(random.choice(mapOfList))
screen.blit(image_lightning, lightning_blits)
colors='blue'
all_screen_play=False
_=0
_2=0
def home(a):
    global downs,whiles_rect_x,whiles_rect_y,whiles_x,whiles_y,font6,font7,font8,font5,font2,\
        whiles_rect_x2, whiles_rect_y2, whiles_x2, whiles_y2,whiles_rect_x3, whiles_rect_y3,\
        whiles_x3, whiles_y3,whiles_rect_x4, whiles_rect_y4, whiles_x4, whiles_y4,click_img,\
        whiles_click,all_screen_play,colors,_,_2,get_lightning,get_coin,is_big,ListOfPlayInfo
    while downs:
        screen.fill((255,255,255))
        draw_button(screen, (30-5, 30-5), 40+len(list(str(get_coin)))*20+30, 50,(105,105,105),(105,105,105),0)
        draw_button(screen, (30-5, 90-5), 40+len(list(str(get_lightning)))*20+30, 50,(105,105,105),(105,105,105),0)
        screen.blit(image_coin,(30,30))
        screen.blit(image_lightning,(30,90))
        screen.blit(font6.render("{}".format(get_coin),True,"white"),(80,30))
        screen.blit(font6.render("{}".format(get_lightning),True,"white"),(80,90))
        font_surface5= font5.render('迷宫游戏（V1.0.2）', True, 'black')
        screen.blit(font_surface5, (100, 270))
        screen.blit(logo, ((900-128)/2-30,270-128-30))
        if a:
            pygame.draw.rect(screen, (255,0,0),(whiles_rect_x,whiles_rect_y,whiles_x,whiles_y),0)
            font_surface4 = font6.render('开始游戏', True, 'white')
            # screen.blit(img_play, (310,510))
            screen.blit(font_surface4, (330, 505))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (whiles_rect_x, whiles_rect_y, whiles_x, whiles_y), 0)
            font_surface4 = font6.render('（不可）开始游戏', True, 'white')
            # screen.blit(img_play, (310,510))
            screen.blit(font_surface4, (330-40, 505))
        pygame.draw.rect(screen, 'orange', (whiles_rect_x2, whiles_rect_y2, whiles_x2, whiles_y2), 0)
        font_surface5 = font6.render('PYAI自动寻路', True, 'white')
        # screen.blit(img_play, (310,510))
        screen.blit(font_surface5, (300, 575))
        pygame.draw.rect(screen, '#0000CD', (whiles_rect_x3, whiles_rect_y3, whiles_x3, whiles_y3), 0)
        font_surface6 = font6.render('查看游戏记录', True, 'white')
        # screen.blit(img_play, (310,510))
        screen.blit(font_surface6, (300, 645))
        pygame.draw.rect(screen, 'cyan', (whiles_rect_x4, whiles_rect_y4, whiles_x4, whiles_y4), 0)
        font_surface7 = font6.render('游戏规则', True, 'white')
        # screen.blit(img_play, (310,510))
        screen.blit(font_surface7, (330, 715))
        # button1=BFButton(screen,(300,500,200,5),'开始游戏',bg=(255,0,0),fg='white',click=do_this)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 300 <= mouse_x <= 540 and 500 <= mouse_y <= 550 and a:
                    t = time.localtime()
                    global h1,m1,s1
                    h1, m1, s1 = t.tm_hour, t.tm_min, t.tm_sec
                    downs = False
                elif 300 <= mouse_x <= 540 and 725 <= mouse_y <= 775:
                    screen.fill((255,255,255))
                    whiles_click=True
                    font_surface8 = font6.render('游戏规则', True, 'black')
                    # screen.blit(img_play, (310,510))
                    screen.blit(font_surface8, (290+80, 40))
                    # pygame.draw.rect(screen, 'black', (10,8,80,17), 2)
                    font_surface9 = font2.render('〈返回主页', True, (100,100,100))
                    # screen.blit(img_play, (310,510))
                    screen.blit(font_surface9, (10, 10))
                    font_surface10 = font7.render(note3,True,'black')
                    screen.blit(font_surface10, (90, 130))
                    font_surface11 = font7.render(note4,True,'black')
                    screen.blit(font_surface11, (0, 170))
                    font_surface12 = font7.render(note5,True,'black')
                    screen.blit(font_surface12, (0, 210))
                    ##################第一阶段按钮绘画开始#####################
                    pygame.draw.rect(screen, 'black', (170, 380-55, 74, 74), 2)
                    font_surface13 = font5.render('↑', False, 'black')
                    screen.blit(font_surface13, (170 + 2, 380 + 2-55))
                    #######################################################
                    pygame.draw.rect(screen, 'black', (170, 380+6+74-55,74,74),2)
                    font_surface13 = font5.render('↓', False, 'black')
                    screen.blit(font_surface13, (170 + 2, 380 + 8+74-55))
                    ########################################################
                    pygame.draw.rect(screen, 'black', (170-74-6, 380 + 6 + 74-55, 74, 74), 2)
                    font_surface13 = font5.render('←', False, 'black')
                    screen.blit(font_surface13, (170 -4-74, 380 + 8 + 74-55))
                    ########################################################
                    pygame.draw.rect(screen, 'black', (170+74+6, 380 + 6 + 74-55, 74, 74), 2)
                    font_surface13 = font5.render('→', False, 'black')
                    screen.blit(font_surface13, (170 + 8+74, 380 + 8 + 74-55))
                    ##################第一阶段按钮绘画完成######################
                    ##################第二阶段按钮绘画开始######################
                    pygame.draw.rect(screen, 'black', (540, 380-55, 74, 74), 2)
                    font_surface13 = font5.render('W', True, 'black')
                    screen.blit(font_surface13, (540+16 + 2, 380 + 2-55))
                    #######################################################
                    pygame.draw.rect(screen, 'black', (540, 380 + 6 + 74-55, 74, 74), 2)
                    font_surface13 = font5.render('S', True, 'black')
                    screen.blit(font_surface13, (540 +16+ 2, 380 + 8 + 74-55))
                    ########################################################
                    pygame.draw.rect(screen, 'black', (540 - 74 - 6, 380 + 6 + 74-55, 74, 74), 2)
                    font_surface13 = font5.render('A', True, 'black')
                    screen.blit(font_surface13, (540 +16- 4 - 74, 380 + 8 + 74-55))
                    ########################################################
                    pygame.draw.rect(screen, 'black', (540 + 74 + 6, 380 + 6 + 74-55, 74, 74), 2)
                    font_surface13 = font5.render('D', True, 'black')
                    screen.blit(font_surface13, (540 + 8+16 + 74, 380 + 8 + 74-55))
                    ##################第二阶段按钮绘画完成######################
                    ##################第一阶段图片绘画开始######################
                    click_img=pygame.transform.scale(click_img, (90,90))
                    screen.blit(click_img, (360,321))
                    ##################第一阶段图片绘画完成######################
                    ##################第三阶段按钮绘画开始######################
                    pygame.draw.rect(screen, 'black', (88, 658, 74, 74), 2)
                    font_surface13 = font5.render('P', True, 'black')
                    screen.blit(font_surface13, (99+10, 660))
                    ########################################################
                    pygame.draw.rect(screen, 'black', (88, 758, 74, 74), 2)
                    font_surface13 = font5.render('Q', True, 'black')
                    screen.blit(font_surface13, (99+10, 760))
                    ########################################################
                    pygame.draw.rect(screen, 'black', (88+76+5, 758, 74, 74), 2)
                    font_surface13 = font5.render('×', True, 'black')
                    screen.blit(font_surface13, (99+74, 760))
                    #################第三阶段按钮绘画完成#######################
                    font_surface13 = font2.render('*除鼠标图标之外，处于同一行的示例均同效',True,'blue')
                    screen.blit(font_surface13, (0,854))
                    font_surface13 = font2.render('视频看不清？试试', True, 'black')
                    screen.blit(font_surface13, (900 - 12 * 15, 500 - 17))
                    while whiles_click:
                        if all_screen_play:
                            if _2 == 0:
                                font_surface9 = font2.render('〈返回至游戏规则', True, (100,100,100))
                                # screen.blit(img_play, (310,510))
                                screen.blit(font_surface9, (10, 10))
                            if video.isOpened():
                                ret, frame = video.read()
                                try:
                                    frame = numpy.rot90(frame, k=-1)
                                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                    frame = pygame.surfarray.make_surface(frame)
                                    frame = pygame.transform.flip(frame, False, True)
                                    frame = pygame.transform.scale(frame, (900, 600))
                                    screen.blit(frame, (0, 150))
                                except:
                                    break
                            for event3 in pygame.event.get():
                                if event3.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event3.type == pygame.MOUSEBUTTONDOWN:
                                    x3,y3=event3.pos
                                    if 10 <= x3 <= 8*15+10 and 10 <= y3 <= 26:
                                        all_screen_play=False
                                        screen.fill((255,255,255))
                                        font_surface8 = font6.render('游戏规则', True, 'black')
                                        # screen.blit(img_play, (310,510))
                                        screen.blit(font_surface8, (290 + 80, 40))
                                        # pygame.draw.rect(screen, 'black', (10,8,80,17), 2)
                                        font_surface9 = font2.render('〈返回主页', True, (100, 100, 100))
                                        # screen.blit(img_play, (310,510))
                                        screen.blit(font_surface9, (10, 10))
                                        font_surface10 = font7.render(note3, True, 'black')
                                        screen.blit(font_surface10, (90, 130))
                                        font_surface11 = font7.render(note4, True, 'black')
                                        screen.blit(font_surface11, (0, 170))
                                        font_surface12 = font7.render(note5, True, 'black')
                                        screen.blit(font_surface12, (0, 210))
                                        ##################第一阶段按钮绘画开始#####################
                                        pygame.draw.rect(screen, 'black', (170, 380 - 55, 74, 74), 2)
                                        font_surface13 = font5.render('↑', False, 'black')
                                        screen.blit(font_surface13, (170 + 2, 380 + 2 - 55))
                                        #######################################################
                                        pygame.draw.rect(screen, 'black', (170, 380 + 6 + 74 - 55, 74, 74), 2)
                                        font_surface13 = font5.render('↓', False, 'black')
                                        screen.blit(font_surface13, (170 + 2, 380 + 8 + 74 - 55))
                                        ########################################################
                                        pygame.draw.rect(screen, 'black', (170 - 74 - 6, 380 + 6 + 74 - 55, 74, 74), 2)
                                        font_surface13 = font5.render('←', False, 'black')
                                        screen.blit(font_surface13, (170 - 4 - 74, 380 + 8 + 74 - 55))
                                        ########################################################
                                        pygame.draw.rect(screen, 'black', (170 + 74 + 6, 380 + 6 + 74 - 55, 74, 74), 2)
                                        font_surface13 = font5.render('→', False, 'black')
                                        screen.blit(font_surface13, (170 + 8 + 74, 380 + 8 + 74 - 55))
                                        ##################第一阶段按钮绘画完成######################
                                        ##################第二阶段按钮绘画开始######################
                                        pygame.draw.rect(screen, 'black', (540, 380 - 55, 74, 74), 2)
                                        font_surface13 = font5.render('W', True, 'black')
                                        screen.blit(font_surface13, (540 + 16 + 2, 380 + 2 - 55))
                                        #######################################################
                                        pygame.draw.rect(screen, 'black', (540, 380 + 6 + 74 - 55, 74, 74), 2)
                                        font_surface13 = font5.render('S', True, 'black')
                                        screen.blit(font_surface13, (540 + 16 + 2, 380 + 8 + 74 - 55))
                                        ########################################################
                                        pygame.draw.rect(screen, 'black', (540 - 74 - 6, 380 + 6 + 74 - 55, 74, 74), 2)
                                        font_surface13 = font5.render('A', True, 'black')
                                        screen.blit(font_surface13, (540 + 16 - 4 - 74, 380 + 8 + 74 - 55))
                                        ########################################################
                                        pygame.draw.rect(screen, 'black', (540 + 74 + 6, 380 + 6 + 74 - 55, 74, 74), 2)
                                        font_surface13 = font5.render('D', True, 'black')
                                        screen.blit(font_surface13, (540 + 8 + 16 + 74, 380 + 8 + 74 - 55))
                                        ##################第二阶段按钮绘画完成######################
                                        ##################第一阶段图片绘画开始######################
                                        click_img = pygame.transform.scale(click_img, (90, 90))
                                        screen.blit(click_img, (360, 321))
                                        ##################第一阶段图片绘画完成######################
                                        ##################第三阶段按钮绘画开始######################
                                        pygame.draw.rect(screen, 'black', (88, 658, 74, 74), 2)
                                        font_surface13 = font5.render('P', True, 'black')
                                        screen.blit(font_surface13, (99 + 10, 660))
                                        ########################################################
                                        pygame.draw.rect(screen, 'black', (88, 758, 74, 74), 2)
                                        font_surface13 = font5.render('Q', True, 'black')
                                        screen.blit(font_surface13, (99 + 10, 760))
                                        ########################################################
                                        pygame.draw.rect(screen, 'black', (88 + 76 + 5, 758, 74, 74), 2)
                                        font_surface13 = font5.render('×', True, 'black')
                                        screen.blit(font_surface13, (99 + 74, 760))
                                        #################第三阶段按钮绘画完成#######################
                                        font_surface13 = font2.render('*除鼠标图标之外，处于同一行的示例均同效', True, 'blue')
                                        screen.blit(font_surface13, (0, 854))
                                        font_surface13 = font2.render('视频看不清？试试', True, 'black')
                                        screen.blit(font_surface13, (900 - 12 * 15, 500 - 17))
                                        _2=0
                            if all_screen_play:
                                _2=1
                        else:
                            if video.isOpened():
                                ret, frame = video.read()
                                try:
                                    frame = numpy.rot90(frame, k=-1)
                                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                    frame = pygame.surfarray.make_surface(frame)
                                    frame = pygame.transform.flip(frame, False, True)
                                    frame=pygame.transform.scale(frame, (600, 400))
                                    screen.blit(frame, (300,500))
                                except:
                                    downs=False
                            for event2 in pygame.event.get():
                                #################备注阶段提示绘画开始#######################
                                pygame.draw.rect(screen, 'white', (900-4*15,500-17,60,15),0)
                                font_surface13 = font2.render('全屏播放', True, colors)
                                screen.blit(font_surface13, (900 - 4 * 15, 500 - 17))
                                #################备注阶段提示绘画完成#######################
                                if event2.type == pygame.MOUSEBUTTONDOWN:
                                    x1,y1=event2.pos
                                    if 10 <= x1 <= 80 and 8 <= y1 <= 27:
                                        whiles_click=False
                                        screen.fill((255,255,255))
                                    if 900-60 <= x1 <= 900 and 500-17 <= y1 <= 500-2:
                                        all_screen_play=True
                                        screen.fill((255,255,255))
                                if event2.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event2.type == pygame.MOUSEMOTION:
                                    x2,y2=event2.pos
                                    if 900-60 <= x2 <= 900 and 500-17 <= y2 <= 500-2:
                                        colors='red'
                                        _=1
                                    else:
                                        colors='blue'
                                        _=1
                            _+=1
                        pygame.display.update()
                elif 300<=mouse_x<=540 and 645<=mouse_y<=645+40:
                    screen.fill((255,255,255))
                    pygame.mixer.music.play()
            if event.type == pygame.MOUSEMOTION:
                mouse_move_x,mouse_move_y=event.pos
                if 300 <= mouse_move_x <= 540 and 500 <= mouse_move_y <= 550 and not is_big:
                    if whiles_x != 260 and whiles_y != 70:
                        whiles_x,whiles_y=whiles_x+10,whiles_y+10
                        whiles_rect_x,whiles_rect_y=290,490
                elif 300 <= mouse_move_x <= 540 and 575 <= mouse_move_y <= 625 and not is_big:
                    if whiles_x2 != 260 and whiles_y2 != 70:
                        whiles_x2,whiles_y2=whiles_x2+10,whiles_y2+10
                        whiles_rect_x2,whiles_rect_y2=290,560
                elif 300 <= mouse_move_x <= 540 and 650 <= mouse_move_y <= 700 and not is_big:
                    if whiles_x3 != 260 and whiles_y3 != 70:
                        whiles_x3,whiles_y3=whiles_x3+10,whiles_y3+10
                        whiles_rect_x3,whiles_rect_y3=290,630
                elif 300 <= mouse_move_x <= 540 and 725 <= mouse_move_y <= 775 and not is_big:
                    if whiles_x4 != 260 and whiles_y4 != 70:
                        whiles_x4,whiles_y4=whiles_x4+10,whiles_y4+10
                        whiles_rect_x4,whiles_rect_y4=290,700
                else:
                    is_big=False
                    whiles_x, whiles_y = 240, 50
                    whiles_rect_x, whiles_rect_y = 300, 500
                    whiles_x2, whiles_y2 = 240, 50
                    whiles_rect_x2, whiles_rect_y2 = 300, 570
                    whiles_rect_x3, whiles_rect_y3 = 300, 640
                    whiles_x3, whiles_y3 = 240, 50
                    whiles_rect_x4, whiles_rect_y4 = 300, 710
                    whiles_x4, whiles_y4 = 240, 50
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
home(True)
run()
pygame.mixer.music.stop()
pygame.mixer.music.unload()
moneyGo=False
tkinter.messagebox.showinfo("选择背景音乐","请选择您想要选的音乐。")
path=tkinter.filedialog.askopenfilename(title="选择MP3文件",filetypes=[("MP3音乐文件",".mp3")],initialdir=os.getcwd()+"\\music")
pygame.mixer.music.load(path)
pygame.mixer.music.play(-1)
while True:
    home(False)
    times = time.localtime()
    h, m, s = times.tm_hour, times.tm_min, times.tm_sec
    my=pygame.Rect(x,y,9,9)
    pygame.draw.rect(screen,(0,255,255),my,0)
    pygame.draw.rect(screen,(255,255,255),(20,0,900,40),0)
    # if sec == -1:
    #     sec=0
    # if sec<s:
    #     s1+=1
    #     sec+=1
    # elif sec!=0:
    #     s1=sec
    if s1 / 60 >0:
        m1+=int(s1/60)
        s1%=60
    if m1 / 60 <0:
        h1+=int(s1/60)
        m1%=60
    if pause:
        if sec == -1:
            sec=0
        if s-1==write_s:
            sec+=1
        if s-2==write_s:
            sec+=2
    if not pause:
        if s-s1 < 0:
            s2=s+(60-s1)
        else:
            s2=s-s1
        if s2 == 59:
            add=True
        if s-s1 == 0 and add:
            m2+=1
            add=False
        if m2 == 59:
            add=True
        if m2 % 60 == 0 and m2 != 0 and add_m:
            h2+=1
            m2%=60
            add_m=False
        font_surface = font.render('你已走的步数：{}，现在是第{}关，计时：{:0>2}:{:0>2}:{:0>2}，此局获得{:0>3}枚金币，{:0>3}个能量值。'.format(str(steps),str(level),str(h2),str(m2),str(s2),this_coin,this_lightning), True, 'orange')
        # h3,m3,s3=h2,m2,s2
    # else:
    #     font_surface = font.render('你已走的步数：{}，现在是第{}关，计时：{:0>2}:{:0>2}:{:0>2}'.format(str(steps), str(level), str(h3), str(m3), str(s3)), True,'orange')
    # pygame.draw.rect(screen, 'white', (0,860,900,30),0)
    screen.blit(font_surface, (20, 20))
    screen.blit(font.render("截屏记录",True,(30,144,255)),(20,5))
    font_surface13 = font.render('点我使用3个能量值/300枚金币合成"钞"能力，直接通关',True,(132,112,255))
    screen.blit(font_surface13, (900-28*20, 5))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            if pause:
                tkinter.messagebox.showwarning('提示','请解除暂停再重试。')
            else:
                obj=""
                with open("Maze_Game_conf_File\\data.mgcf","r",encoding='utf-8') as file:
                    ob=file.readlines()[2:]
                for i in ob:
                    obj+=i
                with open("Maze_Game_conf_File\\data.mgcf", "w", encoding='utf-8') as file:
                    file.write("{}\n{}\n".format(get_coin,get_lightning))
                    file.write(obj)
                    file.write("{}\n".format(nowsss))
                    file.write("{}×{}\n".format(grid_size[0],grid_size[1]))
                    file.write(str(level) + "\n")
                    file.write("{:0>2}:{:0>2}:{:0>2}\n".format(str(h2), str(m2), str(s2)))
                    file.write("{}\n".format(str(pauses)))
                    if len(pauses_time)!=0:
                        for i in pauses_time:
                            file.write("{:0>2}:{:0>2}:{:0>2}".format(i.split(":")[0],i.split(":")[1],i.split(":")[2])+"\n")
                    else:
                        file.write("No pause time.\n")
                    file.write("{}\n".format(steps))
                    file.write("{}\n".format(get_lightning))
                    file.write("{}\n".format(get_coin))
                    file.write("{}\n".format(this_lightning))
                    file.write("{}\n".format(this_coin))
                    file.write("{}\n".format("是" if moneyGo else "否"))
                    file.write("{}\n".format("是" if not secret else "否"))
                pg.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not yes_:
                color=(175,175,175)
                yes_=True
            else:
                color=(255,255,255)
                yes_=False
            for i in maps:
                r=pygame.Rect(i[0],i[1],9,9)
                pygame.draw.rect(screen,color,r,0)
            if 20<=event.pos[0]<=80 and 5 <= event.pos[1] <= 25:
                ok_OR=tkinter.messagebox.askyesnocancel("温馨提示","温馨提示：因为截屏功能是通过虚拟窗口截屏\n，可能游戏窗口未响应几秒钟，截屏完成后会\n提示成功记录下游戏屏幕（截屏时也可以将P\nyGame窗口最小化，因为通过虚拟窗口截屏所\n以不用最大化，截屏后会将图片复制到剪切板\n，Windows11按Windows徽标键+V\n查看剪切板），是否截屏？")
                if ok_OR:
                    a=ScreenShotPyGameWindow.main()
                    tkinter.messagebox.showinfo("提示",'成功记录下PyGame屏幕！您可以从 '+os.getcwd()+' 查看图片！')
                    screenShot=True
                    ScreenShot_Time+=1
                    screen_shot_list.append(a)
                    tkinter.messagebox.showinfo(str(a))
            elif 900-25*20 <= event.pos[0] <= 900 and 5 <= event.pos[1] <= 25:
                if get_lightning>=3:
                    moneyGo=True
                    get_lightning-=3
                elif get_coin>=300:
                    moneyGo=True
                    get_coin-=300
                else:
                    tkinter.messagebox.showwarning('提示','您的能量值和金币都不足，无法合成”钞“能力。')
        elif event.type == pygame.KEYDOWN:
            has_color(screen,my,(0,0,0))
            if event.key == pygame.K_q:
                if pause:
                    tkinter.messagebox.showwarning('提示','请解除暂停再重试。')
                else:
                    obj=""
                    with open("Maze_Game_conf_File\\data.mgcf","r",encoding='utf-8') as file:
                        ob=file.readlines()[2:]
                    for i in ob:
                        obj+=i
                    with open("Maze_Game_conf_File\\data.mgcf", "w", encoding='utf-8') as file:
                        file.write("{}\n{}\n".format(get_coin,get_lightning))
                        file.write(obj)
                        file.write("{}\n".format(nowsss))
                        file.write("{}×{}\n".format(grid_size[0],grid_size[1]))
                        file.write(str(level) + "\n")
                        file.write("{:0>2}:{:0>2}:{:0>2}\n".format(str(h2), str(m2), str(s2)))
                        file.write("{}\n".format(str(pauses)))
                        if len(pauses_time)!=0:
                            for i in pauses_time:
                                file.write("{:0>2}:{:0>2}:{:0>2}".format(i.split(":")[0],i.split(":")[1],i.split(":")[2])+"\n")
                        else:
                            file.write("No pause time.\n")
                        file.write("{}\n".format(steps))
                    file.write("{}\n".format(get_lightning))
                    file.write("{}\n".format(get_coin))
                    file.write("{}\n".format(this_lightning))
                    file.write("{}\n".format(this_coin))
                    file.write("{}\n".format("是" if moneyGo else "否"))
                    file.write("{}\n".format("是" if not secret else "否"))
                    pg.quit()
                    sys.exit()
            if event.key == pygame.K_p:
                if pause:
                    pause=False
                    screen.set_alpha(255)
                    pause_time=0
                    s1+=sec
                    if s1 / 60 > 0:
                        m1+=s1/60
                        s1%=60
                    if m1 / 60 < 0:
                        h1+=m1/60
                        m1%=60
                    tts = time.localtime()
                    Ph, Pm, Ps = tts.tm_hour, tts.tm_min, tts.tm_sec
                    ones2 = Ph * 3600 + Pm * 60 + Ps
                    ones_a=ones2-ones
                    Ph2,Pm2=divmod(ones_a, 3600)
                    Pm2,Ps2=divmod(Pm2, 60)
                    pauses_time.append("{}:{}:{}".format(Ph2,Pm2,Ps2))
                    # add1=h-h3#22-22=0
                    # add2=m-m3#7-6=1
                    # add3=s-s3#0-50=-50
                    # if add3 < 0:
                    #     add2-=1#0
                    #     add3=s+(60-s3)#60-59
                    # if add2<0:
                    #     add1-=1
                    #     add2=m+(60-m3)
                    # h1+=add1
                    # m1+=add2
                    # s1+=add3
                    # if s1 / 60 > 0:
                    #     m1+=int(s1/60)
                    # if m1 / 60 > 0:
                    #     h1+=int(m1/60)
                    # s1+=sec
                else:
                    pauses+=1
                    tts = time.localtime()
                    Ph, Pm, Ps = tts.tm_hour, tts.tm_min, tts.tm_sec
                    ones=Ph*3600+Pm*60+Ps
                    pause=True
                    screen.set_alpha(100)
                    sec=0
                    # h3,m3,s3=h2,m2,s2
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and can['left'] and not pause:
                x-=16
                steps+=1
                if not yes_:
                    mys=pygame.Rect(x+16,y,9,9)
                    pygame.draw.rect(screen,(255,255,255),mys,0)
                else:
                    mys=pygame.Rect(x+16,y,9,9)
                    pygame.draw.rect(screen,(175,175,175),mys,0)
                if (mys[0],mys[1]) in coin_blits:
                    get_coin+=1
                    this_coin+=1
                    while (mys[0],mys[1]) in coin_blits:
                        coin_blits.remove((mys[0],mys[1]))
                if (mys[0],mys[1]) == lightning_blits:
                    get_lightning+=1
                    this_lightning+=1
                    lightning_blits=(0,0)
                if (mys[0],mys[1]) == secret_box and secret:
                    secret=False
                    news_lightning=random.randint(3,6)
                    news_coin=random.randint(100,300)
                    get_coin+=news_coin
                    this_coin+=news_coin
                    get_lightning+=news_lightning
                    this_lightning+=news_lightning
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and can['down'] and not pause:
                y+=16
                steps+=1
                if not yes_:
                    mys=pygame.Rect(x,y-16,9,9)
                    pygame.draw.rect(screen,(255,255,255),mys,0)
                else:
                    mys=pygame.Rect(x,y-16,9,9)
                    pygame.draw.rect(screen,(175,175,175),mys,0)
                if (mys[0],mys[1]) in coin_blits:
                    get_coin+=1
                    while (mys[0],mys[1]) in coin_blits:
                        coin_blits.remove((mys[0],mys[1]))
                if (mys[0],mys[1]) == lightning_blits:
                    get_lightning+=1
                    this_lightning+=1
                    lightning_blits=(0,0)
                if (mys[0],mys[1]) == secret_box and secret:
                    secret=False
                    news_lightning=random.randint(3,6)
                    news_coin=random.randint(100,300)
                    get_coin+=news_coin
                    this_coin+=news_coin
                    get_lightning+=news_lightning
                    this_lightning+=news_lightning
            elif (event.key == pygame.K_UP or event.key == pygame.K_w) and can['up'] and not pause:
                y-=16
                steps+=1
                if not yes_:
                    mys=pygame.Rect(x,y+16,9,9)
                    pygame.draw.rect(screen,(255,255,255),mys,0)
                else:
                    mys=pygame.Rect(x,y+16,9,9)
                    pygame.draw.rect(screen,(175,175,175),mys,0)
                if (mys[0],mys[1]) in coin_blits:
                    get_coin+=1
                    this_coin+=1
                    while (mys[0],mys[1]) in coin_blits:
                        coin_blits.remove((mys[0],mys[1]))
                if (mys[0],mys[1]) == lightning_blits:
                    get_lightning+=1
                    this_lightning+=1
                    lightning_blits=(0,0)
                if (mys[0],mys[1]) == secret_box and secret:
                    secret=False
                    news_lightning=random.randint(3,6)
                    news_coin=random.randint(100,300)
                    get_coin+=news_coin
                    this_coin+=news_coin
                    get_lightning+=news_lightning
                    this_lightning+=news_lightning
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and can['right'] and not pause:
                x+=16
                steps+=1
                if not yes_:
                    mys=pygame.Rect(x-16,y,9,9)
                    pygame.draw.rect(screen,(255,255,255),mys,0)
                else:
                    mys=pygame.Rect(x-16,y,9,9)
                    pygame.draw.rect(screen,(175,175,175),mys,0)
                if (mys[0],mys[1]) in coin_blits:
                    get_coin+=1
                    this_coin+=1
                    while (mys[0],mys[1]) in coin_blits:
                        coin_blits.remove((mys[0],mys[1]))
                if (mys[0],mys[1]) == lightning_blits:
                    get_lightning+=1
                    this_lightning+=1
                    lightning_blits=(0,0)
                if (mys[0],mys[1]) == secret_box and secret:
                    secret=False
                    news_lightning=random.randint(3,6)
                    news_coin=random.randint(100,300)
                    get_coin+=news_coin
                    this_coin+=news_coin
                    get_lightning+=news_lightning
                    this_lightning+=news_lightning
            elif event.key==pygame.K_n:
                moneyGo=True
            maps.append((x,y))

    pygame.draw.rect(screen,'red',rect1,0)
    if rect1.colliderect(my) or moneyGo:
        # tkinter.messagebox.showinfo('提示','恭喜你，成功通过第'+str(level)+'关！')
        x=55
        y=54
        level+=1
        h1,m1,s1=h,m,s
        maps=[(55,54)]
        a=True
        b=False
        blues=False
        reds=False
        screen.fill((255,255,255))
        obj=""
        with open("Maze_Game_conf_File\\data.mgcf","r",encoding='utf-8') as file:
            ob=file.readlines()[2:]
        for i in ob:
            obj+=i
        if moneyGo:
            get_coin=get_coin-int(this_coin/2)
        with open("Maze_Game_conf_File\\data.mgcf", "w", encoding='utf-8') as file:
            file.write("{}\n{}\n".format(get_coin,get_lightning))
            file.write(obj)
            file.write("{}\n".format(nowsss))
            file.write("{}×{}\n".format(grid_size[0],grid_size[1]))
            file.write(str(level)+"\n")
            file.write("{:0>2}:{:0>2}:{:0>2}\n".format(str(h2),str(m2),str(s2)))
            file.write("{}\n".format(str(pauses)))
            if len(pauses_time)!=0:
                for i in pauses_time:
                    file.write("{:0>2}:{:0>2}:{:0>2}".format(i.split(":")[0],i.split(":")[1],i.split(":")[2])+"\n")
            else:
                file.write("No pause time.\n")
            file.write("{}\n".format(steps))
            file.write("{}\n".format(get_lightning))
            file.write("{}\n".format(get_coin))
            file.write("{}\n".format(this_lightning))
            file.write("{}\n".format(this_coin))
            file.write("{}\n".format("是" if moneyGo else "否"))
            file.write("{}\n".format("是" if not secret else "否"))
        screen.blit(font8.render("成功通过第{}关！".format(level-1),True,(255,0,0)),((900-(7+len(list(str(level))))*30)/2,200))
        screen.blit(font7.render("耗时：{:0>2}:{:0>2}:{:0>2}".format(h2,m2,s2),True,"#48D1CC"),(int((900-(3+len(list(str(h2)))+len(list(str(m2)))+len(list(str(s2))))*30)/2),280+10))
        screen.blit(font7.render("获得金币数：{}".format(int(this_coin / (1 + moneyGo))), True, "#48D1CC"), (int((900 - (3 + len(list(str(get_coin)))) * 30) / 2), 280 + 30 * 2))
        screen.blit(font7.render("获得能量值：{}".format(this_lightning),True,"#48D1CC"),(int((900-(3+len(list(str(get_lightning))))*30)/2),280+30*4))
        screen.blit(font7.render("步数：{}".format(steps),True,"#48D1CC"),(int((900-(3+len(list(str(steps))))*30)/2),280+30*6))

        use_xiang_su=len(list(str(ScreenShot_Time)))*15+5*30+540
        use_xiang_su2=use_xiang_su+120
        color_of_show='blue'
        screen.blit(pygame.transform.scale(J,(120,120)),(0,570))

        while a:
            if screenShot:
                screen.blit(font7.render("点击查看",True,color_of_show),(use_xiang_su,780))
            else:
                screen.blit(font7.render("~没有记录精彩瞬间哦，下次探索新功能~",True,color_of_show),(180,690))
            for event4 in pygame.event.get():
                if b:
                    b=False
                xx,yy=pygame.mouse.get_pos()
                if event4.type == pygame.MOUSEBUTTONDOWN:
                    if 850<=yy<=890:
                        if 20<=xx<=440:
                            a=False
                            home(True)
                        elif 450<=xx<=450+420:
                            a=False
                    if use_xiang_su <= xx <= use_xiang_su2 and 780 <= yy <= 810 and screenShot:
                        os.system("explorer "+os.getcwd()+"\\Maze_Game_conf_File\\ScreenShot")
                elif event4.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event4.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen,(255,255,255),(0,900-45-20,900,70))
                    if use_xiang_su<=xx<=use_xiang_su2 and 780<=yy<=810 and screenShot:
                        color_of_show='red'
                    else:
                        color_of_show='blue'
                    if 850 <= yy <= 890:
                        if 20 <= xx <= 440:
                            draw_button(screen, (20, 900 - 50), 420, 40, "#00BFFF", "#00BFFF", 4)
                            draw_button(screen, (20 + 20 + 420, 900 - 50), 420, 40, (255, 0, 0), (255, 255, 255), 4)
                            screen.blit(font7.render("↙返回主页", True, "white"), (20 + 200-50, 900 - 55 + 10))
                            screen.blit(font7.render("下一关↘", True, "red"), (20 + 420 + 20 + 200 - 30, 900 - 55 + 10))
                            b=True
                            blues=True
                            reds=False
                        else:
                            draw_button(screen, (20, 900 - 50), 420, 40, "#00BFFF", (255, 255, 255), 4)
                            draw_button(screen, (20 + 20 + 420, 900 - 50), 420, 40, (255, 0, 0), (255, 255, 255), 4)
                            screen.blit(font7.render("↙返回主页", True, "#00BFFF"), (20 + 200-50, 900 - 55 + 10))
                            screen.blit(font7.render("下一关↘", True, "red"), (20 + 420 + 20 + 200 - 30, 900 - 55 + 10))
                            blues=False
                        if 450 <= xx <= 450 + 420:
                            draw_button(screen, (20, 900 - 50), 420, 40, "#00BFFF", (255, 255, 255), 4)
                            draw_button(screen, (20 + 20 + 420, 900 - 50), 420, 40, (255, 0, 0), (255, 0, 0), 4)
                            screen.blit(font7.render("↙返回主页", True, "#00BFFF"), (20 + 200-50, 900 - 55 + 10))
                            screen.blit(font7.render("下一关↘", True, "white"), (20 + 420 + 20 + 200 - 30, 900 - 55 + 10))
                            b=True
                            reds=True
                        else:
                            draw_button(screen, (20, 900 - 50), 420, 40, "#00BFFF", (255, 255, 255), 4)
                            draw_button(screen, (20 + 20 + 420, 900 - 50), 420, 40, (255, 0, 0), (255, 255, 255), 4)
                            screen.blit(font7.render("↙返回主页", True, "#00BFFF"), (20 + 200-50, 900 - 55 + 10))
                            screen.blit(font7.render("下一关↘", True, "red"), (20 + 420 + 20 + 200 - 30, 900 - 55 + 10))
                            blues=False
                if reds:
                    draw_button(screen, (20, 900 - 50), 420, 40, "#00BFFF", (255, 255, 255), 4)
                    draw_button(screen, (20 + 20 + 420, 900 - 50), 420, 40, (255, 0, 0), (255, 0, 0), 0)
                    screen.blit(font7.render("↙返回主页", True, "#00BFFF"), (20 + 200-50, 900 - 55 + 10))
                    screen.blit(font7.render("下一关↘", True, "white"), (20 + 420 + 20 + 200 - 30, 900 - 55 + 10))
                if blues:
                    draw_button(screen, (20, 900 - 50), 420, 40, "#00BFFF", "#00BFFF", 0)
                    draw_button(screen, (20 + 20 + 420, 900 - 50), 420, 40, (255, 0, 0), (255, 255, 255), 4)
                    screen.blit(font7.render("↙返回主页", True, "white"), (20 + 200-50, 900 - 55 + 10))
                    screen.blit(font7.render("下一关↘", True, "red"), (20 + 420 + 20 + 200 - 30, 900 - 55 + 10))
                if not b:
                    draw_button(screen, (20, 900 - 50), 420, 40, "#00BFFF", (255, 255, 255), 4)
                    draw_button(screen, (20 + 20 + 420, 900 - 50), 420, 40, (255, 0, 0), (255, 255, 255), 4)
                    screen.blit(font7.render("↙返回主页", True, "#00BFFF"), (20 + 200-50, 900 - 55 + 10))
                    screen.blit(font7.render("下一关↘", True, "red"), (20 + 420 + 20 + 200 - 30, 900 - 55 + 10))
                    pygame.draw.circle(screen,(255,255,255),(20 + 20 + 420+20, 900 - 50+20),16)
                    pygame.draw.circle(screen,(255,255,255),(20 + 20 + 400+420, 900 - 50+20),16)
                    pygame.draw.circle(screen,(255,255,255),(20+20, 900 - 50+20),16)
                    pygame.draw.circle(screen,(255,255,255),(20+400, 900 - 50+20),16)
            pygame.display.update()
        steps=0
        get_level+=1
        moneyGo=False
        h2=m2=s2=0
        screen_shot_list=[]
        screenShot=False
        ScreenShot_Time=0
        run()
    write_s=s
    pygame.display.update()