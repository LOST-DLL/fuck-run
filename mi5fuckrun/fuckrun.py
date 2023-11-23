from pyautogui import *
from cnocr import CnOcr
import math
from PIL import Image,ImageDraw,ImageFont
import win32gui

#dev stands for device
dev_window=win32gui.FindWindow(None,'MI 5')
dev_region=win32gui.GetWindowRect(dev_window)
dev_left=dev_region[0]
dev_top=dev_region[1]
dev_width=dev_region[2]-dev_region[0]
dev_height=dev_region[3]-dev_region[1]
dev_region=(dev_region[0],dev_region[1],dev_width,dev_height)
radius=75
#radius=87

map_region=(dev_left+7,dev_top+203,527,558)
#screenshot('MI5.png',map_region)

def get_player():
    #player=locateOnScreen('player.png',region=map_region,confidence=0.65)
    #print('player',player) the camera follows so no need to get_player QWQ
    player=(dev_left+271,dev_top+512)
    return player

def get_joy():
    flpannel=locateOnScreen('pannel.png',region=dev_region,confidence=0.4)
    #print((flpannel[0],flpannel[1]))
    joy=(flpannel[0]+40,flpannel[1]-100)
    return joy

def get_tg():
    tg_region=(dev_region[0]+180,dev_region[1]+224,180,34)
    screenshot('target.png',region=tg_region)
    ocr=CnOcr()
    res=ocr.ocr('target.png')
    #print(res)
    if res==[]:return None
    for char in res[0]['text']:
        if char.isdigit():return char

def zoom():
    moveTo(dev_left+30,dev_top+650)
    click()
    keyDown('ctrl')
    mouseDown()
    move(0,+75,0.5)
    mouseUp()
    keyUp('ctrl')

def get_loc():
    loc=locateOnScreen('topic.png',region=map_region,confidence=0.45)
    print(loc)
    return (loc[0]+22,loc[1]+87)

def update():
    loc=get_loc()
    pl=get_player()
    x=loc[0]-pl[0]
    y=loc[1]-pl[1]
    if x==0:x=0.0000000000001
    theta=math.atan(math.fabs(y/x))
    joy=get_joy()
    if x>=0:f1=1
    else:f1=-1

    if y>=0:f2=1
    else :f2=-1

    put=(joy[0]+radius*f1*math.cos(theta),joy[1]+radius*f2*math.sin(theta))
    return put

def run_more():
    x=dev_region[0]+54
    y=dev_region[1]+122
    return pixel(x,y)!=(33,33,33)

limit=50
#make sure it can stop when your mouse cant be used QWQ

print('Ready go!')
while get_tg()!=None or run_more():
    try:
        put=update()
    except ImageNotFoundException:
        zoom()
        limit-=1
        if limit==0:
            mouseUp()
            moveTo(dev_left+210,dev_top+770)
            click()
            print('Somthing went wrong,auto pause😢')
            exit(0)
    else:
        moveTo(put[0],put[1])
        mouseDown()
        sleep(5)

mouseUp()
moveTo(dev_left+210,dev_top+770)
click()
print('Work complete,thanks for using😘')