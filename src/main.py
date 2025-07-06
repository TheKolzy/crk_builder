from crk_builder.screen_capturer      import ScreenCapturer
from crk_builder.substat_optimizer    import SubstatOptimizer
from crk_builder.text_extractor       import TextExtractor
from crk_builder.utils.window_manager import WindowManager

# CRK VERSION 6.6.002

# Tested only with BS5 emulator
WINDOW_NAME: str = "BlueStacks App Player"

ROWS       : int = 1

# Only 2 or 3 substats can be specified at the same time
# | 0 ATK | 1 HP | 2 ATK SPD | 3 CRIT% | 4 Cooldown | 5 DMG Resist |
SUBSTATS   : tuple[int, ...] = (4, 5)

def main() -> None:
    wm: WindowManager    = WindowManager(WINDOW_NAME)
    if not wm.configure_window():
        return

    sc: ScreenCapturer   = ScreenCapturer(ROWS)
    sc.capture_screen()

    te: TextExtractor    = TextExtractor(ROWS)
    te.process_image()

    so: SubstatOptimizer = SubstatOptimizer(True)
    so.perform_optimization(SUBSTATS)

if __name__ == "__main__":
    main()