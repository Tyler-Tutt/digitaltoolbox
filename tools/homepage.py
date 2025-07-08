import tkinter as tk
from tkinter import ttk
from .toolbase import ToolBase

class Homepage(ToolBase):
    def __init__(self, master, app_controller):
        super().__init__(master, app_controller, "Homepage")

    def build_ui(self):
        label = ttk.Label(self, text=f"{self.tool_name} - UI to be built")
        label.pack(padx=20, pady=20)