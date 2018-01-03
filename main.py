#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import subprocess


click_data = []


def call_cmd(cmd):
    s = subprocess.check_output(cmd.split())
    return s.decode("utf-8").split('\n')


def onclick(event):
    global click_data
    """Deal with click events"""
    button = ['left','middle','right']
    toolbar = plt.get_current_fig_manager().toolbar
    if toolbar.mode!='':
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
            distance_2 = pow(click_data[0][0] - click_data[1][0], 2) + pow(click_data[0][1] - click_data[1][1], 2)
            distance = pow(distance_2, 0.5)
            print("Distance is {}".format(distance))
            delay = int(distance/500*740)
            call_cmd("adb shell input swipe 100 100 100 100 {}".format(delay))


def main():
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

        ax = plt.gca()
        fig = plt.gcf()
        implot = ax.imshow(screenshot)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()


if __name__ == '__main__':
    print("Welcome")
    main()
