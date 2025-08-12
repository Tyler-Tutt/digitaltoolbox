import tkinter as tk
from tkinter import ttk

class ToolBase(tk.Frame):
    """Base class for all tools to inherit from."""
    # master = DigitalToolBoxApp.main_content_frame, app_controller = DigitalToolBoxApp
    def __init__(self, master, app_controller, tool_name, default_prefs=None):
        super().__init__(master)
        self.app_controller = app_controller
        self.tool_name = tool_name
        self.default_prefs = default_prefs if default_prefs is not None else {}
        
        # --- FIX IS HERE ---
        # Call the new method designed to get the entire dictionary for a tool.
        self.prefs = self.app_controller.user_prefs.get_tool_preferences(self.tool_name, self.default_prefs)
        self.build_ui()

    def build_ui(self):
        """Placeholder for UI building in subclasses."""
        label = ttk.Label(self, text=f"{self.tool_name} - UI to be built")
        label.pack(padx=20, pady=20)

    def save_pref(self, key, value):
        """Convenience method to save a preference for this tool."""
        self.app_controller.user_prefs.set_preference(self.tool_name, key, value)
        self.prefs[key] = value # Update local copy

    def get_pref(self, key, default=None):
        """Convenience method to get a preference for this tool."""
        # This call is correct because 'key' will be a string.
        return self.app_controller.user_prefs.get_preference(self.tool_name, key, default)

    def on_show(self):
        """Called when the tool is shown. Override in subclasses if needed."""
        # Refresh preferences when shown, in case they were changed by another instance
        # or by direct file editing (less common for this app type)
        # --- FIX IS HERE ---
        # Also update this line to use the new method
        self.prefs = self.app_controller.user_prefs.get_tool_preferences(self.tool_name, self.default_prefs)

    def on_hide(self):
        """Called when the tool is hidden. Override in subclasses if needed."""
        pass
