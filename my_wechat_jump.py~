# -*- coding: utf-8 -*-

"""
=== 思路 ===
核心：每次落稳之后截图，根据截图算出棋子的坐标和下一个块顶面的中点坐标，
    根据两个点的距离乘以一个时间系数获得长按的时间
识别棋子：靠棋子的颜色来识别位置，通过截图发现最下面一行大概是一条
    直线，就从上往下一行一行遍历，比较颜色（颜色用了一个区间来比较）
    找到最下面的那一行的所有点，然后求个中点，求好之后再让 Y 轴坐标
    减小棋子底盘的一半高度从而得到中心点的坐标
识别棋盘：靠底色和方块的色差来做，从分数之下的位置开始，一行一行扫描，
    由于圆形的块最顶上是一条线，方形的上面大概是一个点，所以就
    用类似识别棋子的做法多识别了几个点求中点，这时候得到了块中点的 X
    轴坐标，这时候假设现在棋子在当前块的中心，根据一个通过截图获取的
    固定的角度来推出中点的 Y 坐标
最后：根据两点的坐标算距离乘以系数来获取长按时间（似乎可以直接用 X 轴距离）
"""
from __future__ import print_function, division
import os
import sys
import time
import math
import random
from PIL import Image
import cv2

from six.moves import input
try:
    from common import debug, config, screenshot
except Exception as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(-1)

import sys
sys.path.append("../wechat_jump_jump")
try:
        import combine_opencv
except Exception as ex:
    print(ex)
    print('请检查项目目录中的 combine_opencv.py 文件是否存在')
    exit(-1)


VERSION = "1.1.1"

# DEBUG 开关，需要调试的时候请改为 True，不需要调试的时候为 False
DEBUG_SWITCH = False


# Magic Number，不设置可能无法正常执行，请根据具体截图从上到下按需
# 设置，设置保存在 config 文件夹中
config = config.open_accordant_config()
under_game_score_y = config['under_game_score_y']
# 长按的时间系数，请自己根据实际情况调节
press_coefficient = config['press_coefficient']
# 二分之一的棋子底座高度，可能要调节
piece_base_height_1_2 = config['piece_base_height_1_2']
# 棋子的宽度，比截图中量到的稍微大一点比较安全，可能要调节
piece_body_width = config['piece_body_width']

def file_num(path= '/home/eacaen/桌面/科赛/img'):
    count = 0
    for root,dirs,files in os.walk(path):    #遍历统计
          for each in files:
                 count += 1   #统计文件夹下文件个数
    return count               #输出结果

def set_button_position(im):
    """
    将 swipe 设置为 `再来一局` 按钮的位置
    """
    global swipe_x1, swipe_y1, swipe_x2, swipe_y2
    w, h = im.size
    left = int(w / 2)
    top = int(1584 * (h / 1920.0))
    left = int(random.uniform(left-50, left+50))
    top = int(random.uniform(top-10, top+10))    # 随机防 ban
    swipe_x1, swipe_y1, swipe_x2, swipe_y2 = left, top, left, top


def jump(distance):
    """
    跳跃一定的距离
    """
    press_time = distance * press_coefficient
    press_time = max(press_time, 100)   # 设置 200ms 是最小的按压时间
    press_time = int(press_time)
    cmd = 'adb shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=swipe_x1,
        y1=swipe_y1,
        x2=swipe_x2,
        y2=swipe_y2,
        duration=press_time+40
    )
    print(cmd)
    os.system(cmd)
    return press_time



def yes_or_no(prompt, true_value='y', false_value='n', default=True):
    """
    检查是否已经为启动程序做好了准备
    """
    default_value = true_value if default else false_value
    prompt = '{} {}/{} [{}]: '.format(prompt, true_value,
        false_value, default_value)
    i = input(prompt)
    if not i:
        return default
    while True:
        if i == true_value:
            return True
        elif i == false_value:
            return False
        prompt = 'Please input {} or {}: '.format(true_value, false_value)
        i = input(prompt)


def main():
    """
    主函数
    """
    op = yes_or_no('请确保手机打开了 ADB 并连接了电脑，'
                   '然后打开跳一跳并【开始游戏】后再用本程序，确定开始？')
    if not op:
        print('bye')
        return
    print('程序版本号：{}'.format(VERSION))
    debug.dump_device_info()
    screenshot.check_screenshot()

    i, next_rest, next_rest_time = (0, random.randrange(3, 10),
                                    random.randrange(5, 10))

    count = file_num('../img') 
    jump_num = 0
    while True:

        jump_num = jump_num + 1
        print('------------>跳了'+str(jump_num)+'次<------------')

        time.sleep(0.5)
        screenshot.pull_screenshot()
        
        imgPath='../wechat_jump_game-master/autojump.png'

        im = Image.open(imgPath)

        img_rgb = cv2.imread(imgPath)
        count = count+1
        # cv2.imwrite('../img/'+'{}.png'.format(count), img_rgb)
        # print('-----****------>writing img to ../img/''{}.png'.format(count))

        # 获取棋子和 board 的位置
        piece_x, piece_y, board_x, board_y = combine_opencv.find_jumper_and_board(imgPath,show=False)
        
        ts = int(time.time())
        print(ts, piece_x, piece_y, board_x, board_y)
        set_button_position(im)
        jump(math.sqrt((board_x - piece_x) ** 2 + (board_y - piece_y) ** 2))
        if DEBUG_SWITCH:
            debug.save_debug_screenshot(ts, im, piece_x,
                                        piece_y, board_x, board_y)
            debug.backup_screenshot(ts)
        im.close()
        i += 1

        if i == 1000:
            print('已经连续打了 {} 下，休息 {}s'.format(i, next_rest_time))
            for j in range(next_rest_time):
                sys.stdout.write('\r程序将在 {}s 后继续'.format(next_rest_time - j))
                sys.stdout.flush()
                time.sleep(1)
            print('\n继续')
            i, next_rest, next_rest_time = (0, random.randrange(30, 100),
                                            random.randrange(10, 60))
        # 为了保证截图的时候应落稳了，多延迟一会儿，随机值防 ban
        time.sleep(random.uniform(0.9, 1.2))


if __name__ == '__main__':
    main()
