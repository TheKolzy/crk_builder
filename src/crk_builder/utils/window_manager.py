from pygetwindow import Win32Window
from typing      import Optional

import pyautogui   as pag
import pygetwindow as pgw

class WindowManager:
    def __init__(self, window_name: str):
        self.__window_name: str                   = window_name
        self.__window     : Optional[Win32Window] = None

    # Changes the window to full screen mode, assuming a screen size of 1920x1080
    def configure_window(self) -> bool:
        if not self.__find_window():
            return False

        self.__resize_window()
        return True

    def __find_window(self) -> bool:
        window_list: list[Win32Window] = pgw.getWindowsWithTitle(self.__window_name)

        if not window_list:
            print(f"[Error]: The \"{self.__window_name}\" window could not be found.")
            return False

        # The first element in the list is the window we are looking for
        self.__window = window_list[0]
        return True

    def __resize_window(self) -> None:
        if self.__window.isMinimized:
            self.__window.restore()

        # Bring the window to the foreground
        if not self.__window.isActive:
            self.__window.activate()

        if not self.__is_fullscreen():
            # BS5 specific keyboard shortcut to put in full screen mode
            pag.press("F11")

    def __is_fullscreen(self) -> bool:
        # Along with the abs() function, there will be an error tolerance of +/- 1
        threshold: int = 1
        return (
            # Full screen size in BS5 is: 0, 0, 1920, 1080
            abs(self.__window.left) <= threshold and
            abs(self.__window.top ) <= threshold and
            abs(self.__window.width  - pag.size().width ) <= threshold and
            abs(self.__window.height - pag.size().height) <= threshold
        )