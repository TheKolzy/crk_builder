from crk_builder.screen_capturer      import ScreenCapturer
from crk_builder.substat_optimizer    import SubstatOptimizer
from crk_builder.text_extractor       import TextExtractor
from crk_builder.utils.window_manager import WindowManager

# CRK VERSION 6.4.102

# [Warning]: Make sure your BS5 instance is named as follows, otherwise it will not work
WINDOW_NAME: str = "BlueStacks App Player"

ROWS       : int = 1

# You can only specify 2 or 3 substats
# | 0 ATK | 1 ATK SPD | 2 CRIT% | 3 Cooldown | 4 DMG Resist |
SUBSTATS   : tuple[int, ...] = (3, 4)

def main() -> None:
    wm: WindowManager    = WindowManager(WINDOW_NAME)
    if not wm.configure_window():
        return

    sc: ScreenCapturer   = ScreenCapturer(ROWS)
    sc.capture_screen()

    te: TextExtractor    = TextExtractor(ROWS)
    te.process_images()

    so: SubstatOptimizer = SubstatOptimizer()
    so.perform_optimization(SUBSTATS)

if __name__ == "__main__":
    main()