from pygetwindow import Win32Window
from typing      import Optional

import pygetwindow as pgw

class WindowManager:
    def __init__(self, window_name: str) -> None:
        self.__window_name: str                   = window_name
        self.__window     : Optional[Win32Window] = None

    def configure_window(self) -> None:
        if not self.__find_window():
            return

    def __find_window(self) -> bool:
        # List of windows with this name
        window_list = pgw.getWindowsWithTitle(self.__window_name)

        if not window_list:
            print(f"[Error]: The \"{self.__window_name}\" window has not been found.")
            return False

        # The first element in the list is the window
        self.__window = window_list[0]
        return True