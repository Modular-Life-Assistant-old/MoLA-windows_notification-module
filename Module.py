import tempfile
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
        # Register the Window class.
        wc = WNDCLASS()
        wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        self.classAtom = RegisterClass(wc)

    def is_available(self):
        return os.name == 'nt'

    def send(self, msg, image=None, sound=None):
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        hwnd = CreateWindow(
            self.classAtom, "Taskbar", style,
            0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
            0, 0, GetModuleHandle(None), None
        )
        UpdateWindow(hwnd)

        if image:
            img_path = os.path.join(tempfile.gettempdir(), 'mola_notif.ico')
            image.save(img_path)
            flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = LoadImage(0, img_path, win32con.IMAGE_ICON, 0, 0, flags)
            # TODO: add thumbnail in notification
            # TODO: action click on notification (open image)

        else:
            hicon = LoadIcon(0, win32con.IDI_APPLICATION)

        Shell_NotifyIcon(NIM_ADD, (
            hwnd, 0, NIF_INFO | NIF_ICON | NIF_MESSAGE | NIF_TIP,
            win32con.WM_USER+20, hicon, "tooltip", msg, 200, settings.NAME,
            0x20 | 0x04  # NIIF_LARGE_ICON | NIIF_USER
        ))