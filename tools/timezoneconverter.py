import tkinter as tk
from tkinter import ttk
from .toolbase import ToolBase
import datetime

class TimezoneTool(ToolBase):
    def __init__(self, master, app_controller):
        # Note: pytz is recommended for robust timezone handling.
        # pip install pytz
        # For this example, we'll simulate it or use basic datetime features.
        default_prefs = {"default_from_tz": "UTC", "default_to_tz": "America/New_York"}
        super().__init__(master, app_controller, "Timezone Calculator", default_prefs)
        # Try to import pytz, if not available, use a message
        try:
            import pytz
            self.pytz = pytz
            self.available_timezones = self.pytz.common_timezones
        except ImportError:
            self.pytz = None
            self.available_timezones = ["UTC", "America/New_York", "Europe/London", "Asia/Tokyo", "Australia/Sydney"] # Sample list

    def build_ui(self):
        
        if not self.pytz:
            ttk.Label(self, text="pytz library not found. Timezone functionality will be limited.\nInstall with: pip install pytz", foreground="red").pack(pady=10)

        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Input Time and From Timezone
        ttk.Label(main_frame, text="Time (HH:MM):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.time_entry = ttk.Entry(main_frame, width=10)
        self.time_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.time_entry.insert(0, datetime.datetime.now().strftime("%H:%M"))

        ttk.Label(main_frame, text="From Timezone:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.from_tz_combo = ttk.Combobox(main_frame, values=self.available_timezones, width=30)
        self.from_tz_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.from_tz_combo.set(self.get_pref("default_from_tz", self.available_timezones[0] if self.available_timezones else "UTC"))

        # To Timezone
        ttk.Label(main_frame, text="To Timezone:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.to_tz_combo = ttk.Combobox(main_frame, values=self.available_timezones, width=30)
        self.to_tz_combo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.to_tz_combo.set(self.get_pref("default_to_tz", self.available_timezones[1] if len(self.available_timezones) > 1 else "America/New_York"))
        
        # Convert Button
        convert_button = ttk.Button(main_frame, text="Convert", command=self.convert_time)
        convert_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Result Display
        self.result_label = ttk.Label(main_frame, text="Converted Time: ", font=("Helvetica", 14))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        main_frame.grid_columnconfigure(1, weight=1) # Make comboboxes expand

    def convert_time(self):
        input_time_str = self.time_entry.get()
        from_tz_str = self.from_tz_combo.get()
        to_tz_str = self.to_tz_combo.get()

        if not self.pytz:
            self.result_label.config(text="Error: pytz library is required for timezone conversion.")
            return

        try:
            hour, minute = map(int, input_time_str.split(':'))
            # Create a naive datetime object for today with the input time
            now = datetime.datetime.now()
            naive_dt = datetime.datetime(now.year, now.month, now.day, hour, minute)

            from_tz = self.pytz.timezone(from_tz_str)
            to_tz = self.pytz.timezone(to_tz_str)

            # Localize the naive datetime to the source timezone
            localized_dt = from_tz.localize(naive_dt)

            # Convert to the target timezone
            converted_dt = localized_dt.astimezone(to_tz)
            
            self.result_label.config(text=f"Converted Time: {converted_dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
            
            # Save last used timezones as preferences
            self.save_pref("default_from_tz", from_tz_str)
            self.save_pref("default_to_tz", to_tz_str)

        except ValueError:
            self.result_label.config(text="Error: Invalid time format (HH:MM) or timezone.")
        except self.pytz.exceptions.UnknownTimeZoneError: # Corrected exception type
            self.result_label.config(text="Error: Unknown timezone selected.")
        except Exception as e:
            self.result_label.config(text=f"An error occurred: {e}")
