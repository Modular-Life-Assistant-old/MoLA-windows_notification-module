from core import settings
from helpers.modules.NotificationModule import NotificationModule


import os
try:
    from win32api import *
    from win32gui import *
    import win32con
except ImportError:
    if os.name == 'nt':
        from core import Log
        Log.crash('python package "pywin32" is required')


class Module(NotificationModule):
    def init(self):
        def on_destroy(self, hwnd, msg, wparam, lparam):
            Shell_NotifyIcon(NIM_DELETE, (hwnd, 0))
            PostQuitMessage(0)

        # Register the Window class.
        wc = WNDCLASS()
        wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = {
                win32con.WM_DESTROY: on_destroy,
        }
        self.classAtom = RegisterClass(wc)

    def is_available(self):
        return os.name == 'nt'

    def send(self, msg):
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        hwnd = CreateWindow(
            self.classAtom, "Taskbar", style,
            0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
            0, 0, GetModuleHandle(None), None
        )
        UpdateWindow(hwnd)
        hicon = LoadIcon(0, win32con.IDI_APPLICATION)

        """
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        hicon = LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        """

        Shell_NotifyIcon(NIM_ADD, (
            hwnd, 0, NIF_ICON | NIF_MESSAGE | NIF_TIP, win32con.WM_USER+20, hicon, "tooltip"
        ))
        Shell_NotifyIcon(NIM_MODIFY, (
            hwnd, 0, NIF_INFO, win32con.WM_USER+20, hicon, "Balloon tooltip", msg, 200, settings.NAME
        ))
