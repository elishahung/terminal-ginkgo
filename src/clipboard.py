import platform

import pyautogui
import pyperclip


def copy_to_input(text: str) -> None:
    """
    Copy text to clipboard and paste it to the current input field.

    Uses Ctrl+V on Windows and Cmd+V on macOS.

    Args:
        text: Text to copy and paste
    """
    pyperclip.copy(text)
    if platform.system() == "Windows":
        pyautogui.hotkey("ctrl", "v")
    else:
        pyautogui.hotkey("command", "v")
