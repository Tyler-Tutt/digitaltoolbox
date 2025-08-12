import tkinter as tk
from tkinter import ttk
from .toolbase import ToolBase
import time

class ClockTool(ToolBase):
    # master = DigitalToolBoxApp.main_content_frame, app_controller = DigitalToolBoxApp
    def __init__(self, master, app_controller):
        default_prefs = {"timezone": "System", "format": "24h", "show_date": True}
        super().__init__(master, app_controller, "Clock", default_prefs)

    def build_ui(self):
        
        self.time_label = ttk.Label(self, text="", font=("Helvetica", 48))
        self.time_label.pack(pady=20, padx=20)

        self.date_label = ttk.Label(self, text="", font=("Helvetica", 18))
        self.date_label.pack(pady=10, padx=20)
        
        self.update_clock()

    def update_clock(self):
        # Note: Timezone handling with pytz would be more robust.
        # For simplicity, this uses local time or a basic UTC offset if we were to implement it.
        # For now, it's just system local time.
        
        current_time = time.strftime('%H:%M:%S' if self.get_pref("format", "24h") == "24h" else '%I:%M:%S %p')
        
        # Ensure time_label exists before configuring (it should, as build_ui is called first)
        if hasattr(self, 'time_label') and self.time_label:
            self.time_label.config(text=current_time)

        if self.get_pref("show_date", True):
            current_date = time.strftime('%A, %B %d, %Y')
            # Ensure date_label exists and is mapped before configuring
            if hasattr(self, 'date_label') and self.date_label:
                self.date_label.config(text=current_date)
                if not self.date_label.winfo_ismapped(): # Show if hidden
                     self.date_label.pack(pady=10, padx=20)
        else:
            if hasattr(self, 'date_label') and self.date_label and self.date_label.winfo_ismapped():
                self.date_label.pack_forget() # Hide if not showing date

        self.after(1000, self.update_clock) # Update every second

    def on_show(self):
        super().on_show()
        self.update_clock() # Ensure clock starts/resumes updating and applies prefs
