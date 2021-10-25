# -*- coding: UTF-8 -*-
"""
@Project ：pyopdll
@File ：opdll_test.py
@Author ：Gao yongxian
@Date ：2021/10/25 20:19
@contact: g1695698547@163.com
"""

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
