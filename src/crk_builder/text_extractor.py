from PIL import Image

import os
import pytesseract

class TextExtractor:
    def __init__(self, rows: int):
        self.__topping_count: int = rows * 5

    def process_images(self) -> None:
        current_path      : str = os.path.dirname(os.path.abspath(__file__))
        screenshots_folder: str = os.path.abspath(os.path.join(current_path
            , "..", "..", "topping_screenshots"))
        # I create the path for the .txt file that will store the toppings substats
        text_path         : str = os.path.abspath(os.path.join(current_path
            , "..", "..", "topping_substats.txt"))

        # Clean the text file before using it
        open(text_path, 'w').close()

        # In the range() function we increment by 1 because it's exclusive
        for topping_number in range(1, self.__topping_count + 1):
            topping_path: str  = os.path.join(screenshots_folder, "topping_capture_"
                + str(topping_number) + ".png")
            topping_screenshot = Image.open(topping_path)
            topping_text       = pytesseract.image_to_string(topping_screenshot)

            with open(text_path, "a") as topping_file:
                topping_file.write("[Topping " + str(topping_number) + "]\n")
                topping_file.write(topping_text)
                topping_file.write("\n")