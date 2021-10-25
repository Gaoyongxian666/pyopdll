# -*- coding: UTF-8 -*-
"""
@Project ：pyopdll
@File ：op.py
@Author ：Gao yongxian
@Date ：2021/10/25 15:53
@contact: g1695698547@163.com
"""

import os
import struct
import time
import ctypes
try:
    from win32com.client import Dispatch
except:
    pass


class OP:
    """
    pyopdll是开源项目OP(operator & open)的Python接口。

    OP(operator & open)地址：https://github.com/WallBreaker2/op
    """

    def __init__(self, dll_path: str = None) -> None:
        """
        初始化并且完成注册

        Args:
            dll_path: op_x64.dll路径。可以指定本地的dll文件，但文件名称必须是op_x64.dll或者op_x86
        """

        if struct.calcsize("P") * 8 == 32:
            self.dll_prefix = "op_x86.dll"
        else:
            self.dll_prefix = "op_x64.dll"
        self.dll_path = dll_path
        if dll_path is None:
            self.dll_path = os.path.join(os.path.dirname(__file__.replace('/', '\\')), self.dll_prefix)
        self.cmd_dll = 'regsvr32 \"' + self.dll_path + '\" /s'

        # 判断是否已经注册注册成功返回版本信息
        if self.__is_reg:
            print("成功注册：" + 'VER:', self.ver(), ',ID:', self.GetID(), ',PATH:',
                  os.path.join(self.GetBasePath(), self.dll_prefix))
        else:
            self.__reg_as_admin()
            if self.__is_reg:
                print("成功注册：" + 'VER:', self.ver(), ',ID:', self.GetID(), ',PATH:',
                      os.path.join(self.GetBasePath(), self.dll_prefix))
            else:
                print("注册失败：" + time.strftime('%Y-%m-%d-%H:%M:%S',
                                              time.localtime(time.time())) + self.dll_path + "：注册失败")

    def __unreg_as_admin(self) -> None:
        """
        删除注册的dll。

        Returns:
            无返回值。
        """
        self.cmd_un_dll = 'regsvr32 /u /s \"' + os.path.join(self.GetBasePath(), self.dll_prefix) + '\"'
        if self.__is_admin:
            os.system(self.cmd_un_dll)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", "/C %s" % self.cmd_un_dll, None, 1)
            time.sleep(3)
            print("删除注册：" + 'VER:', self.ver(), ',ID:', self.GetID(), ',PATH:',
                  os.path.join(self.GetBasePath(), self.dll_prefix))

    def __reg_as_admin(self) -> None:
        """
        注册dll。

        Returns:
            无返回值。
        """
        if self.__is_admin:
            os.system(self.cmd_dll)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", "/C %s" % self.cmd_dll, None, 1)
            time.sleep(3)

    @property
    def __is_reg(self) -> int:
        """
        判断dll是否调用成功。

        Returns:
            返回int数据类型，1代表调用成功，0代表调用失败。
        """
        try:
            self.op = Dispatch("op.opsoft")
            return 1
        except:
            print(
                "调用失败：" + time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time())) + self.dll_path + "：调用失败")
            return 0

    @property
    def __is_admin(self) -> bool:
        """
        判断是否具有管理员权限。

        Returns:
            返回bool类型。
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def __repr__(self) -> str:
        """
        自我描述信息。

        Returns:
            自我描述信息。
        """
        ret = 'VER:' + self.ver() + ',ID:' + str(self.GetID()) + ',PATH:' + os.path.join(
            self.GetBasePath() + self.dll_prefix)
        return ret

    """----------------------------------------取消注册------------------------------------------------"""

    def Un_reg(self) -> None:
        """
        取消已经注册的dll

        Returns:
            无返回值
        """
        self.__unreg_as_admin()

    """----------------------------------------窗口设置------------------------------------------------"""

    def ClientToScreen(self, hwnd: int) -> tuple:
        """
        把窗口坐标转换为屏幕坐标

        Args:
            hwnd: 指定的窗口句柄.你可以使用GetWindow，FindWindow等返回窗口句柄的方法获取句柄

        Returns:
            返回元组数据类型,（窗口句柄，X坐标，Y坐标）.
        """
        return self.op.ClientToScreen(hwnd, 1, 1)

    def EnumProcess(self, name: str) -> str:
        """
        根据进程名枚举进程

        Args:
            name:进程名,比如qq.exe

        Returns:
            返回所有匹配的进程PID,并按打开顺序排序,格式"pid1,pid2,pid3"
        """
        return self.op.EnumProcess(name)

    def EnumWindow(self, parent: int, title: str, class_name: str, _filter: int) -> str:
        """
        根据父窗口,枚举系统中符合条件的子窗口,可以枚举到按键自带的无法枚举到的窗口

        Args:
            parent: 获得的窗口句柄是该窗口的子窗口的窗口句柄,取0时为获得桌面句柄
            title: 窗口标题. 此参数是模糊匹配.
            class_name: 窗口类名. 此参数是模糊匹配.
            _filter: 取值定义如下
                        1 : 匹配窗口标题,参数title有效
                        2 : 匹配窗口类名,参数class_name有效.
                        4 : 只匹配指定父窗口的第一层孩子窗口
                        8 : 匹配所有者窗口为0的窗口,即顶级窗口
                        16 : 匹配可见的窗口
                        32 : 匹配出的窗口按照窗口打开顺序依次排列
                        这些值可以相加,比如4+8+16就是类似于任务管理器中的窗口列表

        Returns:
            返回str数据类型，"hwnd1,hwnd2,hwnd3"，你可以字符串分割变成列表

        示例:

            hwnds = dm.EnumWindow(0,"QQ三国","",1+4+8+16)
            这句是获取到所有标题栏中有QQ三国这个字符串的窗口句柄集合
            hwnds = split(hwnds,",")
            转换为数组后,就可以处理了
            这里注意,hwnds数组里的是字符串,要用于使用,比如BindWindow时,还得强制类型转换,比如int(hwnds(0))
        """
        return self.op.EnumWindow(parent, title, class_name, _filter)

    def EnumWindowByProcess(self, process_name: str, title: str, class_name: str, _filter: int) -> str:
        """
        根据指定进程以及其它条件,枚举系统中符合条件的窗口,可以枚举到按键自带的无法枚举到的窗口

        Args:
            process_name:进程映像名.比如(svchost.exe). 此参数是精确匹配,但不区分大小写.
            title:窗口标题. 此参数是模糊匹配.
            class_name:窗口类名. 此参数是模糊匹配.
            _filter:取值定义如下  1 : 匹配窗口标题,参数title有效2 : 匹配窗口类名,参数class_name有效4 : 只匹配指定映像的所对应的第一个进程. 可能有很多同映像名的进程，只匹配第一个进程的.8 : 匹配所有者窗口为0的窗口,即顶级窗口16 : 匹配可见的窗口

        Returns:
            返回str数据类型，返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"
        """
        return self.op.EnumWindowByProcess(process_name, title, class_name, _filter)

    def EnumWindowSuper(self, spec1: str, flag1: int, type1: int, spec2: str, flag2: int, type2: int, sort: int) -> str:
        """
        根据两组设定条件来枚举指定窗口.

        Args:
            spec1:查找串1. (内容取决于flag1的值)
            flag1:flag1取值如下:
                            0表示spec1的内容是标题
                            1表示spec1的内容是程序名字. (比如notepad)
                            2表示spec1的内容是类名
                            3表示spec1的内容是程序路径.(不包含盘符,比如\windows\system32)
                            4表示spec1的内容是父句柄.(十进制表达的串)
                            5表示spec1的内容是父窗口标题
                            6表示spec1的内容是父窗口类名
                            7表示spec1的内容是顶级窗口句柄.(十进制表达的串)
                            8表示spec1的内容是顶级窗口标题
                            9表示spec1的内容是顶级窗口类名
            type1:0精确判断1模糊判断
            spec2:查找串2. (内容取决于flag2的值)
            flag2:flag2取值如下:
                            0表示spec2的内容是标题
                            1表示spec2的内容是程序名字. (比如notepad)
                            2表示spec2的内容是类名
                            3表示spec2的内容是程序路径.(不包含盘符,比如\windows\system32)
                            4表示spec2的内容是父句柄.(十进制表达的串)
                            5表示spec2的内容是父窗口标题
                            6表示spec2的内容是父窗口类名
                            7表示spec2的内容是顶级窗口句柄.(十进制表达的串)
                            8表示spec2的内容是顶级窗口标题
                            9表示spec2的内容是顶级窗口类名
            type2:0精确判断,1模糊判断
            sort:0不排序.1对枚举出的窗口进行排序,按照窗口打开顺序.

        Returns:
            返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"
        """
        return self.op.EnumWindowSuper(spec1, flag1, type1, spec2, flag2, type2, sort)

    def FindWindow(self, class_name: str = '', title_name: str = '') -> int:
        """
        查找符合类名或者标题名的顶层可见窗

        Args:
            class_name: 窗口类名，如果为空，则匹配所有. 这里的匹配是模糊匹配.
            title_name: 窗口标题,如果为空，则匹配所有.这里的匹配是模糊匹配.

        Returns:
            整数型表示的窗口句柄，没找到返回0

        For example:

            hwnd = dm.FindWindow("","记事本")

        """
        return self.op.FindWindow(class_name, title_name)

    def FindWindowByProcess(self, process_name: str, class_: str, title: str) -> int:
        """
        根据指定的进程名字，来查找可见窗口.

        Args:
            process_name:进程名. 比如(notepad.exe).这里是精确匹配,但不区分大小写.
            class_:窗口类名，如果为空，则匹配所有. 这里的匹配是模糊匹配.
            title:窗口标题,如果为空，则匹配所有.这里的匹配是模糊匹配.

        Returns:
            表示的窗口句柄，没找到返回0
        """
        return self.op.FindWindowByProcess(process_name, class_, title)

    def FindWindowByProcessId(self, process_id: int, class_: str, title: str) -> int:
        """
        根据指定的进程Id，来查找可见窗口.

        Args:
            process_id: 进程id.
            class_: 窗口类名，如果为空，则匹配所有. 这里的匹配是模糊匹配.
            title: 窗口标题,如果为空，则匹配所有.这里的匹配是模糊匹配.

        Returns:
            表示的窗口句柄，没找到返回0
        """
        return self.op.FindWindowByProcessId(process_id, class_, title)

    def FindWindowEx(self, parent: int, _class: str, title: str) -> int:
        """
        查找符合类名或者标题名的顶层可见窗口,如果指定了parent,则在parent的第一层子窗口中查找.

        Args:
            parent:父窗口句柄，如果为空，则匹配所有顶层窗口
            _class:窗口类名，如果为空，则匹配所有. 这里的匹配是模糊匹配.
            title:窗口标题,如果为空，则匹配所有. 这里的匹配是模糊匹配.

        Returns:
            表示的窗口句柄，没找到返回0

        For example:

            hwnd = dm.FindWindowEx(0,"","记事本")

        """
        return self.op.FindWindowEx(parent, _class, title)

    def FindWindowSuper(self, spec1: str, flag1: int, type1: int, spec2: str, flag2: int, type2: int) -> int:
        """
        根据两组设定条件来查找指定窗口.

        Args:
            spec1:查找串1. (内容取决于flag1的值)
            flag1:flag1取值如下:
                            0表示spec1的内容是标题
                            1表示spec1的内容是程序名字. (比如notepad)
                            2表示spec1的内容是类名
                            3表示spec1的内容是程序路径.(不包含盘符,比如\windows\system32)
                            4表示spec1的内容是父句柄.(十进制表达的串)
                            5表示spec1的内容是父窗口标题
                            6表示spec1的内容是父窗口类名
                            7表示spec1的内容是顶级窗口句柄.(十进制表达的串)
                            8表示spec1的内容是顶级窗口标题
                            9表示spec1的内容是顶级窗口类名
            type1:0精确判断1模糊判断
            spec2:查找串2. (内容取决于flag2的值)
            flag2:flag2取值如下:
                            0表示spec2的内容是标题
                            1表示spec2的内容是程序名字. (比如notepad)
                            2表示spec2的内容是类名
                            3表示spec2的内容是程序路径.(不包含盘符,比如\windows\system32)
                            4表示spec2的内容是父句柄.(十进制表达的串)
                            5表示spec2的内容是父窗口标题
                            6表示spec2的内容是父窗口类名
                            7表示spec2的内容是顶级窗口句柄.(十进制表达的串)
                            8表示spec2的内容是顶级窗口标题
                            9表示spec2的内容是顶级窗口类名
            type2:0精确判断,1模糊判断

        Returns:
            表示的窗口句柄，没找到返回0
        """
        return self.op.FindWindowSuper(spec1, flag1, type1, spec2, flag2, type2)

    def GetClientRect(self, hwnd: int) -> tuple:
        """
        获取窗口客户区域在屏幕上的位置

        Args:
            hwnd:指定的窗口句柄

        Returns:
            (窗口句柄,窗口客户区左上角X坐标,窗口客户区左上角Y坐标,窗口客户区右下角X坐标,窗口客户区右下角Y坐标)
        """
        return self.op.GetClientRect(hwnd, 1, 1, 1, 1)

    def GetClientSize(self, hwnd: int) -> tuple:
        """
        获取窗口客户区域的宽度和高度

        Args:
            hwnd:指定的窗口句柄

        Returns:
            (指定的窗口句柄,宽度,高度)
        """
        return self.op.GetClientSize(hwnd, 1, 1)

    def GetForegroundFocus(self) -> int:
        """
        获取顶层活动窗口中具有输入焦点的窗口句柄

        Returns:
            返回整型表示的窗口句柄
        """
        return self.op.GetForegroundFocus()

    def GetForegroundWindow(self) -> int:
        """
        获取顶层活动窗口,可以获取到按键自带插件无法获取到的句柄

        Returns:
            返回整型表示的窗口句柄
        """
        return self.op.GetForegroundWindow()

    def GetMousePointWindow(self) -> int:
        """
        获取鼠标指向的窗口句柄,可以获取到按键自带的插件无法获取到的句柄

        Returns:
            返回整型表示的窗口句柄
        """
        return self.op.GetMousePointWindow()

    def GetPointWindow(self, x: int, y: int) -> int:
        """
        获取给定坐标的窗口句柄,可以获取到按键自带的插件无法获取到的句柄

        Args:
            x:屏幕X坐标
            y:屏幕Y坐标

        Returns:
            返回整型表示的窗口句柄
        """
        return self.op.GetPointWindow(x, y)

    def GetSpecialWindow(self, flag: int) -> int:
        """
        获取特殊窗口

        Args:
            flag:取值定义如下
                    0 : 获取桌面窗口
                    1 : 获取任务栏窗口

        Returns:
            以整型数表示的窗口句柄
        """
        return self.op.GetSpecialWindow(flag)

    def GetProcessInfo(self, pid: int) -> str:
        """
        根据指定的pid获取进程详细信息,(进程名,进程全路径,CPU占用率(百分比),内存占用量(字节))

        Args:
            pid:进程pid

        Returns:
            字符串: 格式"进程名|进程路径|cpu|内存"
        """
        return self.op.GetProcessInfo(pid)

    def GetWindow(self, hwnd: int, flag: int) -> int:
        """
        获取给定窗口相关的窗口句柄

        Args:
            hwnd:窗口句柄
            flag:取值定义如下
                    0 : 获取父窗口
                    1 : 获取第一个儿子窗口
                    2 : 获取First 窗口
                    3 : 获取Last窗口
                    4 : 获取下一个窗口
                    5 : 获取上一个窗口
                    6 : 获取拥有者窗口
                    7 : 获取顶层窗口

        Returns:
            返回整型表示的窗口句柄
        """
        return self.op.GetWindow(hwnd, flag)

    def GetWindowClass(self, hwnd: int) -> str:
        """
        获取窗口的类名

        Args:
            hwnd:指定的窗口句柄

        Returns:
            窗口的类名
        """
        return self.op.GetWindowClass(hwnd)

    def GetWindowProcessId(self, hwnd: int) -> int:
        """
        获取指定窗口所在的进程ID.

        Args:
            hwnd:窗口句柄

        Returns:
            返回整型表示的是进程ID
        """
        return self.op.GetWindowClass(hwnd)

    def GetWindowProcessPath(self, hwnd: int) -> str:
        """
        获取指定窗口所在的进程的exe文件全路径.

        Args:
            hwnd:窗口句柄

        Returns:
            返回字符串表示的是exe全路径名
        """
        return self.op.GetWindowProcessPath(hwnd)

    def GetWindowRect(self, hwnd: int) -> tuple:
        """
        获取窗口在屏幕上的位置

        Args:
            hwnd:指定的窗口句柄

        Returns:
            (指定的窗口句柄,窗口左上角X坐标,窗口左上角Y坐标 窗口右下角X坐标,窗口右下角Y坐标)
        """
        return self.op.GetWindowRect(self, hwnd, 1, 1, 1, 1)

    def GetWindowState(self, hwnd: int, flag: int) -> int:
        """
        获取指定窗口的一些属性

        Args:
            hwnd: 指定的窗口句柄
            flag: 取值定义如下:
                    0 : 判断窗口是否存在
                    1 : 判断窗口是否处于激活
                    2 : 判断窗口是否可见
                    3 : 判断窗口是否最小化
                    4 : 判断窗口是否最大化
                    5 : 判断窗口是否置顶
                    6 : 判断窗口是否无响应
                    7 : 判断窗口是否可用(灰色为不可用)
                    8 : 另外的方式判断窗口是否无响应,如果6无效可以尝试这个

        Returns:
            0代表失败，1代表成功

        """
        return self.op.GetWindowState(hwnd, 4)

    def GetWindowTitle(self, hwnd: int) -> str:
        """
        获取窗口的标题

        Args:
            hwnd:指定的窗口句柄

        Returns:
            窗口的标题
        """
        return self.op.GetWindowTitle(hwnd)

    def MoveWindow(self, hwnd: int, x: int, y: int) -> int:
        """
        移动指定窗口到指定位置

        Args:
            hwnd:指定的窗口句柄
            x:X坐标
            y:Y坐标

        Returns:
            0代表失败，1代表成功
        """
        return self.op.MoveWindow(hwnd, x, y)

    def ScreenToClient(self, hwnd: int) -> tuple:
        """
        把屏幕坐标转换为窗口坐标

        Args:
            hwnd:指定的窗口句柄

        Returns:
            返回元组（指定的窗口句柄，屏幕X坐标，屏幕Y坐标）
        """
        return self.op.ScreenToClient(hwnd, 1, 1)

    def SendPaste(self, hwnd: int) -> int:
        """
        向指定窗口发送粘贴命令. 把剪贴板的内容发送到目标窗口.

        Args:
            hwnd:指定的窗口句柄

        Returns:
            0代表失败，1代表成功
        """
        return self.op.SendPaste(hwnd)

    def SendString(self, hwnd: int, str: str) -> int:
        """
        向指定窗口发送文本数据

        Args:
            hwnd:指定的窗口句柄
            str:发送的文本数据

        Returns:
            0代表失败，1代表成功
        """
        return self.op.SendString(hwnd, str)

    def SendString2(self, hwnd: int, str: str) -> int:
        """
        向指定窗口发送文本数据

        Args:
            hwnd: 指定的窗口句柄
            str: 发送的文本数据

        Returns:
            0代表失败，1代表成功

        注: 此接口为老的SendString，如果新的SendString不能输入，可以尝试此接口.
        """
        return self.op.SendString2(hwnd, str)

    def SetClientSize(self, hwnd: int, width: int, height: int) -> int:
        """
        设置窗口客户区域的宽度和高度

        Args:
            hwnd: 指定的窗口句柄
            width: 宽度
            height: 高度

        Returns:
            0代表失败，1代表成功
        """
        return self.op.SetClientSize(hwnd, width, height)

    def SetWindowSize(self, hwnd: int, width: int, height: int) -> int:
        """
        设置窗口的大小

        Args:
            hwnd: 指定的窗口句柄
            width: 宽度
            height: 高度

        Returns:
            0代表失败，1代表成功
        """
        return self.op.SetWindowSize(hwnd, width, height)

    def SetWindowState(self, hwnd: int, flag: int) -> int:
        """
        设置窗口的状态

        Args:
            hwnd: 指定的窗口句柄
            flag: 取值定义如下
                    0 : 关闭指定窗口
                    1 : 激活指定窗口
                    2 : 最小化指定窗口,但不激活
                    3 : 最小化指定窗口,并释放内存,但同时也会激活窗口.
                    4 : 最大化指定窗口,同时激活窗口.
                    5 : 恢复指定窗口 ,但不激活
                    6 : 隐藏指定窗口
                    7 : 显示指定窗口
                    8 : 置顶指定窗口
                    9 : 取消置顶指定窗口
                    10 : 禁止指定窗口
                    11 : 取消禁止指定窗口
                    12 : 恢复并激活指定窗口
                    13 : 强制结束窗口所在进程.

        Returns:
            0代表失败，1代表成功
        """
        return self.op.SetWindowState(hwnd, flag)

    def SetWindowText(self, hwnd: int, title: str) -> int:
        """
        设置窗口的标题

        Args:
            hwnd: 指定的窗口句柄
            title: 标题

        Returns:
            0代表失败，1代表成功
        """
        return self.op.SetWindowText(hwnd, title)

    def SetWindowTransparent(self, hwnd: int, trans: int) -> int:
        """
        设置窗口的透明度

        Args:
            hwnd: 指定的窗口句柄
            trans: 透明度取值(0-255) 越小透明度越大 0为完全透明(不可见) 255为完全显示(不透明)

        Returns:
            0代表失败，1代表成功
        """
        return self.op.SetWindowTransparent(hwnd, trans)

    """----------------------------------------基本设置------------------------------------------------"""

    def GetBasePath(self) -> str:
        """
        获取注册在系统中的dll的路径.

        Returns:
            返回dll所在路径.
        """
        return self.op.GetBasePath()

    def GetID(self) -> int:
        """
        返回当前对象的ID值，这个值对于每个对象是唯一存在的。可以用来判定两个对象是否一致.

        Returns:
            当前对象的ID值.
        """
        return self.op.GetID()

    def GetLastError(self) -> int:
        """
        获取插件命令的最后错误

        Returns:
            返回值表示错误值。 0表示无错误.

        注: 此函数必须紧跟上一句函数调用，中间任何的语句调用都会改变这个值.
        """
        return self.op.GetLastError()

    def GetPath(self) -> str:
        """
        获取全局路径.(可用于调试)

        Returns:
            以字符串的形式返回当前设置的全局路径
        """
        return self.op.GetPath()

    def SetPath(self, path: str) -> int:
        """
        设置全局路径,设置了此路径后,所有接口调用中,相关的文件都相对于此路径. 比如图片,字库等.

        Args:
            path: 路径,可以是相对路径,也可以是绝对路径

        Returns:
            0代表失败，1代表成功
        """
        return self.op.GetPath(path)

    def SetShowErrorMsg(self, show: int) -> int:
        """
        设置是否弹出错误信息,默认是打开.

        Args:
            show: 0表示不打开,1表示打开.

        Returns:
            0代表失败，1代表成功
        """
        return self.op.SetShowErrorMsg(show)

    def ver(self) -> str:
        """
        返回当前插件版本号

        Returns:
            当前插件的版本描述字符串
        """
        return self.op.ver()

    def EnablePicCache(self, enable: int) -> int:
        """
        设置是否开启或者关闭插件内部的图片缓存机制. (默认是打开).

        Args:
            enable:0代表关闭，1代表打开

        Returns:
            0代表失败，1代表成功

        注: 有些时候，系统内存比较吃紧，这时候再打开内部缓存，可能会导致缓存分配在虚拟内存，这样频繁换页，反而导致图色效率下降.这时候就建议关闭图色缓存. 所有图色缓存机制都是对本对象的，也就是说，调用图色缓存机制的函数仅仅对本对象生效. 每个对象都有一个图色缓存队列.
        """
        return self.op.EnablePicCache(enable)

    """----------------------------------------后台设置------------------------------------------------"""

    def BindWindow(self, hwnd: int, display: str, mouse: str, keypad: str, mode: int) -> int:
        """
        绑定指定的窗口,并指定这个窗口的屏幕颜色获取方式,鼠标仿真模式,键盘仿真模式,以及模式设定.
        Args:
            hwnd:指定的窗口句柄
            display:屏幕颜色获取方式 取值有以下几种:
                "normal" : 正常模式,平常我们用的前台截屏模式
                "gdi" : gdi模式,用于窗口采用GDI方式刷新时. 此模式占用CPU较大. 参考SetAero
                "dx" : dx模式,等同于dx.d3d9
                "dx.d3d9" dx模式，使用d3d9渲染
                "dx.d3d10" dx模式，使用d3d10渲染
                "dx.d3d11" dx模式，使用d3d11渲染
                "opengl" opengl模式，使用opengl渲染的窗口，支持最新版雷电模拟器，以及夜神6.1，支持最小化窗口截图
                "opengl.nox" opengl模式，针对最新夜神模拟器的渲染方式，测试中。。。
            mouse:鼠标仿真模式 取值有以下几种
                "normal" : 正常模式,平常我们用的前台鼠标模式
                "windows": Windows模式,采取模拟windows消息方式 同按键自带后台插件.
            keypad:键盘仿真模式 取值有以下几种
                "normal" : 正常模式,平常我们用的前台键盘模式
                "windows": Windows模式,采取模拟windows消息方式 同按键的后台插件
            mode:模式

        Returns:
            0代表失败，1代表成功
        """
        return self.op.BindWindow(hwnd, display, mouse, keypad, mode)

    def UnBindWindow(self) -> int:
        """
        解除绑定窗口,并释放系统资源.一般在OnScriptExit调用

        Returns:
            0代表失败，1代表成功
        """
        return self.op.UnBindWindow()

    """----------------------------------------Win API------------------------------------------------"""

    def RunApp(self, app_path: str, mode: int) -> int:
        """
        运行指定的应用程序.

        Args:
            app_path:指定的可执行程序全路径.
            mode:取值如下0:普通模式  1:加强模式

        Returns:
            0代表失败，1代表成功
        """
        return self.op.RunApp(app_path, mode)

    def WinExec(self, cmdline: str, cmdshow: int) -> str:
        """
        运行指定的应用程序.

        Args:
            cmdline: 指定的可执行程序全路径.
            cmdshow: 取值如下 0:隐藏 1:用最近的大小和位置显示, 激活

        Returns:
            0代表失败，1代表成功
        """
        return self.op.WinExec(cmdline, cmdshow)

    def GetCmdStr(self, cmdline: str, millseconds: int) -> str:
        """
        运行指定的应用程序.

        Args:
            cmdline:指定的可执行程序全路径.
            millseconds:等待的时间(毫秒)

        Returns:
             cmd输出的字符
        """
        return self.op.GetCmdStr(cmdline, millseconds)

    """----------------------------------------鼠标键盘------------------------------------------------"""
    '''
    key_str     虚拟键码    
    "1",          49    
    "2",          50    
    "3",          51    
    "4",          52   
    "5",          53   
    "6",          54   
    "7",          55    
    "8",          56    
    "9",          57    
    "0",          48    
    "-",          189    
    "=",          187   
    "back",       8         
    "a",          65  
    "b",          66   
    "c",          67    
    "d",          68   
    "e",          69  
    "f",          70  
    "g",          71  
    "h",          72   
    "i",          73   
    "j",          74  
    "k",          75  
    "l",          76  
    "m",          77   
    "n",          78   
    "o",          79   
    "p",          80   
    "q",          81   
    "r",          82  
    "s",          83  
    "t",          84   
    "u",          85    
    "v",          86   
    "w",          87   
    "x",          88    
    "y",          89 
    "z",          90   
    "ctrl",       17 
    "alt",        18  
    "shift",      16   
    "win",        91    
    "space",      32  
    "cap",        20 
    "tab",        9 
    "~",          192   
    "esc",        27  
    "enter",      13   
    "up",         38   
    "down",       40  
    "left",       37   
    "right",      39      
    "option",     93    
    "print",      44 
    "delete",     46
    "home",       36  
    "end",        35   
    "pgup",       33 
    "pgdn",       34    
    "f1",         112   
    "f2",         113   
    "f3",         114  
    "f4",         115  
    "f5",         116   
    "f6",         117
    "f7",         118  
    "f8",         119   
    "f9",         120   
    "f10",        121   
    "f11",        122   
    "f12",        123
    "[",          219  
    "]",          221   
    "\\",         220  
    ";",          186  
    "'",          222   
    ",",          188  
    ".",          190  
    "/",          191
    '''

    def GetCursorPos(self) -> tuple:
        """
        获取鼠标位置.

        Returns:
            (x,y)
        """
        return self.op.GetCursorPos(1, 1)

    def GetKeyState(self, vk_code: int) -> int:
        """
        获取指定的按键状态.(前台信息,不是后台)

        Args:
            vk_code: 虚拟按键码

        Returns:
            0代表失败，1代表成功
        """
        return self.op.GetKeyState(vk_code)

    def KeyDown(self, vk_code: int) -> int:
        """
        按住指定的虚拟键码

        Args:
            vk_code: 虚拟按键码

        Returns:
            0代表失败，1代表成功
        """
        return self.op.KeyDown(vk_code)

    def KeyDownChar(self, key_str: str) -> int:
        """
        按住指定的虚拟键码

        Args:
            key_str: 符串描述的键码. 大小写无所谓. 点这里查看具体对应关系

        Returns:
            0代表失败，1代表成功
        """
        return self.op.KeyDownChar(key_str)

    def KeyPress(self, vk_code: int) -> int:
        """
        按下指定的虚拟键码

        Args:
            vk_code: 虚拟按键码

        Returns:
            0代表失败，1代表成功
        """
        return self.op.KeyPress(vk_code)

    def KeyPressChar(self, key_str: str) -> int:
        """
        按下指定的虚拟键码

        Args:
            key_str: 字符串描述的键码. 大小写无所谓. 点这里查看具体对应关系

        Returns:
            0代表失败，1代表成功
        """
        return self.op.KeyPressChar(key_str)

    def KeyUp(self, vk_code: int) -> int:
        """
        弹起来虚拟键vk_code

        Args:
            vk_code: 虚拟按键码

        Returns:
            0代表失败，1代表成功
        """
        return self.op.KeyUp(vk_code)

    def KeyUpChar(self, key_str: str) -> int:
        """
        弹起来虚拟键key_str

        Args:
            key_str: 字符串描述的键码. 大小写无所谓. 点这里查看具体对应关系.

        Returns:
            0代表失败，1代表成功
        """
        return self.op.KeyUpChar(key_str)

    def LeftClick(self) -> int:
        """
        按下鼠标左键

        Returns:
            0代表失败，1代表成功
        """
        return self.op.LeftClick()

    def LeftDoubleClick(self) -> int:
        """
        双击鼠标左键

        Returns:
            0代表失败，1代表成功
        """
        return self.op.LeftDoubleClick()

    def LeftDown(self) -> int:
        """
        按住鼠标左键

        Returns:
            0代表失败，1代表成功
        """
        return self.op.LeftDown()

    def LeftUp(self) -> int:
        """
        弹起鼠标左键

        Returns:
            0代表失败，1代表成功
        """
        return self.op.LeftUp()

    def MiddleClick(self) -> int:
        """
        按下鼠标中键

        Returns:
            0代表失败，1代表成功
        """
        return self.op.MiddleClick()

    def MoveR(self, rx: int, ry: int) -> int:
        """
        鼠标相对于上次的位置移动rx,ry

        Args:
            rx: 相对于上次的X偏移
            ry: 相对于上次的Y偏移

        Returns:
            0代表失败，1代表成功
        """
        return self.op.MoveR(rx, ry)

    def MoveTo(self, x: int, y: int) -> int:
        """
        把鼠标移动到目的点(x,y)

        Args:
            x: X坐标
            y: Y坐标

        Returns:
            0代表失败，1代表成功
        """
        return self.op.MoveTo(x, y)

    def MoveToEx(self, x: int, y: int, w: int, h: int) -> str:
        """
        把鼠标移动到目的范围内的任意一点

        Args:
            x:X坐标
            y:Y坐标
            w:宽度(从x计算起)
            h:高度(从y计算起)

        Returns:
            返回要移动到的目标点. 格式为x,y. 比如MoveToEx 100,100,10,10,返回值可能是101,102
        """
        return self.op.MoveToEx(x, y, w, h)

    def RightClick(self) -> int:
        """
        按下鼠标右键

        Returns:
            0代表失败，1代表成功
        """
        return self.op.RightClick()

    def RightDown(self) -> int:
        """
        按住鼠标右键

        Returns:
            0代表失败，1代表成功
        """
        return self.op.RightDown()

    def RightUp(self) -> int:
        """
        弹起鼠标右键

        Returns:
            0代表失败，1代表成功
        """
        return self.op.RightUp()

    def WaitKey(self, vk_code: int, time_out: int) -> int:
        """
        等待指定的按键按下 (前台,不是后台)

        Args:
            vk_code:虚拟按键码,当此值为0，表示等待任意按键。 鼠标左键是1,鼠标右键时2,鼠标中键是4
            time_out:等待多久,单位毫秒. 如果是0，表示一直等待

        Returns:
            0:超时 1:指定的按键按下 (当vk_code不为0时) 按下的按键码:(当vk_code为0时)
        """
        return self.op.WaitKey(vk_code, time_out)

    def WheelDown(self) -> int:
        """
        滚轮向下滚

        Returns:
            0代表失败，1代表成功
        """
        return self.op.WheelDown()

    def WheelUp(self) -> int:
        """
        滚轮向上滚

        Returns:
            0代表失败，1代表成功
        """
        return self.op.WheelUp()

    """----------------------------------------图色功能------------------------------------------------"""

    def Capture(self, x1: int, y1: int, x2: int, y2: int, file: str) -> int:
        """
        抓取指定区域(x1, y1, x2, y2)的图像,保存为file(24位位图)

        Args:
            x1:区域的左上X坐标
            y1:区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标
            file:保存的文件名,保存的地方一般为SetPath中设置的目录,当然这里也可以指定全路径名.

        Returns:
            0代表失败，1代表成功
        """
        return self.op.Capture(x1, y1, x2, y2, file)

    def CmpColor(self, x: int, y: int, color: str, sim: float) -> int:
        """
        比较指定坐标点(x,y)的颜色

        Args:
            x: X坐标
            y: Y坐标
            color: 颜色字符串,可以支持偏色,多色,例如 "ffffff-202020|000000-000000" 这个表示白色偏色为202020,和黑色偏色为000000.颜色最多支持10种颜色组合. 注意，这里只支持RGB颜色.
            sim:相似度(0.1-1.0)

        Returns:
            0: 颜色匹配 1: 颜色不匹配
        """
        return self.op.CmpColor(x, y, color, sim)

    def FindColor(self, x1: int, y1: int, x2: int, y2: int, color: str, sim: float, dir: int) -> tuple:
        """
        查找指定区域内的颜色,颜色格式"RRGGBB-DRDGDB",注意,和按键的颜色格式相反

        Args:
            x1:区域的左上X坐标
            y1:区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标
            color:颜色 格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020".注意，这里只支持RGB颜色.
            sim:相似度,取值范围0.1-1.0
            dir:查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左,从下到上 4：从中心往外查找 5: 从上到下,从左到右 6: 从上到下,从右到左 7: 从下到上,从左到右 8: 从下到上,从右到左

        Returns:
            (x1, y1, x2, y2, color, sim, dir,返回X坐标,返回Y坐标)
        """
        return self.op.FindColor(x1, y1, x2, y2, color, sim, dir, 1, 1)

    def FindColorEx(self, x1: int, y1: int, x2: int, y2: int, color: str, sim: float, dir: int) -> str:
        """
        查找指定区域内的所有颜色,颜色格式"RRGGBB-DRDGDB",注意,和按键的颜色格式相反

        Args:
            x1:区域的左上X坐标
            y1:区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标
            color:颜色 格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020".注意，这里只支持RGB颜色.
            sim:相似度,取值范围0.1-1.0
            dir:查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左,从下到上 4：从中心往外查找 5: 从上到下,从左到右 6: 从上到下,从右到左 7: 从下到上,从左到右 8: 从下到上,从右到左

        Returns:
            返回所有颜色信息的坐标值,然后通过GetResultCount等接口来解析 (由于内存限制,返回的颜色数量最多为1800个左右)
        """
        return self.op.FindColorEx(x1, y1, x2, y2, color, sim, dir)

    def FindMultiColor(self, x1: int, y1: int, x2: int, y2: int, first_color: str, offset_color: str, sim: float,
                       dir: int) -> tuple:
        """
        根据指定的多点查找颜色坐标

        Args:
            x1:区域的左上X坐标
            y1:区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标
            first_color:颜色格式为"RRGGBB-DRDGDB|RRGGBB-DRDGDB|…………",比如"123456-000000"这里的含义和按键自带Color插件的意义相同，只不过我的可以支持偏色和多种颜色组合.所有的偏移色坐标都相对于此颜色.注意，这里只支持RGB颜色.
            offset_color:偏移颜色可以支持任意多个点 格式和按键自带的Color插件意义相同, 只不过我的可以支持偏色和多种颜色组合,格式为"x1|y1|RRGGBB-DRDGDB|RRGGBB-DRDGDB……,……xn|yn|RRGGBB-DRDGDB|RRGGBB-DRDGDB……"
                             比如"1|3|aabbcc|aaffaa-101010,-5|-3|123456-000000|454545-303030|565656"等任意组合都可以，支持偏色还可以支持反色模式，比如"1|3|-aabbcc|-334455-101010,-5|-3|-123456-000000|-353535|454545-101010","-"表示除了指定颜色之外的颜色.
            sim:相似度,取值范围0.1-1.0
            dir:查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上

        Returns:
            (x1, y1, x2, y2,first_color,offset_color,sim, dir,返回的X坐标,返回的Y坐标) 坐标是first_color所在的坐标

        """
        return self.op.FindMultiColor(x1, y1, x2, y2, first_color, offset_color, sim, dir, 1, 1)

    def FindMultiColorEx(self, x1: int, y1: int, x2: int, y2: int, first_color: str, offset_color: str, sim: float,
                         dir: int) -> str:
        """
        查找指定区域内的所有颜色,颜色格式"RRGGBB-DRDGDB",注意,和按键的颜色格式相反

        Args:
            x1:区域的左上X坐标
            y1:区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标
            first_color:颜色格式为"RRGGBB-DRDGDB|RRGGBB-DRDGDB|…………",比如"123456-000000"这里的含义和按键自带Color插件的意义相同，只不过我的可以支持偏色和多种颜色组合.所有的偏移色坐标都相对于此颜色.注意，这里只支持RGB颜色.
            offset_color:偏移颜色可以支持任意多个点 格式和按键自带的Color插件意义相同, 只不过我的可以支持偏色和多种颜色组合,格式为"x1|y1|RRGGBB-DRDGDB|RRGGBB-DRDGDB……,……xn|yn|RRGGBB-DRDGDB|RRGGBB-DRDGDB……"
                             比如"1|3|aabbcc|aaffaa-101010,-5|-3|123456-000000|454545-303030|565656"等任意组合都可以，支持偏色还可以支持反色模式，比如"1|3|-aabbcc|-334455-101010,-5|-3|-123456-000000|-353535|454545-101010","-"表示除了指定颜色之外的颜色.
            sim:相似度,取值范围0.1-1.0
            dir:查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上


        Returns:
            返回所有颜色信息的坐标值,然后通过GetResultCount等接口来解析(由于内存限制,返回的坐标数量最多为1800个左右)坐标是first_color所在的坐标
        """
        return self.op.FindMultiColorEx(x1, y1, x2, y2, first_color, offset_color, sim, dir)

    def FindPic(self, x1: int, y1: int, x2: int, y2: int, pic_name: str, delta_color: str, sim: float,
                dir: int) -> tuple:
        """
        查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.

        Args:
            x1:区域的左上X坐标
            y1:区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标
            pic_name:图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            delta_color:颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40 (这里是16进制表示)
            sim:相似度,取值范围0.1-1.0
            dir:查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上

        Returns:
            (x1, y1, x2, y2, pic_name, delta_color,sim, dir,图片左上角的X坐标, 图片左上角的Y坐标)
        """
        return self.op.FindPic(x1, y1, x2, y2, pic_name, delta_color, sim, dir, 1, 1)

    def FindPicEx(self, x1: int, y1: int, x2: int, y2: int, pic_name: str, delta_color: str, sim: float,
                  dir: int) -> str:
        """
        查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.这个函数可以查找多个图片,并且返回所有找到的图像的坐标.

        Args:
            x1:区域的左上X坐标
            y1:区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标
            pic_name:图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp"
            delta_color:颜色色偏比如"203040" 表示RGB的色偏分别是20 30 40 (这里是16进制表示)
            sim:相似度,取值范围0.1-1.0
            dir:查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上

        Returns:
            返回的是所有找到的坐标格式如下"id,x,y|id,x,y..|id,x,y" (图片左上角的坐标)比如"0,100,20|2,30,40" 表示找到了两个,第一个,对应的图片是图像序号为0的图片,坐标是(100,20),第二个是序号为2的图片,坐标(30,40) (由于内存限制,返回的图片数量最多为1500个左右)
        """

        return self.op.FindPicEx(x1, y1, x2, y2, pic_name, delta_color, sim, dir)

    def GetColor(self, x: int, y: int) -> str:
        """
        获取(x,y)的颜色,颜色返回格式"RRGGBB",注意,和按键的颜色格式相反

        Args:
            x:X坐标
            y:Y坐标
        Returns:
            颜色字符串(注意这里都是小写字符，和工具相匹配)
        """
        return self.op.GetColor(x, y)

    def CapturePre(self, file: str) -> int:
        """
        抓取上次操作的图色区域，保存为file(32位位图)

        Args:
            file:保存的文件名,保存的地方一般为SetPath中设置的目录,当然这里也可以指定全路径名.

        Returns:
             0代表失败 1代表成功

        注意，要开启此函数，必须先调用EnableDisplayDebug 任何图色或者文字识别函数，都可以通过这个来截取.

        """
        return self.op.CapturePre(file)

    def EnableDisplayDebug(self, enable_debug: int) -> int:
        """
        开启图色调试模式，此模式会稍许降低图色和文字识别的速度.默认不开启.

        Args:
            enable_debug:0为关闭  1为开启

        Returns:
             0代表失败 1代表成功

        """
        return self.op.EnableDisplayDebug(enable_debug)

    def GetScreenData(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """
        获取指定区域的图像,用二进制数据的方式返回,（不适合按键使用）方便二次开发.

        Args:
            x1:区域的左上X坐标
            y1:区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标

        Returns:
            返回的是指定区域的二进制颜色数据地址,每个颜色是4个字节,表示方式为(BBGGRR00)

        注意,调用完此接口后，返回的数据指针在当前op对象销毁时，或者再次调用GetScreenData时，会自动释放.

        """
        return self.op.GetScreenData(x1, y1, x2, y2)

    def GetScreenDataBmp(self, x1: int, y1: int, x2: int, y2: int) -> tuple:
        """
        获取指定区域的图像,用24位位图的数据格式返回,方便二次开发.（或者可以配合SetDisplayInput的mem模式）

        Args:
            x1:区域的左上X坐标
            y1:区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标

        Returns:
             (x1,y1,x2,y2,返回图片的数据,返回图片的数据长度)
        """
        return self.op.GetScreenDataBmp(x1, y1, x2, y2, 1, 1)

    def SetDisplayInput(self, mode: str) -> int:
        """
        设定图色的获取方式，默认是显示器或者后台窗口(具体参考BindWindow)

        Args:
            mode:图色输入模式取值有以下几种
                    "screen" 这个是默认的模式，表示使用显示器或者后台窗口
                    "pic:file" 指定输入模式为指定的图片,如果使用了这个模式，则所有和图色相关的函数均视为对此图片进行处理，比如文字识别查找图片 颜色 等等一切图色函数.需要注意的是，设定以后，此图片就已经加入了缓冲，如果更改了源图片内容，那么需要 释放此缓冲，重新设置.
                    "mem:addr" 指定输入模式为指定的图片,此图片在内存当中. addr为图像内存地址,一般是GetScreenDataBmp的返回值（前54字节为位图信息，后面的是像素数据），注意与大漠的区别.如果使用了这个模式，则所有和图色相关的函数,均视为对此图片进行处理.比如文字识别 查找图片 颜色 等等一切图色函数所有坐标都相对此图片，如果不想受到影响，调用GetScreenDataBmp时应时整个窗口的大小.

        Returns:
             0代表失败 1代表成功
        """
        return self.op.SetDisplayInput(mode)

    """----------------------------------------常用算法------------------------------------------------"""

    def AStarFindPath(self, mapWidth: int, mapHeight: int, disable_points: str, beginX: int, beginY: int, endX: int,
                      endY: int) -> int:
        """
        A星算法

        Args:
            mapWidth:区域的左上X坐标
            mapHeight:区域的左上Y坐标
            disable_points:不可通行的坐标，以"|"分割，例如:"10,15|20,30"
            beginX:源坐标X
            beginY:源坐标Y
            endX:目的坐标X
            endY:目的坐标Y

        Returns:
            0代表失败 1代表成功
        """
        return self.op.AStarFindPath(mapWidth, mapHeight, disable_points, beginX, beginY, endX, endY)

    """----------------------------------------文字识别------------------------------------------------"""

    def FindStr(self, x1: int, y1: int, x2: int, y2: int, string_: str, color_format: str, sim: float) -> tuple:
        """
        在屏幕范围(x1,y1,x2,y2)内,查找string(可以是任意个字符串的组合),并返回符合color_format的坐标位置,相似度sim同Ocr接口描述.(多色,差色查找类似于Ocr接口,不再重述)

        Args:
            x1:区域的左上X坐标
            y1::区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标
            string_:待查找的字符串,可以是字符串组合，比如"长安|洛阳|大雁塔",中间用"|"来分割字符串
            color_format:颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例 .注意，RGB和HSV格式都支持
            sim:双精度浮点数:相似度,取值范围0.1-1.0

        Returns:
            (x1,y1,x2,y2,string_,color_format,sim,返回X坐标没找到返回-1,返回Y坐标没找到返回-1)

        示例:

            op_ret = op.FindStr(0,0,2000,2000,"长安","9f2e3f-000000",1.0,intX,intY)
            If intX >= 0 and intY >= 0 Then
                 op.MoveTo intX,intY
            End If

            op_ret = op.FindStr(0,0,2000,2000,"长安|洛阳","9f2e3f-000000",1.0,intX,intY)
            If intX >= 0 and intY >= 0 Then
                 op.MoveTo intX,intY
            End If

            // 查找时,对多行文本进行换行,换行分隔符是"|". 语法是在","后增加换行字符串.任意字符串都可以.
            op_ret = op.FindStr(0,0,2000,2000,"长安|洛阳","9f2e3f-000000,|",1.0,intX,intY)
            If intX >= 0 and intY >= 0 Then
                 op.MoveTo intX,intY
            End If
            注: 此函数的原理是先Ocr识别，然后再查找。

        """
        return self.op.FindStr(x1, y1, x2, y2, string_, color_format, sim, 1, 1)

    def FindStrEx(self, x1: int, y1: int, x2: int, y2: int, string_: str, color_format: str, sim: float) -> str:
        """
        在屏幕范围(x1,y1,x2,y2)内,查找string(可以是任意个字符串的组合),并返回符合color_format的坐标位置,相似度sim同Ocr接口描述.(多色,差色查找类似于Ocr接口,不再重述)

        Args:
            x1:区域的左上X坐标
            y1::区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标
            string_:待查找的字符串,可以是字符串组合，比如"长安|洛阳|大雁塔",中间用"|"来分割字符串
            color_format:颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例 .注意，RGB和HSV格式都支持
            sim:双精度浮点数:相似度,取值范围0.1-1.0

        Returns:
            返回所有找到的坐标集合,格式如下: "id,x0,y0|id,x1,y1|......|id,xn,yn" 比如"0,100,20|2,30,40" 表示找到了两个,第一个,对应的是序号为0的字符串,坐标是(100,20),第二个是序号为2的字符串,坐标(30,40)

        示例:

            op_ret = op.FindStrEx(0,0,2000,2000,"长安|洛阳","9f2e3f-000000",1.0)
            If len(op_ret) > 0 Then
               ss = split(op_ret,"|")
               index = 0
               count = UBound(ss) + 1
               Do While index < count
                  TracePrint ss(index)
                  sss = split(ss(index),",")
                  id = int(sss(0))
                  x = int(sss(1))
                  y = int(sss(2))
                  op.MoveTo x,y
                  Delay 1000
                  index = index+1
               Loop
            End If
            注: 此函数的原理是先Ocr识别，然后再查找。

        """
        return self.op.FindStrEx(x1, y1, x2, y2, string_, color_format, sim)

    def Ocr(self, x1: int, y1: int, x2: int, y2: int, color_format: str, sim: float) -> str:
        """
        识别屏幕范围(x1,y1,x2,y2)内符合color_format的字符串,并且相似度为sim,sim取值范围(0.1-1.0),这个值越大越精确,越大速度越快,越小速度越慢,请斟酌使用!

        Args:
            x1:区域的左上X坐标
            y1:区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标
            color_format:区域的右下Y坐标
            sim:双精度浮点数:相似度,取值范围0.1-1.0

        Returns:
            返回识别到的字符串

        示例:

            //RGB单色识别
            s = op.Ocr(0,0,2000,2000,"9f2e3f-000000",1.0)
            MessageBox s

            //RGB单色差色识别
            s = op.Ocr(0,0,2000,2000,"9f2e3f-030303",1.0)
            MessageBox s

            //RGB多色识别(最多支持10种,每种颜色用"|"分割)
            s = op.Ocr(0,0,2000,2000,"9f2e3f-030303|2d3f2f-000000|3f9e4d-100000",1.0)
            MessageBox s

        """
        return self.op.Ocr(x1, y1, x2, y2, color_format, sim)

    def OcrEx(self, x1: int, y1: int, x2: int, y2: int, color_format: str, sim: float) -> str:
        """
        识别屏幕范围(x1,y1,x2,y2)内符合color_format的字符串,并且相似度为sim,sim取值范围(0.1-1.0),这个值越大越精确,越大速度越快,越小速度越慢,请斟酌使用!这个函数可以返回识别到的字符串，以及每个字符的坐标.

        Args:
            x1:区域的左上X坐标
            y1:区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标
            color_format:区域的右下Y坐标
            sim:双精度浮点数:相似度,取值范围0.1-1.0

        Returns:
            返回识别到的字符串 格式如 "字符0$x0$y0|…|字符n$xn$yn"
        """
        return self.op.OcrEx(x1, y1, x2, y2, color_format, sim)

    def SetDict(self, index: int, file: str) -> int:
        """
        设置字库文件

        Args:
            index:字库的序号,取值为0-19,目前最多支持20个字库
            file:字库文件名

        Returns:
            0代表失败 1代表成功
        """
        return self.op.SetDict(index, file)

    def UseDict(self, index: int) -> int:
        """
        表示使用哪个字库文件进行识别(index范围:0-9)设置之后，永久生效，除非再次设定

        Args:
            index:字库编号(0-9)

        Returns:
            0代表失败 1代表成功
        """
        return self.op.UseDict(index)

    def OcrAuto(self, x1: int, y1: int, x2: int, y2: int, sim: float) -> str:
        """
        识别屏幕范围(x1,y1,x2,y2)内的字符串,自动二值化，而无需指定颜色,适用于字体颜色和背景相差较大的场合

        Args:
            x1:区域的左上X坐标
            y1:区域的左上Y坐标
            x2:区域的右下X坐标
            y2:区域的右下Y坐标
            sim:相似度,取值范围0.1-1.0

        Returns:
            返回识别到的字符串
        """
        return self.op.OcrAuto(x1, y1, x2, y2, sim)

    def OcrFromFile(self, file_name: str, color_format: str, sim: float) -> str:
        """

        Args:
            file_name:文件名
            color_format:颜色格式串
            sim:相似度,取值范围0.1-1.0

        Returns:
            返回识别到的字符串
        """
        return self.op.OcrFromFile(file_name, color_format, sim)

    def OcrAutoFromFile(self, file_name: str, sim: float) -> str:
        """

        Args:
            file_name:文件名
            sim:相似度,取值范围0.1-1.0

        Returns:
            返回识别到的字符串
        """
        return self.op.OcrAutoFromFile(file_name, sim)

    """----------------------------------------系统设置------------------------------------------------"""

    # def Beep(self, duration: int = 1000, f: int = 800) -> int:
    #     """
    #     蜂鸣器
    #
    #     Args:
    #         duration:时长(ms)
    #         f: 频率
    #
    #     Returns:
    #         0代表失败，1代表成功
    #     """
    #     return self.op.Beep(f, duration)
    #
    # def ExitOs(self, _type: int) -> int:
    #     """
    #     退出系统(注销 重启 关机)
    #
    #     Args:
    #         _type: 取值为以下类型 0 : 注销系统 1 : 关机 2 : 重新启动
    #
    #     Returns:
    #         0代表失败，1代表成功
    #
    #     """
    #     return self.op.ExitOs(_type)
    #
    # def GetClipboard(self) -> str:
    #     """
    #     获取剪贴板的内容
    #
    #     Returns:
    #         以字符串表示的剪贴板内容
    #     """
    #     return self.op.GetClipboard()
    #
    # def GetMachineCode(self) -> str:
    #     """
    #     获取本机的机器码.(带网卡). 此机器码用于插件网站后台. 要求调用进程必须有管理员权限. 否则返回空串.
    #
    #     Returns:
    #         字符串:字符串表达的机器机器码
    #
    #     注: 此机器码包含的硬件设备有硬盘,显卡,网卡等. 其它不便透露. 重装系统不会改变此值.
    #     另要注意,插拔任何USB设备,(U盘，U盾,USB移动硬盘,USB键鼠等),以及安装任何网卡驱动程序,(开启或者关闭无线网卡等)都会导致机器码改变.
    #
    #     """
    #     return self.op.GetMachineCode()
    #
    # def GetDiskSerial(self) -> str:
    #     """
    #     获取本机的硬盘序列号.支持ide scsi硬盘. 要求调用进程必须有管理员权限. 否则返回空串.
    #
    #     Returns:
    #         字符串表达的硬盘序列号
    #
    #     """
    #     return self.op.GetDiskSerial()
    #
    # def GetMachineCodeNoMac(self) -> str:
    #     """
    #     获取本机的机器码.(不带网卡) 要求调用进程必须有管理员权限. 否则返回空串.
    #
    #     Returns:
    #         字符串表达的机器机器码
    #
    #     注: 此机器码包含的硬件设备有硬盘,显卡,网卡等. 其它不便透露. 重装系统不会改变此值.
    #     另要注意,插拔任何USB设备,(U盘，U盾,USB移动硬盘,USB键鼠等),以及安装任何网卡驱动程序,(开启或者关闭无线网卡等)都会导致机器码改变.
    #
    #     """
    #     return self.op.GetMachineCodeNoMac()
    #
    # def GetScreenHeight(self) -> int:
    #     """
    #     获取屏幕的高度.
    #
    #     Returns:
    #         返回屏幕的高度
    #     """
    #     return self.op.GetScreenHeight()
    #
    # def GetScreenWidth(self) -> int:
    #     """
    #     获取屏幕的宽度.
    #
    #     Returns:
    #         返回屏幕的宽度
    #     """
    #     return self.op.GetScreenWidth()
    #
    # def GetTime(self) -> int:
    #     """
    #     获取当前系统从开机到现在所经历过的时间，单位是毫秒
    #
    #     Returns:
    #         时间(单位毫秒)
    #     """
    #     return self.op.GetTime()
    #
    # def SetClipboard(self, value: str) -> int:
    #     """
    #     设置剪贴板的内容
    #
    #     Args:
    #         value: 以字符串表示的剪贴板内容
    #
    #     Returns:
    #         0代表失败，1代表成功
    #     """
    #     return self.op.SetClipboard(value)
