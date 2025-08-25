import tkinter as tk
from tkinter import ttk
from .toolbase import ToolBase

class CharacterSheet(ToolBase):
    """TTRPG Character Sheet Module"""
    def __init__(self, master, app_controller):
        super().__init__(master, app_controller, "Character Sheet")

    def build_ui(self):
        # --- Main Layout Configuration ---
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # --- Style Configuration ---
        # Using more subtle colors for better readability
        style = ttk.Style()
        style.configure('Dark.TFrame', background="#AD1919") # Main container
        style.configure('Stats.TFrame', background="#580DAD") # Left side
        style.configure('Right.TFrame', background="#379611") # Right side

        # --- Main Container Frame ---
        container = ttk.Frame(self, style="Dark.TFrame", padding=10)
        container.grid(column=0, row=0, sticky="nsew")

        container.columnconfigure(0, weight=1) # Left side column
        container.columnconfigure(1, weight=3) # Right side column (takes up more space)
        container.rowconfigure(0, weight=1)

        # --- Left Side: Stats Container ---
        statscontainer = ttk.Frame(container, style="Stats.TFrame", padding=10)
        statscontainer.grid(column=0, row=0, sticky="nsew", padx=(0, 5))
        
        # Configure the grid inside the stats container to create the table
        statscontainer.columnconfigure(0, weight=1) # Label column
        statscontainer.columnconfigure(1, weight=1) # Point column
        statscontainer.columnconfigure(2, weight=1) # Modifier column

        # --- Create the Stats Table ---
        # Define the stats in a list for easy management
        character_stats = [
            "Strength", "Dexterity", "Constitution",
            "Intelligence", "Wisdom", "Charisma"
        ]

        # Loop through the stats to create a label and an entry for each
        # 'enumerate' gives us both the index (for the row) and the value
        for i, stat_name in enumerate(character_stats):
            # Create the label for the stat name
            label = ttk.Label(statscontainer, text=f"{stat_name}:")
            label.grid(column=0, row=i, sticky="ew", pady=2, padx=5)

            # Create the number input widget (ttk.Entry)
            entry = ttk.Entry(statscontainer, width=5)
            entry.grid(column=1, row=i, sticky="ew", pady=2, padx=5)

            # Modifier Column
            label = ttk.Label(statscontainer, text="1")
            label.grid(column=2, row=i, sticky="ew", pady=2, padx=5)
        
        # --- Right Side Container ---
        rightsidecontainer = ttk.Frame(container, style="Right.TFrame", padding=10)
        rightsidecontainer.grid(column=1, row=0, sticky="nsew", padx=(5, 0))
        
        # Example content for the right side
        right_label = ttk.Label(rightsidecontainer, text="Inventory / Notes")
        right_label.pack()
