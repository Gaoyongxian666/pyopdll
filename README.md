# Welcome to pyopdll

### 项目简介

`pyopdll`是开源项目`OP(operator & open)`的Python接口,
内部封装了`op_x64.dll`和`op_x86.dll`,支持32位和64位Python3


### OP(operator & open)  

* Windows消息模拟，常见的键盘消息和鼠标消息模拟。
* 支持常见的截图方式，gdi,dx（包括d3d9,d3d10,d3d11),opengl截图，支持常见模拟器（雷电，夜神）的最小化截图
* 找色找图,支持偏色，支持模糊识别
* 字符识别(OCR),最大支持255 X 255 超大点阵，支持偏色，支持模糊识别，支持系统字库，兼容大漠字库
* 插件有32位和64位版本，支持32/64位绑定
* 项目完全开源,无后门无病毒，可放心使用

### 项目地址

* [OP(operator & open)](https://github.com/WallBreaker2/op)
* [pyopdll](https://github.com/Gaoyongxian666/pyopdll)
* [pyopdll文档](https://pyopdll.readthedocs.io/zh/latest/)

### 安装

    pip install pyopdll

### 快速开始

    import time
    from pyopdll import OP
    
    if __name__ == '__main__':

    op = OP()

    print(op.GetCursorPos())

    # 打印注册路径
    path = op.GetBasePath()
    print(path)

    # 打印坐标颜色
    print(op.GetColor(2,2))

    # 取消注册
    # op.Un_reg()

    # 运行本地程序
    # op.RunApp(r"C:\Program Files (x86)\Xianghu\CCtalk\CCtalk.exe",0)
    

    # 窗口句柄就是一个int类型的数字
    # 获取鼠标指向的窗口句柄
    hwnd = op.GetMousePointWindow()
    print(hwnd)
    # 打印窗口大小
    print(op.GetClientSize(hwnd))
    # 打印窗体标题栏
    print(op.GetWindowTitle(hwnd))

    # 获取在前台的窗口的句柄
    print(op.GetForegroundWindow())

    # 寻找记事本的句柄
    # 标题需要严格一致才可找到
    txt_hwnd=op.FindWindow("","新建文本文档.txt - 记事本")
    print(txt_hwnd)
    # 打印程序路径
    print(op.GetWindowProcessPath(txt_hwnd))
    # 最大化指定窗口,同时激活窗口.
    print(op.SetWindowState(txt_hwnd,4))
    # 使记事本窗口移动
    op.MoveWindow(txt_hwnd, 10, 10)

    # 拖拽
    op.MoveTo(300,50)
    op.LeftDown()
    for i in range(100):
        time.sleep(0.01)
        op.MoveR(1,0)
    op.LeftUp()

    # 获取标题还有.py的所有句柄
    # 注意：返回的是str，但句柄必须是int类型，要强行转化
    hwnd_str_list=op.EnumWindow(0,".py","",1+2+4+8).split(",")
    print(hwnd_str_list)
    for hwnd in hwnd_str_list:
        print(op.GetWindowClass(int(hwnd)))
        print(op.GetWindowProcessPath(int(hwnd)))
        print(op.GetWindowTitle(int(hwnd)))
        # 全部移动
        # op.MoveWindow(int(hwnd),100,100)

    # 推荐相对移动
    op.MoveR(100, 100)


### 键盘代码

| key_str   | 虚拟键码 |
| --------- | -------- |
| "1",      | 49       |
| "2",      | 50       |
| "3",      | 51       |
| "4",      | 52       |
| "5",      | 53       |
| "6",      | 54       |
| "7",      | 55       |
| "8",      | 56       |
| "9",      | 57       |
| "0",      | 48       |
| "-",      | 189      |
| "=",      | 187      |
| "back",   | 8        |
| "a",      | 65       |
| "b",      | 66       |
| "c",      | 67       |
| "d",      | 68       |
| "e",      | 69       |
| "f",      | 70       |
| "g",      | 71       |
| "h",      | 72       |
| "i",      | 73       |
| "j",      | 74       |
| "k",      | 75       |
| "l",      | 76       |
| "m",      | 77       |
| "n",      | 78       |
| "o",      | 79       |
| "p",      | 80       |
| "q",      | 81       |
| "r",      | 82       |
| "s",      | 83       |
| "t",      | 84       |
| "u",      | 85       |
| "v",      | 86       |
| "w",      | 87       |
| "x",      | 88       |
| "y",      | 89       |
| "z",      | 90       |
| "ctrl",   | 17       |
| "alt",    | 18       |
| "shift",  | 16       |
| "win",    | 91       |
| "space",  | 32       |
| "cap",    | 20       |
| "tab",    | 9        |
| "~",      | 192      |
| "esc",    | 27       |
| "enter",  | 13       |
| "up",     | 38       |
| "down",   | 40       |
| "left",   | 37       |
| "right",  | 39       |
| "option", | 93       |
| "print",  | 44       |
| "delete", | 46       |
| "home",   | 36       |
| "end",    | 35       |
| "pgup",   | 33       |
| "pgdn",   | 34       |
| "f1",     | 112      |
| "f2",     | 113      |
| "f3",     | 114      |
| "f4",     | 115      |
| "f5",     | 116      |
| "f6",     | 117      |
| "f7",     | 118      |
| "f8",     | 119      |
| "f9",     | 120      |
| "f10",    | 121      |
| "f11",    | 122      |
| "f12",    | 123      |
| "[",      | 219      |
| "]",      | 221      |
| "\\",     | 220      |
| ";",      | 186      |
| "'",      | 222      |
| ",",      | 188      |
| ".",      | 190      |
| "/",      | 191      |

