## `RunApp(self, app_path, mode)`

运行指定的应用程序.

Parameters:

- **app_path** (`str`) – 指定的可执行程序全路径.
- **mode** (`int`) – 取值如下 0:普通模式 1:加强模式

Returns:

- `int` – 0 代表失败，1 代表成功

## `WinExec(self, cmdline, cmdshow)`

运行指定的应用程序.

Parameters:

- **cmdline** (`str`) – 指定的可执行程序全路径.
- **cmdshow** (`int`) – 取值如下 0:隐藏 1:用最近的大小和位置显示, 激活

Returns:

- `str` – 0 代表失败，1 代表成功

## `GetCmdStr(self, cmdline, millseconds)`

运行指定的应用程序.

Parameters:

- **cmdline** (`str`) – 指定的可执行程序全路径.
- **millseconds** (`int`) – 等待的时间(毫秒)

Returns:

- `str` – cmd 输出的字符
