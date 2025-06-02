from crk_builder.screen_capturer      import ScreenCapturer
from crk_builder.text_extractor       import TextExtractor
from crk_builder.utils.window_manager import WindowManager

# [Warning]: Make sure your BS5 instance is named as follows, otherwise it will not work
WINDOW_NAME: str = "BlueStacks App Player"

ROWS       : int = 1

def main() -> None:
    wm: WindowManager = WindowManager(WINDOW_NAME)
    if not wm.configure_window():
        return

    sc: ScreenCapturer = ScreenCapturer(ROWS)
    sc.capture_screen()

    te: TextExtractor = TextExtractor(ROWS)
    te.process_images()

if __name__ == "__main__":
    main()