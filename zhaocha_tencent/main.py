import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import time

debug = False


def call_cmd(cmd):
    s = subprocess.check_output(cmd.split())
    return s.decode("utf-8").split('\n')


def diff_value(v1, v2, tol):
    if abs(v1 - v2) > tol:
        return True
    else:
        return False


def main():
    tolerance = 0.11
    step = 4
    cmd = [
        # 'adb shell screencap -p /sdcard/screenshot.png',
        'adb shell screencap /sdcard/screenshot.png',
        'adb pull /sdcard/screenshot.png',
    ]
    while True:
        plt.close()
        start = time.clock()

        if not debug:
            call_cmd(cmd[0])
            call_cmd(cmd[1])
            filename = 'screenshot.png'
        else:
            filename = '12836.png'
            # filename = 'screenshot.png'

        screenshot = mpimg.imread(filename)
        print(screenshot.shape)  # y, x
        center = [int(screenshot.shape[0]/2), int(screenshot.shape[1]/2)]

        height = 830
        width = 830
        offset_x1 = 72
        offset_y1 = 35
        offset_x2 = 72
        offset_y2 = 35

        output_img1 = np.zeros([height, width, screenshot.shape[2]])
        output_img2 = np.zeros([height, width, screenshot.shape[2]])
        part1 = [
            [center[0]-height-offset_y1, center[0]-offset_y1],    # y1->y2
            [center[1]-int(width/2)+offset_x1, center[1]+int(width/2)+offset_x1],    # x1->x2
        ]

        part2 = [
            [center[0]+offset_y2, center[0]+height+offset_y2],    # y1->y2
            [center[1]-int(width/2)+offset_x2, center[1]+int(width/2)+offset_x2],    # x1->x2
        ]

        output_img1[0:height, 0:width] = screenshot[part1[0][0]:part1[0][1], part1[1][0]:part1[1][1]]
        output_img2[0:height, 0:width] = screenshot[part2[0][0]:part2[0][1], part2[1][0]:part2[1][1]]
        for i in range(step, height-step, step):
            for j in range(step, width-step, step):
                if diff_value(output_img1[i, j][0], output_img2[i, j][0], tolerance) or \
                        diff_value(output_img1[i, j][1], output_img2[i, j][1], tolerance) or \
                        diff_value(output_img1[i, j][2], output_img2[i, j][2], tolerance):
                    for k in range(-step, 1):
                        for m in range(-step, 1):
                            output_img2[i, j][0] = 255/255
                            output_img2[i, j][1] = 244/255
                            output_img2[i, j][2] = 8/255
                            output_img2[i+k, j][0] = 255/255
                            output_img2[i+k, j][1] = 244/255
                            output_img2[i+k, j][2] = 8/255
                            output_img2[i, j+m][0] = 255/255
                            output_img2[i, j+m][1] = 244/255
                            output_img2[i, j+m][2] = 8/255
                            output_img2[i+k, j+m][0] = 255/255
                            output_img2[i+k, j+m][1] = 244/255
                            output_img2[i+k, j+m][2] = 8/255

        plt.subplots(figsize=(10, 8))
        ax = plt.gca()
        fig = plt.gcf()
        implot = ax.imshow(output_img2)
        print(time.clock() - start)
        plt.show()


if __name__ == '__main__':
    main()
