# WxJumpHelper

## How To Use
make sure adb is ready for any path
1. Install matplotlib:
    for Python 2: pip install matplotlib
    for Python 3: pip3 install matplotlib
2. Connect your Android phone to your computer and select 'USB for file transfer'.
3. Open the game and be ready to jump.
4. Run the main.py and a screenshot will popup shortly.
5. Click the character bottom and then click the destination center.
6. The character will jump automatically.
7. Close the screenshot window and ready for another jump.
8. Enjoy!

## How It Works
The script uses adb to get the screenshot and calculate the coordination of your two click(start point and stop point) and give a proper jumping

## Further work
Deep Learning version is under development...

## EasterEgg: Use JS script to modify score directly
install nodejs, execute below steps in wx_t1t_hack.js dir
1. npm init --y
2. npm install crypto-js request-promise

replace session id with yours
(session id could be fetched by fiddle or charles)


# (微信小游戏：跳一跳) 辅助程序
## 如何使用
在使用前确保adb程序已经安装并且能在任何路径下执行adb命令

1. 安装matplotlib库:
    Python 2: pip install matplotlib
    Python 3: pip3 install matplotlib
2. 连接你的安卓手机到你电脑上，选择USB文件传送
3. 启动游戏，进入起跳画面
4. 运行main.py，游戏截图会自动出现
5. 点击角色的底部中间，然后再点击需要跳到的地方的位置
6. 自动开始起跳
7. 关闭截图窗口，进入下一次起跳阶段
8. 玩的开心！

## 工作原理
脚本用adb获取屏幕截图并计算鼠标两次点击的距离，换算成起跳时间

## 未来计划
机器学习（强化学习）版正在开发中，敬请期待...

## 彩蛋：使用脚本直接修改分数
安装nodejs，在脚本wx_t1t_hack.js目录下执行
1. npm init --y
2. npm install crypto-js request-promise

修改脚本wx_t1t_hack.js的senssion_id为你自己的session id
（session id可以通过fiddle或者charles得到）

