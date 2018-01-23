# WxJumpHelper

## How To Use
setup below variable in code:

```
for i in range(0, 5):   # default jump 5 rounds
    learning_seq.append(random.randint(50, 110))
```

default is 5 rounds and jump times (random int) between 50 to 110。You properly get
your score over 700. User should use lower jump times and increase them later to
form a learning curve.

make sure adb is ready for any path
1. Install matplotlib:
    * for Python 2: pip install matplotlib
    * for Python 3: pip3 install matplotlib
2. Install OpenCV
3. Connect your Android phone to your computer and select 'USB for file transfer'.
4. Open the game and be ready to jump.
5. Run the main.py and a screenshot will popup shortly.

![alt text][bottle]

6. The character will jump automatically.
7. Enjoy!

## How It Works
The script uses adb to get the screenshot and calculate the coordination (start point and stop point) and give a proper jumping

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
* 100% automation and support simulating of learning curve
---------------------
* referer version：5->6
* data version: 1->2
* data format：add fields [steps, timestamp]

[data format](https://github.com/chucklqsun/WxJumpHelper/blob/master/send_data_format.txt)

### Warning
* Please do not post score over 1000, otherwise you have risk, such as ban!
* Please do not increase your history best dramatically.
* wx_t1t_hack.js will not be updated in this project, please use it at discretion.

# (微信小游戏：跳一跳) 辅助程序
## 如何使用
在使用前确保adb程序已经安装并且能在任何路径下执行adb命令
在一下代码里配置跳跃的参数:

```
for i in range(0, 5):   # default jump 5 rounds
    learning_seq.append(random.randint(50, 110))
```

默认是跳五轮，每轮跳跃次数在50,110之间的随机整数，分数大概会有七百分的样子。用户可以先降低
随机的范围，比如说(20,50)来模拟新手，然后逐步提高，形成学习曲线。

1. 安装matplotlib库:
    * Python 2: pip install matplotlib
    * Python 3: pip3 install matplotlib
2. 安装opencv
3. 连接你的安卓手机到你电脑上，选择USB文件传送
4. 启动游戏，进入起跳画面
5. 运行main.py，游戏截图会自动出现

![alt text][bottle]

6. 自动开始起跳
7. 玩的开心！

## 工作原理
脚本用adb获取屏幕截图并计算瓶子和目标物体中心的距离，换算成起跳时间

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
* 另外让自己的分数变化太陡峭，历史分数突然大幅变化会引起封号。(官方已经表态，学习曲线会被反外挂参考，很重要)
* 本项目中，wx_t1t_hack.js已经停止更新，被封号的可能性会很大，请酌情使用。

更新:
* 实现完全自动化和模拟学习曲线
---------------------
* referer版本：5->6
* 数据版本: 1->2
* 数据格式：添加字段[steps, timestamp]

[数据格式](https://github.com/chucklqsun/WxJumpHelper/blob/master/send_data_format.txt)

## 又一个彩蛋（大家来找茬腾讯版）
这个游戏暂时没有开发出特别好用的辅助，就先放这个项目下，供大家参考研究。
* zhaocha_tencent/test.js用来抓取这游戏里的原图，resID就是游戏里每关的图片ID,会保存在resID.png。仅供研究使用。
* main.py是游戏开始后，截取安卓手机的屏幕，自动识别不同点后，在电脑上显示标记好的图片。(缺点是速度不够快，仅供研究用)

## 头脑王者辅助（敬请期待）
抓取题库和答案的脚本brain/main.py会被封号。


[bottle]: https://github.com/chucklqsun/WxJumpHelper/raw/master/imgs/bottle.png "Bottle"
