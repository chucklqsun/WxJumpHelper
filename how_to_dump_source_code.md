[原文][ref1]

# 留个记录，别人用来dump微信小游戏的源代码的方法。

## 准备工作
一部已经 root 的 Android 手机
安装微信 6.6.1 版本的 apk
电脑上已安装 Android SDK 并可以使用 adb 命令
需要注意的是必须是已经 root 了的 Android 手机，否则将没有权限访问对应手机的系统文件夹

通过 USB 将手机连接到电脑上，然后运行以下命令

$  adb devices
如果显示了一下信息

List of devices attached
71MBBL6228EU	device
说明手机已经连接到电脑上，如显示未找到 adb 命令，则说明 Android SDK 安装错误或 adb 未添加到电脑 path 中，请自行上网进行相应查阅

手机连接电脑成功后，运行一下命令

$  adb shell
$  su   //手机会卡一下，然后SuperSU会跳出来提示是否授权ROOT权限给ADB，同意
终端出类似 root@{手机型号} 前缀，说明已经进入到 root 模式下

$ cd /data/data/com.tencent.mm/MicroMsg/{User}/appbrand/pkg
{User} 为当前用户的用户名，类似于 1ed**********c514a18

然后当前目录就是微信用于存放小程序和小游戏下载包的位置

$ ls
_-791877121_3.wxapkg
_1079392110_5.wxapkg
_1079392110_5.wxapkg_xdir
_1123949441_92.wxapkg
_576754010_1.wxapkg

以上是我的微信中所下载过的小程序和小游戏源码

因为 /data 目录为系统级目录，无法直接将其进行复制，需要重新挂载为可操作模式

$ mount -o remount,rw /data
此时就可以将当前目录下的文件拷贝到 sdcard 中

$ cd /data/data/com.tencent.mm/MicroMsg/{User}/appbrand/pkg/_1079392110_5.wxapkg /mnt/sdcard
然后将 _1079392110_5.wxapkg 文件拷贝到电脑里，通过该脚本进行解压后，即为其源码

## 编译源码
通过微信小游戏开发工具新建一个空白的小程序或者小游戏的项目，主要不要选择快速启动模板

然后把刚才解压出来的源代码复制到刚刚创建的项目目录中，开发工具会提示编译错误，这时只要在项目中新建一个 game.JSON 文件，并在文件里写入以下代码
{
  "deviceOrientation" : "portrait"
}
然后将开发工具的调试基础库改为 game

程序就会在开发者工具里运行起来了

[ref1]: https://www.v2ex.com/t/419352?p=1 "如何获得微信小游戏跳一跳源码"