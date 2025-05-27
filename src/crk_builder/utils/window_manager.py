from pygetwindow import Win32Window
from typing      import Optional

import pyautogui   as pag
import pygetwindow as pgw

class WindowManager:
    def __init__(self, window_name: str):
        self.__window_name: str                   = window_name
        self.__window     : Optional[Win32Window] = None

    def configure_window(self) -> None:
        if not self.__find_window():
            return

        self.__resize_window()

    def __find_window(self) -> bool:
        window_list: list[Win32Window] = pgw.getWindowsWithTitle(self.__window_name)

        if not window_list:
            print(f"[Error]: The \"{self.__window_name}\" window could not be found.")
            return False

        # The first element is the window
        self.__window = window_list[0]
        return True

    def __resize_window(self) -> None:
        if self.__window.isMinimized:
            self.__window.restore()

        # Bring the window to the foreground
        if not self.__window.isActive:
            self.__window.activate()

        if not self.__is_fullscreen():
            pag.press("F11")

    def __is_fullscreen(self) -> bool:
        # Value +/- 1 with abs
        threshold: int = 1
        return (
            # 0, 0, 1920, 1080
            abs(self.__window.left) <= threshold and
            abs(self.__window.top ) <= threshold and
            abs(self.__window.width  - pag.size().width ) <= threshold and
            abs(self.__window.height - pag.size().height) <= threshold
        )