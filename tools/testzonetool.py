import tkinter as tk
from tkinter import ttk, messagebox
from .toolbase import ToolBase


class TestZoneTool(ToolBase):
    # TestZoneTool is a child class of ToolBase which is a child class of tk.frame
    # 
    def __init__(self, master, app_controller):
        default_prefs = {"last_entry": "Hello, Grid!"}
        super().__init__(master, app_controller, "Test Zone", default_prefs)

    def build_ui(self):
        # --- Configure the main frame's grid ---
        # self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)

        # --- Create and configure a style for the border ---
        # 1. Create a Style object
        style = ttk.Style()
        # 2. Configure a new custom style.
        #    'Border.TFrame' is a custom name we invented. It inherits from TFrame.
        #    'borderwidth' is the width in pixels.
        #    'relief' is the visual style. 'solid' is a simple line. Other options: 'sunken', 'raised', 'groove', 'ridge'.
        style.configure('Border.TFrame', borderwidth=9, relief='solid')

        # Create a container frame inside the main tool frame
        # 'containter' is a new frame inside self (TestZoneTool WHICH IS a Subclass of Toolbase WHICH IS a subclass of tk.frame)
        # Therefore the first attribute of container (a WIDGET) must be a the frame it belongs to... aka 'self', aka 'tk.frame' from the ultimate Parent Class
        # Apply the new style using the 'style' option.
        container = ttk.Frame(self, padding="5", style='Border.TFrame')
        container.grid(row=0, column=0, sticky="nsew")

        # Configure the container's grid
        # container.columnconfigure(0, weight=1)
        # container.rowconfigure(0, weight=1)

        # --- Place Widgets using .grid() ---
        self.my_label = ttk.Label(container, relief='raised', text="This is the Test Zone!")
        self.my_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.my_entry = ttk.Entry(container, width=40)
        self.my_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.my_entry.insert(0, self.get_pref("last_entry", "default text"))

        self.my_button = ttk.Button(container, text="Click Me!", command=self.on_button_click)
        self.my_button.grid(row=2, column=0, padx=5, pady=10)

    def on_button_click(self):
        entered_text = self.my_entry.get()
        self.my_label.config(text=f"You entered: {entered_text}")
        self.save_pref("last_entry", entered_text)
        messagebox.showinfo("Button Clicked", f"Hello from the Test Zone! You wrote:\n'{entered_text}'")
