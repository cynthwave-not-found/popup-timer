import keyboard
import subprocess
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

#ref
HOTKEY = "ctrl+alt+t"
TIMER_SCRIPT = "timer.py"

def show_error(message): 
    root = tk.Tk()
    #hide
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showerror("Timer Launcher", message)
    root.destroy()

def launch_timer(): 
    try: 
        script_path = Path(__file__).parent / TIMER_SCRIPT
        if not script_path.exists(): 
            show_error(f"Timer script not found!\nExpected file: {TIMER_SCRIPT}")
            return
        
        print(f"Launching timer with hotkey")
        subprocess.Popen(["pythonw", str(script_path)])

    except Exception as e: 
        show_error(f"Failed to launch timer:\n{str(e)}")

keyboard.add_hotkey(HOTKEY, launch_timer)
print(f"Timer Launcher Started! Press {HOTKEY.upper()} to open timer")
keyboard.wait()