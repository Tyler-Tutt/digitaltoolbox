import tkinter as tk
from tkinter import ttk, messagebox
from .toolbase import ToolBase

class ButtonCommand(ToolBase):
    def __init__(self, master, app_controller):
        default_prefs = {"last_entry": "Hello, Grid!"}
        super().__init__(master, app_controller, "Button Command", default_prefs)

    def build_ui(self):
        # --- Configure the main frame's grid ---
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # --- Create and configure a style for the border ---
        # 1. Create a Style object
        style = ttk.Style()
        # 2. Configure this style's ('style') style.
        style.configure('frame.TFrame', borderwidth=2, relief='solid', background="red")
        style.configure('button2.TButton', background="green")

        # Create a container frame inside the main tool frame
        # Apply the new style using the 'style' option.
        container = ttk.Frame(self, padding="3", style='frame.TFrame')
        container.grid(column=0, row=0, sticky="nsew", padx=10, pady=10)

        # Configure the container's grid
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=3)
        container.rowconfigure(1, weight=1)

        # --- Place Widgets using .grid() ---
        self.my_label = ttk.Label(container, relief='raised', text="Welcome to Button Command", padding=(5,10,25), background="blue")
        self.my_label.grid(column=0, row=0, padx=15, pady=0, sticky="n,s")

        self.my_button = ttk.Button(container, text="Click Me!", command=self.on_button_click)
        self.my_button.grid(column=0, row=1, padx=5, pady=10)
        
        self.my_button2 = ttk.Button(container, text="Click Me!2", style='button2.TButton', command=self.on_button_click)
        self.my_button2.grid(column=1, row=1, padx=5, pady=10)

    def on_button_click(self):
        entered_text = "Hello World"
        messagebox.showinfo("Button Clicked", f"Hello from the Test Zone! You wrote:\n'{entered_text}'")