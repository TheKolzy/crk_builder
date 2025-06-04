from PIL import Image

import os
import pytesseract

class TextExtractor:
    # The rows are used to know the number of toppings there are
    def __init__(self, rows: int):
        self.__topping_count: int = rows * 5

    def process_images(self) -> None:
        # Calculate paths for files/folders
        current_path     : str = os.path.dirname(os.path.abspath(__file__))
        screenshot_folder: str = os.path.abspath(os.path.join(current_path
            , "..", "..", "topping_screenshots"))
        text_path        : str = os.path.abspath(os.path.join(current_path
            , "..", "..", "topping_substats.txt"))

        # Empty the text file before writing to it
        open(text_path, 'w').close()

        # The second argument of the range() function is exclusive, so we increase by 1
        for topping in range(1, self.__topping_count + 1):
            # Loads and extracts the substats from the topping screenshot
            screenshot_path   : str   = os.path.join(screenshot_folder, "topping_capture_"
                + str(topping) + ".png")
            topping_screenshot: Image = Image.open(screenshot_path)
            topping_text      : str   = pytesseract.image_to_string(topping_screenshot)

            # Writes the topping substats to a text file
            with open(text_path, "a") as topping_file:
                topping_file.write("[Topping " + str(topping) + "]\n")
                topping_file.write(topping_text)
                topping_file.write("\n")