#!/usr/bin/env python
import cv2
from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import subprocess
import random
import matplotlib.patches as patches

coefficient = 1.5   # modify for your resolution, e.g. 1280 to 1920 is x1.5, 1920 to 1920 is x1.0
click_data = []
debug = False
rr = None


def get_height():
    info = call_cmd("adb shell wm size")
    height = info[0].split("x")[1]
    print("Height {}".format(height))
    return height


def call_cmd(cmd):
    s = subprocess.check_output(cmd.split())
    return s.decode("utf-8").split('\n')


def get_object_center(img, bottle_filter):
    pin_point = []
    for i in range(int(len(img)/5), int(len(img)*2/3)):
        for j in range(100, len(img[i])-100):
            if img[i][j] != 0 and (j < (bottle_filter[0]-5) or j > (bottle_filter[0]+int(90/coefficient))):
                # print("%s,%s,%s" % (i, j, img[i][j]))
                pin_point.append([j, i])
        if len(pin_point) > 0:
            break
    center_top = [int((pin_point[0][0] + pin_point[-1][0])/2), pin_point[0][1]]
    center = [center_top[0], center_top[1]+int(80/coefficient)]
    # supposed border width is 5 pix
    # for i in range(center_top[1]+5, int(len(img)*2/3)):
    #     if img[i, center_top[0]] == 255:
    #         center[1] = int((i+center_top[1])/2)
    #         break
    return center


# def on_motion(event):
#     global ax, rr, click_data
    # if rr is not None:
    #     rr.set_visible(False)
    # Create a Rectangle patch
    # rect = patches.Rectangle((event.xdata, event.ydata), 40, 30, linewidth=1, edgecolor='r', facecolor='none')

    # Add the patch to the Axes
    # if event.xdata and event.ydata:
    #     rr = patches.Rectangle([event.xdata-40, event.ydata-15], 80, 30, linewidth=1, edgecolor='r', facecolor='none')
    #     if len(click_data) == 0:
    #         ax.add_patch(rr)


def jump(self_kill=False):
    global fig
    global click_data
    distance_2 = (click_data[0][0] - click_data[1][0]) * (click_data[0][0] - click_data[1][0]) + \
                 (click_data[0][1] - click_data[1][1]) * (click_data[0][1] - click_data[1][1])
    distance = pow(distance_2, 0.5)
    print("Distance is {}".format(distance))
    # delay = int(distance/540*806)
    delay = int(distance / 540 * (755*coefficient))  # change to your value properly, 1080*1920=>755
    x1 = round(random.randint(100, 500) + random.random(), 3)
    y1 = round(random.randint(100, 500) + random.random(), 3)
    x2 = round(x1 + random.random(), 3)
    y2 = round(y1 + random.random(), 3)
    if self_kill:
        delay = int(delay*1.3)
        print("delay is:%s" % delay)
    call_cmd("adb shell input swipe {} {} {} {} {}".format(x1, y1, x2, y2, delay))
    plt.pause(1.2)
    plt.close()
    return


# def onclick(event):
#     global fig
#     global click_data
#     """Deal with click events"""
#     button = ['left', 'middle', 'right']
#     toolbar = plt.get_current_fig_manager().toolbar
#     if toolbar.mode != '':
#         print("You clicked on something, but toolbar is in mode {:s}.".format(toolbar.mode))
#     else:
#         click_data.append([event.xdata, event.ydata])
#         print("You {0}-clicked coords ({1},{2}) (pix ({3},{4}))".format(button[event.button+1],\
#                                                                          event.xdata,\
#                                                                          event.ydata,\
#                                                                          event.x,\
#                                                                          event.y))


def main():
    global coefficient
    coefficient = 1920/int(get_height())
    learning_seq = []
    # 30-80: 240
    # 50-110:730
    for i in range(0, 5):   # default jump 5 rounds
        learning_seq.append(random.randint(50, 110))
    cur_jump_count = 0
    learning_idx = 0
    global ax
    global fig
    global click_data
    cmd = [
        'adb shell screencap -p /sdcard/screenshot.png',
        'adb pull /sdcard/screenshot.png',
    ]
    while True:
        if learning_idx >= len(learning_seq):
            break

        plt.close()
        global click_data
        click_data = []
        if not debug:
            call_cmd(cmd[0])
            call_cmd(cmd[1])
        screenshot = mpimg.imread('screenshot.png')
        print(screenshot.shape)

        # imread()函数读取目标图片和模板
        img_rgb = cv2.imread("screenshot.png", 0)
        template = cv2.imread('bottle.png', 0)
        template = cv2.resize(template, None, fx=1/coefficient, fy=1/coefficient, interpolation=cv2.INTER_CUBIC)

        # matchTemplate 函数：在模板和输入图像之间寻找匹配,获得匹配结果图像
        # minMaxLoc 函数：在给定的矩阵中寻找最大和最小值，并给出它们的位置
        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print("%s,%s,%s,%s" % (min_val, max_val, min_loc, max_loc))
        bottle_center = [max_loc[0]+int(40/coefficient), max_loc[1]+int(185/coefficient)]
        click_data.append(bottle_center)

        # plt.subplots(figsize=(6, 5))
        plt.subplots(figsize=(0, 0))
        ax = plt.gca()
        fig = plt.gcf()

        img = cv2.GaussianBlur(img_rgb, (5, 5), 0)
        canny = cv2.Canny(img, 1, 10)
        object_center = get_object_center(canny, max_loc)
        click_data.append(object_center)


        implot = ax.imshow(canny)
        # cid = fig.canvas.mpl_connect('button_press_event', onclick)
        # fig.canvas.mpl_connect('motion_notify_event', on_motion)
        cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

        rb = patches.Rectangle(object_center, 1, 1, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rb)

        rr = patches.Rectangle(bottle_center, 1, 1, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rr)

        print("Round:%s-%s Leap: %s-%s" %
              (len(learning_seq), learning_idx+1, learning_seq[learning_idx], cur_jump_count + 1))
        if cur_jump_count < learning_seq[learning_idx]:
            print("to jump")
            cur_jump_count += 1
            jump()
        elif cur_jump_count == learning_seq[learning_idx]:
            print("to self KILL")
            cur_jump_count += 1
            jump(self_kill=True)
        else:
            plt.pause(10)
            print("to restart")
            cur_jump_count = 0
            learning_idx += 1
            # restart game
            call_cmd("adb shell input tap %s %s" % (random.randint(int(400/coefficient), int(700/coefficient)),
                                                    random.randint(int(1500/coefficient), int(1600/coefficient))))
            plt.pause(5)
            plt.close()
        plt.show()


if __name__ == '__main__':
    print("Welcome")
    main()
    print("Done")
