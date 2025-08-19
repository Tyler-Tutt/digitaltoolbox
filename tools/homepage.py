import tkinter as tk
from tkinter import ttk

# --- Relative Imports ---
# Import the base class that this tool inherits from.
from .toolbase import ToolBase
# Import all the other tool classes that you want to navigate to.
from .testzonetool import TestZoneTool
from .calculator import CalculatorTool
from .clock import ClockTool
from .buttoncommand import ButtonCommand

class Homepage(ToolBase):
    def __init__(self, master, app_controller):
        super().__init__(master, app_controller, "Homepage")

    def build_ui(self):
        """Builds the UI for the homepage with navigation buttons created in a loop."""
        
        # --- Grid Configuration ---
        self.columnconfigure(0, weight=1)
        
        # --- Welcome Label ---
        welcome_label = ttk.Label(self, text="Welcome to your Digital Toolbox!", font=("Helvetica", 18, "bold"))
        welcome_label.grid(row=0, column=0, pady=(20, 30))

        # --- Button Container ---
        button_frame = ttk.Frame(self, borderwidth=2, relief="solid")
        button_frame.grid(row=1, column=0, pady=10)
        
        # --- Data for Navigation Buttons ---
        # Create a list of tuples. Each tuple contains:
        # 1. The text to display on the button.
        # 2. The class of the tool to open when the button is clicked.
        tool_buttons = [
            ("Calculator", CalculatorTool),
            ("Clock", ClockTool),
            ("Button Command", ButtonCommand),
            ("Test Zone", TestZoneTool)
        ]

        # --- Create Buttons in a Loop ---
        # Loop through the data structure to create each button.
        # This avoids repeating the button creation code.
        for button_text, tool_class in tool_buttons:
            # The 'command' uses a lambda function. The 'tool=tool_class' is a special
            # technique to ensure that each button gets the correct tool_class
            # from this specific loop iteration.
            button = ttk.Button(
                button_frame,
                text=button_text,
                command=lambda tool=tool_class: self.app_controller.show_tool(tool)
            )
            # Pack each button into the button_frame.
            button.pack(pady=5, ipadx=35, ipady=5, fill='both')