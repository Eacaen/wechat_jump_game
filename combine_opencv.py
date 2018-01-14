# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import time
import random
import math


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
  
def get_jumper(canny_img , rgb_img = 0):
    # 利用边缘检测的结果寻找物块的上沿和下沿
    # 进而计算物块的中心点
    H, W = canny_img.shape
    jumper_left_x = []
    jumper_left_y = []

    jumper_right_x = []
    jumper_right_y = []

    search_area_top = int(H/3)
    search_area_bottom = int(2*H/3)

    search_area_left  = int(0.1*W)
    search_area_right = int(0.9*W)


    base = [102, 60 , 54 ] #BGR 在最下面的几个像素
    DIFF_THERESHOLD = 2
    
    for row in range( search_area_left , search_area_right):
        for col in range( search_area_top , search_area_bottom ):
            pixel = rgb_img[ col , row ]
            pixel_prv = canny_img[ col +1, row  ]
            pixel_prv2 = canny_img[ col +2, row  ]

            if colorDiff( pixel , base) < DIFF_THERESHOLD and ( pixel_prv != 0 or pixel_prv2 != 0):
                jumper_left_x.append(row)
                jumper_left_y.append(col)

#不一定要来回照两遍
    # for row in range( search_area_right , search_area_left , -1 ):
    #     for col in range( search_area_top , search_area_bottom ):
    #         pixel = rgb_img[ col , row ]
    #         pixel_prv = canny_img[ col +1, row  ]
    #         pixel_prv2 = canny_img[ col +2, row  ]

    #         if colorDiff( pixel , base) < DIFF_THERESHOLD and ( pixel_prv != 0 or pixel_prv2 != 0):
    #             jumper_right_x.append(row)
    #             jumper_right_y.append(col)

    x_center = (sum(jumper_left_x)+sum(jumper_right_x))// (len(jumper_left_x)+len(jumper_right_x))
    y_center = -18 + (sum(jumper_left_y)+sum(jumper_right_y))// (len(jumper_left_y)+len(jumper_right_y))

    return canny_img, x_center, y_center

def colorDiff(p1, p2):
    r0 = abs(int(p1[0]) - int(p2[0]))
    r1 = abs(int(p1[1]) - int(p2[1]))
    r2 = abs(int(p1[2]) - int(p2[2]))
    res = r0+r1+r2
    return res


def get_center(canny_img , rgb_img = 0):
    # 利用边缘检测的结果寻找物块的上沿和下沿
    # 进而计算物块的中心点
    y_top = np.nonzero([max(row) for row in canny_img[500:]])[0][0] + 500
    x_top = int(np.mean(np.nonzero(canny_img[y_top])))

    base = rgb_img[ y_top+1 , x_top]

    # print 'base color' , base , y_top , x_top
    # print 'top canny像素',canny_img[x_top , y_top]
    # print 'top rgb像素',base

    H, W = canny_img.shape
    # print H,W
    y_bottom = y_top + 280
    DIFF_THERESHOLD = 9
    white_center_top = 0
    white_center_bottom = 0

    for row in range( y_top , y_bottom):
                #如果有的话，找中心白点
        pixel = rgb_img[ row ,x_top ]
        pixel_prv = rgb_img[ row-2 ,x_top ]
        pixel_next = rgb_img[ row+2 ,x_top ]

        if colorDiff( pixel , [245 , 245 , 245 ]) == 0 and colorDiff( pixel_prv , [245 , 245 , 245 ]) != 0:
            if white_center_top == 0:
                white_center_top = row
                y_top = row
                continue
        if colorDiff( pixel , [245 , 245 , 245 ]) == 0 and colorDiff( pixel_next , [245 , 245 , 245 ]) != 0:
                white_center_bottom = row
                y_bottom = row
                print '----------------------------->跳到中心<-----------------------------'
            
                x_center, y_center = x_top, (y_top + y_bottom) // 2
                return canny_img, x_center, y_center

    for row in range( y_bottom , y_top, -1 ):
        pixel = rgb_img[ row ,x_top ]
                #找相同颜色，从下向上找，如果从上往下，带来诸多问题
        diff = colorDiff( pixel , base)
        if diff < DIFF_THERESHOLD and \
            (canny_img[row+2, x_top] != 0 or canny_img[row+1, x_top] != 0 or \
            canny_img[row , x_top-1] != 0 or canny_img[row, x_top+1] != 0 ) \
            and row >y_top+11 :
            print '----------------------------->匹配色<-----------------------------'
            y_bottom = row
            break

    x_center, y_center = x_top, (y_top + y_bottom) // 2
    return canny_img, x_center, y_center


def find_jumper_and_board(imgPath,\
    Target='/home/eacaen/桌面/科赛/my_wechart_jump_game/temp_player.png',\
    value=0.7,\
     show = False,\
     time=0):
    """
    寻找关键坐标
    """ 

#模板匹配，找到小人
    # max_loc1_x ,max_loc1_y , w,  h = mathc_img(imgPath,Target,value)

    # x_jumper , y_jumper = max_loc1_x + int(w/2)+2 , max_loc1_y + 185

    img_rgb = cv2.imread(imgPath)

    img_gauss = cv2.GaussianBlur(img_rgb, (5,5), 0)

    canny_img = cv2.Canny(img_gauss, 1, 10)
    H, W = canny_img.shape

#不使用模板，直接找
    canny_img, x_jumper , y_jumper = get_jumper(canny_img , img_rgb)

    # 消去小人轮廓对边缘检测结果的干扰
    for k in range(y_jumper - 300, y_jumper + 50):
        for b in range(x_jumper - 60, x_jumper + 60):
            canny_img[k][b] = 0

    canny_img, x_center, y_center = get_center(canny_img , img_rgb)

    if show:
        cv2.circle(canny_img, (x_center, y_center), 10, 255, -1)
        cv2.circle(canny_img, (x_jumper, y_jumper), 10, 255, -1)

        cv2.namedWindow("guass",cv2.WINDOW_NORMAL)  
        cv2.imshow('guass',canny_img)
        cv2.waitKey(time)
        cv2.destroyAllWindows()

    return x_jumper , y_jumper , x_center, y_center

if __name__ == '__main__':
    imgDir = '/home/eacaen/桌面/科赛/img'
    imgPath = random.choice(list(os.path.join(imgDir, name) for name in os.listdir(imgDir)))
    print imgPath

    imgPath = imgDir + '/98.png'
    find_jumper_and_board(imgPath, show =1)

    # imgPath = imgDir + '/449.png'
    # find_jumper_and_board(imgPath, show =1)

    # for name in os.listdir(imgDir):
    #     imgPath =  os.path.join(imgDir, name)
    #     print imgPath
    #     find_jumper_and_board(imgPath, show = 0)

    # for i in range(550,650):
    #     imgPath =  '/home/eacaen/桌面/科赛/img/'+str(i)+'.png'
    #     print imgPath
    #     find_jumper_and_board(imgPath, show = 1) 
    #     import time
    #     time.sleep(2)
