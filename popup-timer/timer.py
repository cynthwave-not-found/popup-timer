import tkinter as tk
from tkinter import messagebox
from tkinter import font
import ctypes
from pathlib import Path
import time
from customtkinter import *
from PIL import Image
import keyboard

set_appearance_mode("dark")

class TimerApp: 
    def __init__(self): 
        self.root = CTk()
        self.root.title("Timer")
        self.root.geometry("400x320")
        self.root.resizable(False, False)
        
        #aka total time
        self.time_left = 0.0
        self.start_time = 0.0
        self.is_running = False
        self.pause = False
        self.paused_time = 0.0

        self.create_widgets()
        self.root.bind("<space>",self.on_space)
#load nunito font: disabled for simplicity
#note: the nunito font version is available on the subbranch {fonts}
'''        success = self.load_custom_font("fonts/Nunito-Regular.ttf")
        if success: 
            nunito_font = tk.font.Font(family="Nunito", size=14, weight="bold")
        else: 
            print("Failed to load Nunito font")

    def load_custom_font(self, font_path: str) -> bool: 
        try: 
            FR_PRIVATE = 0x10
            path = Path(font_path).resolve()

            ctypes.windll.gdi32.AddFontResourceExW.restype = ctypes.c_int
            result = ctypes.windll.gdi32.AddFontResourceExW(
                str(path), FR_PRIVATE, 0
            )
            if result == 0:
                print(f"Failed to load font: {font_path}")
                return False
            
            print(f"Sucessfully loaded: {path.name}")
            return True

        except Exception as e: 
            print (f"Error loading font: {e}")
            return False
'''
    def create_widgets(self): 
        title = CTkLabel(self.root, text="Timer", font=("Nunito", 28, "bold"))
        title.pack(pady=10)

        self.display = CTkLabel(self.root, text="00:00:000",font=("Nunito", 48, "bold"))
        self.display.place(relx=0.5, rely=0.35, anchor="center")

#input frames
        input_frame = CTkFrame(master=self.root, fg_color="#A67927", width=300, height=100,border_color="#FFCC70", border_width=2)
        input_frame.place(relx=0.5, rely=0.6, anchor="center")

        CTkLabel(input_frame, text="Minutes:", font=("Nunito", 10, "italic")).grid(row=0,column=0, padx=5)
        self.min_entry = CTkEntry(input_frame, width=50, font=("Nunito", 14))
        self.min_entry.grid(row=0, column=1, padx=5, pady=8)
        self.min_entry.insert(0,"5")

        CTkLabel(input_frame, text="Seconds:", font=("Nunito", 10, "italic")).grid(row=0, column=2, padx=5)
        self.sec_entry = CTkEntry(input_frame, width=50, font=("Nunito", 14))
        self.sec_entry.grid(row=0,column=3, padx=15, pady=8)
        self.sec_entry.insert(0,"0")

        frame2 = CTkFrame(master=self.root, fg_color="#242424", width=300, height=650, border_color="#242424", border_width=2)
        frame2.place(relx=0.5, rely=0.8, anchor="center")

#button frames
        self.start_btn = CTkButton(frame2, text="Start", font=("Nunito", 12),
                                   border_color="#FFCC70", border_width=1, fg_color="transparent", width=20,command=self.start_timer)
        self.start_btn.grid(row=0,column=0,padx=10)
        
        self.pause_btn = CTkButton(frame2, text="Pause", font=("Nunito", 12), 
                                   border_color="#FFCC70", border_width=1, fg_color="transparent", width=20, command=self.toggle_pause, state="disabled")
        self.pause_btn.grid(row=0,column=1,padx=10)

        self.reset_btn = CTkButton(frame2, text="Reset", font=("Nunito", 12), 
                                    border_color="#FFCC70", border_width=1, fg_color="transparent", width=20, command=self.reset_timer)
        self.reset_btn.grid(row=0, column=2, padx=10)
    
    def on_space(self, event=None): 
        self.toggle_pause()

    def toggle_pause(self): 
        if not self.is_running: 
            self.start_timer()
            return
        if self.pause: 
            self.pause = False
            self.pause_btn.configure(text="Pause")
            self.start_time = time.perf_counter() - self.paused_time
            self.update_timer()
        else:
            self.pause = True
            self.pause_btn.configure(text="Resume")
            self.paused_time = time.perf_counter() - self.start_time
    
    def start_timer(self): 
        if self.is_running:
            return
        
        try: 
            minutes = int(self.min_entry.get() or 0)
            seconds = int(self.sec_entry.get() or 0)
            self.time_left = minutes * 60 + seconds

            if self.time_left <= 0: 
                 messagebox.showwarning("Invalid", "Please enter time greater than 0")
                 return
        
            self.is_running = True
            self.pause = False
            self.paused_time = 0.0
            self.start_time = time.perf_counter()
            self.pause_btn.configure(state="normal", text="Pause")
            self.update_timer()
        except ValueError: 
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def update_timer(self):
        if not self.is_running or self.pause: 
            return
        
        elapsed = time.perf_counter() - self.start_time
        remaining = self.time_left - elapsed

        if remaining <= 0:
            self.finish_timer()
            return
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        millis = int((remaining % 1) * 1000)

        self.display.configure(text=f"{minutes:02d}:{seconds:02d}:{millis:03d}")

        self.root.after(10, self.update_timer)

    def reset_timer(self): 
        self.is_running = False
        self.pause = False
        self.time_left = 0.0
        self.display.configure(text="00:00:000")
        self.pause_btn.configure(text="Pause",state="disabled")
        self.min_entry.delete(0, tk.END)
        self.min_entry.insert(0,"5")
        self.sec_entry.delete(0,tk.END)
        self.sec_entry.insert(0,"0")

    def finish_timer(self): 
        self.is_running = False
        self.pause = False
        self.display.configure(text="00:00:000")

        try:
            self.root.bell()
            self.root.bell()
            messagebox.showinfo("Timer","Time's up!")
        except:
            pass

    def run(self): 
        self.root.mainloop()


if __name__ == "__main__": 
    app = TimerApp()
    app.run()
    
