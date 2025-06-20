from PIL import Image

import os
import pyautogui as pag
import shutil
import time

class ScreenCapturer:
    def __init__(self, rows: int):
        self.__rows              : int = rows
        self.__screenshots_folder: str = ""
        self.__topping_number    : int = 1 # Number used to differentiate topping screenshots

        self.__clean_folder()

    # Take screenshots according to the number of rows provided
    def capture_screen(self) -> None:
        # Coordinates of the topping at position [1, 1]
        first_topping_x: int = 1085 # (- Left, + Right)
        first_topping_y: int = 325  # (- Up  , + Down )

        # Offset to move to the next row or column
        next_topping   : int = 172

        # Variables for the scrolling algorithm
        current_block  : int = 1
        current_row    : int = 1

        # Safety timeout for the window to maximize properly before taking screenshots
        time.sleep(1)

        # Iteration of the rows
        # The second argument of the range() function is exclusive, so we increase by 1
        for row in range(1, self.__rows + 1):
            # Scrolls one block (four rows) upwards
            if (current_row > 4 and ((current_row - 1) % 4) == 0
                    and self.__rows >= current_block * 4):
                pag.click(1085, 325 + (next_topping * 3)) # Topping at position [4, 1]
                pag.mouseDown()
                pag.moveTo(1085, 117, duration = 1)       # Moves upward
                time.sleep(0.5)
                pag.mouseUp()

                # Reset coordinates to the topping at position [1, 1]
                first_topping_x = 1085
                first_topping_y = 325
            # Scrolls one row upwards
            elif current_row > 4 and self.__rows < current_block * 4:
                pag.click(1085, 325 + (next_topping * 3)) # Topping at position [4, 1]
                pag.mouseDown()
                pag.moveTo(1085, 659, duration = 1)       # Moves upward
                time.sleep(0.5)
                pag.mouseUp()

                # Reset coordinates to the topping at position [4, 1]
                first_topping_x = 1085
                first_topping_y = 325 + (next_topping * 3)

            # Iteration of the columns
            for column in range(1, 6):
                time.sleep(0.25)
                pag.click(first_topping_x, first_topping_y)
                time.sleep(0.25)
                self.__take_screenshot()
                first_topping_x += next_topping  # Move to the next column/topping on the same row

            # The entire row has been iterated, now start with the row below
            first_topping_x  = 1085
            first_topping_y += next_topping

            # For the scrolling algorithm, every 4 rows increases the variable by 1
            if current_row % 4 == 0:
                current_block += 1
            current_row += 1

    def __clean_folder(self) -> None:
        # Create a path for the screenshots folder
        current_path             : str = os.path.dirname(os.path.abspath(__file__))
        self.__screenshots_folder: str = os.path.abspath(os.path.join(current_path
            , "..", "..", "topping_screenshots"))

        # Deletes and creates the folder each time the program is run
        if os.path.exists(self.__screenshots_folder):
            shutil.rmtree(self.__screenshots_folder)
        if not os.path.exists(self.__screenshots_folder):
            os.makedirs(self.__screenshots_folder)

    def __take_screenshot(self) -> None:
        # Create a path for every topping screenshot
        screenshot_file: str = os.path.join(self.__screenshots_folder, "topping_capture_"
            + str(self.__topping_number) + ".png")

        # To adjust the size of the screenshot, first set the X and Y, then Width and Height
        # X (+ Right, - Left), Y (+ Down, - Up), Width, Height
        topping_screenshot: Image = pag.screenshot(region = (120, 635, 740, 180))
        topping_screenshot.save(screenshot_file)
        self.__topping_number += 1