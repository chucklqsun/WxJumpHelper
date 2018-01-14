#!/usr/bin/env python
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
    if rr is not None:
        rr.set_visible(False)
    # Create a Rectangle patch
    # rect = patches.Rectangle((event.xdata, event.ydata), 40, 30, linewidth=1, edgecolor='r', facecolor='none')

    # Add the patch to the Axes
    if event.xdata and event.ydata:
        rr = patches.Rectangle([event.xdata-40, event.ydata-15], 80, 30, linewidth=1, edgecolor='r', facecolor='none')
        if len(click_data) == 0:
            ax.add_patch(rr)


def onclick(event):
    global fig
    global click_data
    """Deal with click events"""
    button = ['left', 'middle', 'right']
    toolbar = plt.get_current_fig_manager().toolbar
    if toolbar.mode != '':
        print("You clicked on something, but toolbar is in mode {:s}.".format(toolbar.mode))
    else:
        if len(click_data) < 2:
            print("You {0}-clicked coords ({1},{2}) (pix ({3},{4}))".format(button[event.button+1],\
                                                                             event.xdata,\
                                                                             event.ydata,\
                                                                             event.x,\
                                                                             event.y))
            click_data.append([event.xdata, event.ydata])
        if len(click_data) == 2:
            distance_2 = (click_data[0][0] - click_data[1][0])*(click_data[0][0] - click_data[1][0]) + \
                         (click_data[0][1] - click_data[1][1])*(click_data[0][1] - click_data[1][1])
            distance = pow(distance_2, 0.5)
            print("Distance is {}".format(distance))
            # delay = int(distance/540*806)
            delay = int(distance/540*780)   # change to your value properly
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

        plt.subplots(figsize=(12, 10))
        ax = plt.gca()
        fig = plt.gcf()
        implot = ax.imshow(screenshot)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        fig.canvas.mpl_connect('motion_notify_event', on_motion)
        cursor = Cursor(ax, useblit=True, color='red', linewidth=1)
        plt.show()


if __name__ == '__main__':
    print("Welcome")
    main()
