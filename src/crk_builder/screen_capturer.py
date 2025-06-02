import os
import pyautogui as pag
import shutil
import time

class ScreenCapturer:
    def __init__(self, rows: int):
        self.__rows             : int = rows
        self.__screenshot_folder: str = ""
        self.__topping_number   : int = 1

        self.__reset_folder()

    # Iterate the specified number of rows and take screenshots
    def capture_screen(self) -> None:
        # Coordinates of the topping [1, 1]
        first_topping_x: int = 1085 # (- Left, + Right)
        first_topping_y: int = 325  # (- Up  , + Down )

        # Offset to move to the next row or column
        next_topping   : int = 172

        # Variables for the scrolling algorithm
        current_block  : int = 1 # Every 4 rows increases by 1
        current_row    : int = 1

        # Iteration of the rows
        # In the range() function we increment by 1 because it's exclusive
        for row in range(1, self.__rows + 1):
            # Scrolls one block, that is, four rows
            if (current_row > 4 and ((current_row - 1) % 4) == 0
                    and self.__rows >= current_block * 4):
                pag.click(1085, 325 + (next_topping * 3)) # Topping [4, 1]
                pag.mouseDown()
                pag.moveTo(1085, 117, duration = 1)       # Moves upward
                time.sleep(0.5)
                pag.mouseUp()

                # Reset coordinates to the topping [1, 1]
                first_topping_x = 1085
                first_topping_y = 325
            # Scrolls one row
            elif current_row > 4 and self.__rows < current_block * 4:
                pag.click(1085, 325 + (next_topping * 3)) # Topping [4, 1]
                pag.mouseDown()
                pag.moveTo(1085, 659, duration = 1)       # Moves upward
                time.sleep(0.5)
                pag.mouseUp()

                # Reset coordinates to the topping [4, 1]
                first_topping_x = 1085
                first_topping_y = 325 + (next_topping * 3)

            # Iteration of the columns
            for column in range(1, 6):
                time.sleep(0.125)
                pag.click(first_topping_x, first_topping_y)
                time.sleep(0.125)
                self.__take_screenshot()
                first_topping_x += next_topping  # Move to the next column

            # The entire row has been iterated, now start with the row below
            first_topping_x  = 1085
            first_topping_y += next_topping

            # For the scrolling algorithm, every 4 rows increases by 1
            if current_row % 4 == 0:
                current_block += 1
            current_row += 1

    def __reset_folder(self) -> None:
        current_path             : str = os.path.dirname(os.path.abspath(__file__))
        self.__screenshot_folder : str = os.path.abspath(os.path.join(current_path
            , "..", "..", "topping_screenshots"))

        # Delete and create a new folder every time
        if os.path.exists(self.__screenshot_folder):
            shutil.rmtree(self.__screenshot_folder)
        if not os.path.exists(self.__screenshot_folder):
            os.makedirs(self.__screenshot_folder)

    def __take_screenshot(self) -> None:
        screenshot_path: str = os.path.join(self.__screenshot_folder, "topping_capture_"
            + str(self.__topping_number) + ".png")

        # X (+ Right, - Left), Y (+ Down, - Up), Width (+, -), Height (+, -)
        topping_screenshot = pag.screenshot(region = (120, 635, 740, 180))
        topping_screenshot.save(screenshot_path)
        self.__topping_number += 1