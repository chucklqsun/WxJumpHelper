#!/usr/bin/env python
import cv2
from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import subprocess
import random
import matplotlib.patches as patches

click_data = []


def call_cmd(cmd):
    s = subprocess.check_output(cmd.split())
    return s.decode("utf-8").split('\n')


rr = None


def on_motion(event):
    global ax, rr, click_data
    # if rr is not None:
    #     rr.set_visible(False)
    # Create a Rectangle patch
    # rect = patches.Rectangle((event.xdata, event.ydata), 40, 30, linewidth=1, edgecolor='r', facecolor='none')

    # Add the patch to the Axes
    # if event.xdata and event.ydata:
    #     rr = patches.Rectangle([event.xdata-40, event.ydata-15], 80, 30, linewidth=1, edgecolor='r', facecolor='none')
    #     if len(click_data) == 0:
    #         ax.add_patch(rr)


def onclick(event):
    global fig
    global click_data
    """Deal with click events"""
    button = ['left', 'middle', 'right']
    toolbar = plt.get_current_fig_manager().toolbar
    if toolbar.mode != '':
        print("You clicked on something, but toolbar is in mode {:s}.".format(toolbar.mode))
    else:
        click_data.append([event.xdata, event.ydata])
        print("You {0}-clicked coords ({1},{2}) (pix ({3},{4}))".format(button[event.button+1],\
                                                                         event.xdata,\
                                                                         event.ydata,\
                                                                         event.x,\
                                                                         event.y))
        distance_2 = (click_data[0][0] - click_data[1][0])*(click_data[0][0] - click_data[1][0]) + \
                     (click_data[0][1] - click_data[1][1])*(click_data[0][1] - click_data[1][1])
        distance = pow(distance_2, 0.5)
        print("Distance is {}".format(distance))
        # delay = int(distance/540*806)
        delay = int(distance/540*770)   # change to your value properly
        x1 = round(random.randint(100, 500)+random.random(), 3)
        y1 = round(random.randint(100, 500)+random.random(), 3)
        x2 = round(x1+random.random(), 3)
        y2 = round(y1+random.random(), 3)
        call_cmd("adb shell input swipe {} {} {} {} {}".format(x1, y1, x2, y2, delay))
        plt.pause(0.9)
        plt.close()


def main():
    global ax
    global fig
    global click_data
    cmd = [
        'adb shell screencap -p /sdcard/screenshot.png',
        'adb pull /sdcard/screenshot.png',
    ]
    while True:
        plt.close()
        global click_data
        click_data = []
        call_cmd(cmd[0])
        call_cmd(cmd[1])
        screenshot = mpimg.imread('screenshot.png')
        print(screenshot.shape)

        # imread()函数读取目标图片和模板
        img_rgb = cv2.imread("screenshot.png", 0)
        template = cv2.imread('bottle.png', 0)

        # matchTemplate 函数：在模板和输入图像之间寻找匹配,获得匹配结果图像
        # minMaxLoc 函数：在给定的矩阵中寻找最大和最小值，并给出它们的位置
        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print("%s,%s,%s,%s" % (min_val, max_val, min_loc, max_loc))
        bottle_center = [max_loc[0]+40, max_loc[1]+185]
        click_data.append(bottle_center)

        plt.subplots(figsize=(12, 10))
        ax = plt.gca()
        fig = plt.gcf()

        img = cv2.GaussianBlur(img_rgb, (5, 5), 0)
        canny = cv2.Canny(img, 1, 10)
        implot = ax.imshow(canny)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        fig.canvas.mpl_connect('motion_notify_event', on_motion)
        cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

        rr = patches.Rectangle(bottle_center, 1, 1, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rr)

        plt.show()


if __name__ == '__main__':
    print("Welcome")
    main()
