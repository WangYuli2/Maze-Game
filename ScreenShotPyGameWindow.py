"""
@author: 王俞励
"""
import time
import win32gui, win32ui, win32con, win32api
import GetWindowNumber
import win32clipboard as clip
from ctypes import *
from PIL import Image
import os,io
def copy(imagepath):
    img = Image.open(imagepath)
    output = io.BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    clip.OpenClipboard()
    clip.EmptyClipboard()
    clip.SetClipboardData(win32con.CF_DIB, data)  # 图片
    clip.CloseClipboard()
def window_capture(filename,find):
    GetWindowNumber.main()
    num=0
    for k,v in GetWindowNumber.hwnd_title.items():
        if v and v == find:
            num=k
    hwnd = num  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][3]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, 900, 900)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (900, 900), mfcDC, (0, 0), win32con.SRCCOPY)
    fuben_NUM=2
    filename2=filename
    #filename2为filename的副本。fuben_NUM为副本数量
    while os.path.exists(os.getcwd()+"\\Maze_Game_conf_File\\ScreenShot\\"+filename2):#如果文件名"Maze_game_Screen_Shot{s}.png"存在，就要去/加括号s+1
        #将filename2拆分为['Maze_Game_Screen_Shot', 'png']取'Maze_Game_Screen_Shot'+'（[副本数]）'+'.png'，做成文件名
        filename2="Maze_Game_Screen_Shot"+f"（{fuben_NUM}）"+".png"
        fuben_NUM+=1#副本数+1
    saveBitMap.SaveBitmapFile(saveDC, os.getcwd()+"\\Maze_Game_conf_File\\ScreenShot\\"+filename2)
    copy(os.getcwd()+"\\Maze_Game_conf_File\\ScreenShot\\"+filename2)
    return fuben_NUM-1 #TODO TODO TODO TODO 返回的是第n个截屏！！！！
def main():
    return window_capture("Maze_Game_Screen_Shot.png","Maze Game's window, version 1.0.2")