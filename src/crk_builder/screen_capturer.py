import pyautogui as pag

class ScreenCapturer:
    def __init__(self, rows: int):
        self.__rows: int = 2

    def capture_screen(self):
        self.__click_topping()

    def __click_topping(self) -> None:
        # Coordinates of the topping: [1, 1], assuming screen size is 1920x1080
        first_topping_x: int = 1085 # (- Left, + Right)
        first_topping_y: int = 325  # (- Up  , + Down )

        # Offset to move to the next column or row
        next_topping: int = 172

        # We add one because it's exclusive
        for row in range(1, self.__rows + 1):
            for column in range(1, 6):
                pag.click(first_topping_x, first_topping_y)
                first_topping_x += next_topping
            first_topping_x = 1085
            first_topping_y += next_topping