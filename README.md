<!--
 * @Author: xuranXYS
 * @LastEditTime: 2023-06-24 15:21:58
 * @GitHub: www.github.com/xiaoxustudio
 * @WebSite: www.xiaoxustudio.top
 * @Description: By xuranXYS
-->
# Xscript
一个基于python 编写的（伪）脚本语言
### 目前支持：
- 本地变量的创建
- 全局变量的创建
- 执行少数函数
- 表达式计算

Example：
```
//入口main
fc main(){
    // 创建局部变量
    local a=10+1;
    // 创建全局变量
    global b="xuran";

    //以下为输出结果
    tw(a+1);
    tw(b);
    tw(789);
    tw("XYSYYDS");
    //获取隐私变量local
    tw($local);
}
```

fc 创建main函数，目前都是从main函数开始执行，每句代码必须以分号结尾
隐私变量目前有$local、$global
## 使用方法
### 1.自行编译

在根目录下面打开命令行运行以下命令编译
```
pyinstaller -D or F main.py -p ./xs
```

PS：需要安装pyinstaller

### 2.使用已编译版本

可在releases里面下载已经编译好的版本

### 3.运行

在根目录下面打开命令行运行以下命令运行xs文件
```
./main.exe a.xs
```
PS：前提已经编译源码并生成文件
## 关于
作者xuranXYS 
## 有问题反馈
在使用中有任何问题，欢迎反馈给我，可以用以下联系方式跟我交流
* 网站主页：[小徐工作室](https://www.xiaoxustudio.top)
* 邮件(xugame@qq.com)
* B站: [@徐然XYS](https://space.bilibili.com/291565199)

* 捐助开发者
! [支付宝](https://github.com/xiaoxu1111/xuranxys_Game/blob/main/zfb.jpg)
