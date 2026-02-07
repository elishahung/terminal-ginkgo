import platform
import pyperclip
from pynput.keyboard import Key, Controller

keyboard = Controller()

def copy_to_input(text: str) -> None:
    """
    Copy text to clipboard and paste it to the current input field.

    Uses Ctrl+V on Windows and Cmd+V on macOS.

    Args:
        text: Text to copy and paste
    """
    pyperclip.copy(text)
    system = platform.system()
    
    if system == "Darwin":  # macOS
        modifier = Key.cmd
    else:  # Windows 或 Linux
        modifier = Key.ctrl

    # 3. 執行貼上動作
    with keyboard.pressed(modifier):
        keyboard.press('v')
        keyboard.release('v')
