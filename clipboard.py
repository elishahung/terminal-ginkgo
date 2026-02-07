import pyperclip
import platform
import pyautogui

def copy_to_input(text: str):
    pyperclip.copy(text)
    if platform.system() == "Windows":
        pyautogui.hotkey("ctrl", "v")
    else:
        pyautogui.hotkey("command", "v")
