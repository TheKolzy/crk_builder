from crk_builder.utils.window_manager import WindowManager

WINDOW_NAME: str = "BlueStacks App Player"

def main() -> None:
    wm: WindowManager = WindowManager(WINDOW_NAME)
    wm.configure_window()

if __name__ == "__main__":
    main()