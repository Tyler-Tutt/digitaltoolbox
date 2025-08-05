import tkinter as tk
from tkinter import ttk
from .toolbase import ToolBase

class DiffChecker(ToolBase):
    def __init__(self, master, app_controller):
        super().__init__(master, app_controller, "Diff Checker")

    def build_ui(self):
        label = ttk.Label(self, text=f"{self.tool_name} - TODO")
        label.pack(padx=20, pady=20)