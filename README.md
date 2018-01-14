# WxJumpHelper

## How To Use
make sure adb is ready for any path
1. Install matplotlib:
    * for Python 2: pip install matplotlib
    * for Python 3: pip3 install matplotlib
2. Connect your Android phone to your computer and select 'USB for file transfer'.
3. Open the game and be ready to jump.
4. Run the main.py and a screenshot will popup shortly.
5. Click the character bottom center and then click the destination center.

![alt text][bottle]

6. The character will jump automatically.
7. Close the screenshot window and ready for another jump.
8. Enjoy!

## How It Works
The script uses adb to get the screenshot and calculate the coordination of your two click(start point and stop point) and give a proper jumping

## Further work
Deep Learning version is under development...

## EasterEgg: Use JS script to modify score directly
[original source](https://gist.github.com/feix/6dd1f62a54c5efa10f1e1c24f8efc417)

**Windows User**
before "npm install sleep", please install windows-build-tools first(which is sometimes not useful)
```
npm install --global --production windows-build-tools
```
You can also delete "sleep" related code(but have big risk if server verifies timestamp)

install nodejs, execute below steps in wx_t1t_hack.js dir
1. npm init --y
2. npm install crypto-js request-promise sleep

replace session id with yours
modify score_you_want
(session id could be fetched by fiddle or charles)

### Run & Enjoy
node wx_t1t_hack.js

Update:
* referer version：5->6
* data version: 1->2
* data format：add fields [steps, timestamp]

[data format](https://github.com/chucklqsun/WxJumpHelper/blob/master/send_data_format.txt)

### Warning
* Please do not post score over 1000, otherwise you have risk, such as ban!
* Please do not increase your history best dramatically.

# (微信小游戏：跳一跳) 辅助程序
## 如何使用
在使用前确保adb程序已经安装并且能在任何路径下执行adb命令

1. 安装matplotlib库:
    * Python 2: pip install matplotlib
    * Python 3: pip3 install matplotlib
2. 连接你的安卓手机到你电脑上，选择USB文件传送
3. 启动游戏，进入起跳画面
4. 运行main.py，游戏截图会自动出现
5. 点击角色的底部中间，然后再点击需要跳到的地方的位置

![alt text][bottle]

6. 自动开始起跳
7. 关闭截图窗口，进入下一次起跳阶段
8. 玩的开心！

## 工作原理
脚本用adb获取屏幕截图并计算鼠标两次点击的距离，换算成起跳时间

## 未来计划
机器学习（强化学习）版正在开发中，敬请期待...

## 彩蛋：使用脚本直接修改分数
[原始代码](https://gist.github.com/feix/6dd1f62a54c5efa10f1e1c24f8efc417)

安装nodejs，在脚本wx_t1t_hack.js目录下执行
1. npm init --y
2. npm install crypto-js request-promise sleep

**Windows用户**
npm install sleep 在windows需要额外安装编译套件并且不保证成功
```
npm install --global --production windows-build-tools
```
也可以删除sleep相关代码(如果服务器校验timestamp，风险会很大)。

修改脚本wx_t1t_hack.js的senssion_id为你自己的session id
分数score_you_want
（session id可以通过fiddle或者charles得到）

### 运行 & 玩的开心
node wx_t1t_hack.js

### 注意
* 据观察，目前上万的用户会被关小黑屋（其他用户不可见你的分数），上千的也有被ban的可能。
* 不知道是因为数据不可信还是分数太高本身的原因，玩家务必控制分数在三位数。
* 另外让自己的分数变化太陡峭，历史分数突然大幅变化会引起封号。

更新:
* referer版本：5->6
* 数据版本: 1->2
* 数据格式：添加字段[steps, timestamp]

[数据格式](https://github.com/chucklqsun/WxJumpHelper/blob/master/send_data_format.txt)

[bottle]: https://github.com/chucklqsun/WxJumpHelper/raw/master/imgs/bottle.png "Bottle"
