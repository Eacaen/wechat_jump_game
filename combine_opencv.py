# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import time
import random

def mathc_img(image,Target,value):
    img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(Target,0)

    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)

    min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res)
    # print  min_val1, max_val1, min_loc1, max_loc1 

    if max_val1 > value:
        return max_loc1[0] ,max_loc1[1] , w,  h
    else:
        return 0
  


def get_center(canny_img ):
    # 利用边缘检测的结果寻找物块的上沿和下沿
    # 进而计算物块的中心点
    y_top = np.nonzero([max(row) for row in canny_img[850:]])[0][0] + 850
    x_top = int(np.mean(np.nonzero(canny_img[y_top])))

    H, W = canny_img.shape
    print H,W
    y_bottom = y_top + 80
    for row in range(y_bottom, H):
        if canny_img[row, x_top] != 0:
            y_bottom = row
            break
    print y_top, y_bottom
    x_center, y_center = x_top, (y_top + y_bottom) // 2
    return canny_img, x_center, y_center


def find_jumper_and_board(imgPath,\
    Target='/home/eacaen/桌面/科赛/my_wechart_jump_game/temp_player.png',\
    value=0.7,\
     show = False):
    """
    寻找关键坐标
    """ 
    max_loc1_x ,max_loc1_y , w,  h = mathc_img(imgPath,Target,value)

    x_jumper , y_jumper = max_loc1_x + int(w/2) , max_loc1_y + 190

    img_rgb = cv2.imread(imgPath)

    img_gauss = cv2.GaussianBlur(img_rgb, (5,5), 0)

    canny_img = cv2.Canny(img_gauss, 1, 10)
    H, W = canny_img.shape

    # 消去小跳棋轮廓对边缘检测结果的干扰
    for k in range(max_loc1_y - 200, max_loc1_y + 200):
        for b in range(max_loc1_x - 10, max_loc1_x + 100):
            canny_img[k][b] = 0

    canny_img, x_center, y_center = get_center(canny_img)

    if show:
        cv2.circle(canny_img, (x_center, y_center), 10, 255, -1)
        cv2.circle(canny_img, (x_jumper, y_jumper), 10, 255, -1)

        cv2.namedWindow("guass",cv2.WINDOW_NORMAL)  
        cv2.imshow('guass',canny_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return x_jumper , y_jumper , x_center, y_center

if __name__ == '__main__':
    imgDir = '/home/eacaen/桌面/科赛/img'
    imgPath = random.choice(list(os.path.join(imgDir, name) for name in os.listdir(imgDir)))
    print imgPath

    imgPath = imgDir + '/201.png'
    find_jumper_and_board(imgPath, show =1)

    # for name in os.listdir(imgDir):
    #     imgPath =  os.path.join(imgDir, name)
    #     print imgPath
    #     find_jumper_and_board(imgPath, show = 0)

    # for i in range(200,250):
    #     imgPath =  '/home/eacaen/桌面/科赛/img/'+str(i)+'.png'
    #     print imgPath
    #     find_jumper_and_board(imgPath, show = 1) 
