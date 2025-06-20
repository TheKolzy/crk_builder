from PIL import Image

import os
import pytesseract

class TextExtractor:
    # The number of rows is used to calculate how many toppings there are
    def __init__(self, rows: int):
        self.__topping_count: int = rows * 5

    def process_image(self) -> None:
        # Get the path of the screenshots folder and create the substats file path
        current_path      : str = os.path.dirname(os.path.abspath(__file__))
        screenshots_folder: str = os.path.abspath(os.path.join(current_path
            , "..", "..", "topping_screenshots"))
        substats_file     : str = os.path.abspath(os.path.join(current_path
            , "..", "..", "topping_substats.txt"))

        # Clears the substats file before writing to it
        open(substats_file, 'w').close()

        # The second argument of the range() function is exclusive, then it's increased by 1
        for topping_index in range(1, self.__topping_count + 1):
            # Loads the topping screenshots and then extract the substats from them
            screenshot_file   : str   = os.path.join(screenshots_folder, "topping_capture_"
                + str(topping_index) + ".png")
            topping_screenshot: Image = Image.open(screenshot_file)
            substats_text     : str   = pytesseract.image_to_string(topping_screenshot)

            # Writes the topping substats to the substats file
            with open(substats_file, "a") as topping_file:
                topping_file.write("[Topping " + str(topping_index) + "]\n")
                topping_file.write(substats_text)
                topping_file.write("\n")