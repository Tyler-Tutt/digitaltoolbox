import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import sys # Access system-specific parameters
import database # database.py file
from database import UserPreferences

# TODO Current ToDo: Just figured out how to launch a python app in windows even when developing on WSL
# TODO Do a good Obsidian Guide so as to be able to recreate that workflow / research easier/efficient of the same workflow

# --- tool imports from package ---
from tools.buttoncommand import ButtonCommand
from tools.calculator import CalculatorTool
from tools.clock import ClockTool
from tools.homepage import Homepage
from tools.snakegame import SnakeGameTool
from tools.testzonetool import TestZoneTool
from tools.timezoneconverter import TimezoneTool
from tools.diffchecker import DiffChecker
from tools.toolbase import ToolBase

# --- Configuration ---
USER_DATA_DIR = "user_data"
DEFAULT_USER = "default_user"
DEFAULT_TOOL = None

# --- Main Application ---
class DigitalToolboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Toolbox")

        # The size of a frame is determined by the size and layout of any widgets within it. 
        # In turn, this is controlled by the geometry manager that manages the contents of the frame itself.
        #self.root.geometry("500x500") # Initial size
        # No Initial Size = Frame will adapt to widgets within it
        # 'zoomed' = maximized window
        self.root.attributes('-fullscreen', True)
        # root.state('zoomed')

        # This line tells Tkinter to call our custom quit_app function
        # whenever the user clicks the 'X' button on the window.
        # This ensures the database connection is always closed cleanly.
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

        # --- Set up the hotkey binding ---
        # The .bind() method links an event pattern to a callback function.
        # This is bound to the root window, so it works globally.
        self.root.bind('<Control-q>', self.quit_app)
        self.root.bind('<Control-r>', self.restart_app)
        self.root.bind('<Control-h>', self.return_to_homepage)

        self.current_user = DEFAULT_USER
        self.user_prefs = UserPreferences(self.current_user)

        self.current_tool_frame = None

        # --- Menu ---
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Switch User", command=self.switch_user)
        file_menu.add_separator()
        file_menu.add_command(label="Restart (Ctrl+R)", command=self.restart_app)
        file_menu.add_separator()
        file_menu.add_command(label="Exit (Ctrl+Q)", command=self.quit_app)

        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Homepage", command=lambda: self.show_tool(Homepage))
        tools_menu.add_command(label="Calculator", command=lambda: self.show_tool(CalculatorTool))
        tools_menu.add_command(label="Clock", command=lambda: self.show_tool(ClockTool))
        tools_menu.add_command(label="Timezone Calculator", command=lambda: self.show_tool(TimezoneTool))
        tools_menu.add_command(label="Snake Game", command=lambda: self.show_tool(SnakeGameTool))
        tools_menu.add_command(label="Test Zone", command=lambda: self.show_tool(TestZoneTool))
        tools_menu.add_command(label="Button Command", command=lambda: self.show_tool(ButtonCommand))
        tools_menu.add_command(label="Diff Checker", command=lambda: self.show_tool(DiffChecker))
        
        # Settings Menu (Example for Clock)
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        clock_settings_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="Clock Settings", menu=clock_settings_menu)
        
        self.clock_format_var = tk.StringVar(value=self.user_prefs.get_preference("Clock", "format", "24h"))
        clock_settings_menu.add_radiobutton(label="24-hour Format", variable=self.clock_format_var, value="24h", command=self.update_clock_setting)
        clock_settings_menu.add_radiobutton(label="12-hour Format", variable=self.clock_format_var, value="12h", command=self.update_clock_setting)
        
        self.clock_show_date_var = tk.BooleanVar(value=self.user_prefs.get_preference("Clock", "show_date", True))
        clock_settings_menu.add_checkbutton(label="Show Date", variable=self.clock_show_date_var, command=self.update_clock_setting)

        # --- Status Bar ---
        self.status_bar = ttk.Label(root, text=f"Current User: {self.current_user}", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # --- Main content area ---
        # padding & borderwidth on the *frame widget* control the 'padding' & 'border' (Box Model)
        self.main_content_frame = ttk.Frame(root, borderwidth=3, relief="groove")
        # padx & pady on the *Geometry Manager for the widget* control the 'Margin'
        self.main_content_frame.pack(fill="both", expand=True)

        # Show a default tool or welcome message
        self.show_tool(DEFAULT_TOOL) # Show's a default Tool on startup

    # The 'event=None' allows this method to be called by the keybinding 
    # (which sends an event object) and the menu (which doesn't).
    def quit_app(self, event=None):
        """Callback function to quit the application."""
        self.root.quit()

    def restart_app(self, event=None):
        """Destroys the current window and restarts the python script."""
        # First, cleanly destroy the current Tkinter window
        self.root.destroy()
        # Then, use os.execl to replace the current process with a new one.
        # sys.executable is the path to the current Python interpreter.
        # sys.argv is the list of original command line arguments.
        os.execl(sys.executable, sys.executable, *sys.argv)

    def return_to_homepage(self, event=None):
        self.show_tool(Homepage)

    def update_clock_setting(self):
        self.user_prefs.set_preference("Clock", "format", self.clock_format_var.get())
        self.user_prefs.set_preference("Clock", "show_date", self.clock_show_date_var.get())
        # If clock is currently shown, it should update itself via its on_show or internal logic
        if isinstance(self.current_tool_frame, ClockTool):
            # self.current_tool_frame.on_show() # Trigger a refresh of the clock display
            # The clock's own update_clock loop will pick up preference changes.
            # If on_show is called, it re-calls update_clock which is fine.
            # Or, we could have a more specific update_display method in ClockTool.
            # For now, the periodic update_clock will handle it.
            # To make changes immediate, we can call update_clock directly if it's safe
            if hasattr(self.current_tool_frame, 'update_clock'):
                 self.current_tool_frame.update_clock()

    def switch_user(self):
        new_user = simpledialog.askstring("Switch User", "Enter username:", parent=self.root)
        if new_user and new_user.strip():
            if self.current_tool_frame and hasattr(self.current_tool_frame, 'on_hide'):
                self.current_tool_frame.on_hide()
            
            self.user_prefs.close_connection()
            self.current_user = new_user.strip()
            self.user_prefs = UserPreferences(self.current_user)
            
            self.status_bar.config(text=f"Current User: {self.current_user}")
            messagebox.showinfo("User Switched", f"Switched to user: {self.current_user}", parent=self.root)
            
            # Refresh current tool with new user's preferences or show default
            if self.current_tool_frame:
                tool_class = type(self.current_tool_frame)
                self.show_tool(tool_class) # This re-instantiates the tool
            else:
                self.show_tool(ClockTool) # Or a default welcome screen

            # Update settings menu variables to reflect new user's preferences
            self.clock_format_var.set(self.user_prefs.get_preference("Clock", "format", "24h"))
            self.clock_show_date_var.set(self.user_prefs.get_preference("Clock", "show_date", True))

        elif new_user is not None: # User entered empty string
            messagebox.showwarning("Invalid User", "Username cannot be empty.", parent=self.root)

    def show_tool(self, tool_class):
        if self.current_tool_frame:
            if hasattr(self.current_tool_frame, 'on_hide'):
                self.current_tool_frame.on_hide()
            self.current_tool_frame.destroy()
            self.current_tool_frame = None # Ensure it's cleared

        # Instantiate the new tool, passing the app_controller (self)
        self.current_tool_frame = tool_class(self.main_content_frame, self)
        self.current_tool_frame.pack(fill="both", expand=True)
        if hasattr(self.current_tool_frame, 'on_show'):
            self.current_tool_frame.on_show()
        
        # Update window title or other app-level things based on tool
        self.root.title(f"Digital Toolbox - {self.current_tool_frame.tool_name}")

# --- Initiate tk loop ---
if __name__ == "__main__":
    database.init_db()

    DEFAULT_TOOL = Homepage

    root = tk.Tk()
    app = DigitalToolboxApp(root)
    root.mainloop()