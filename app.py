import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import time
import datetime # Ensure this is imported
import random

# --- Configuration ---
USER_DATA_DIR = "user_data"
DEFAULT_USER = "default_user"

# --- User and Preference Management ---
class UserPreferences:
    def __init__(self, username):
        self.username = username
        self.user_dir = os.path.join(USER_DATA_DIR, self.username)
        os.makedirs(self.user_dir, exist_ok=True)
        self.preferences = {}
        self.load_all_preferences()

    def _get_pref_file_path(self, tool_name):
        """Helper to get the path to a tool's preference file."""
        return os.path.join(self.user_dir, f"{tool_name}_prefs.json")

    def load_preferences(self, tool_name, default_prefs=None):
        """Loads preferences for a specific tool."""
        if default_prefs is None:
            default_prefs = {}
        file_path = self._get_pref_file_path(tool_name)
        try:
            with open(file_path, 'r') as f:
                prefs = json.load(f)
                self.preferences[tool_name] = prefs
                return prefs
        except (FileNotFoundError, json.JSONDecodeError):
            self.preferences[tool_name] = default_prefs
            self.save_preferences(tool_name, default_prefs) # Save defaults if not found
            return default_prefs

    def save_preferences(self, tool_name, prefs_data):
        """Saves preferences for a specific tool."""
        file_path = self._get_pref_file_path(tool_name)
        self.preferences[tool_name] = prefs_data # Update in-memory cache
        try:
            with open(file_path, 'w') as f:
                json.dump(prefs_data, f, indent=4)
        except IOError as e:
            print(f"Error saving preferences for {tool_name}: {e}")


    def get_preference(self, tool_name, key, default=None):
        """Gets a specific preference value for a tool."""
        return self.preferences.get(tool_name, {}).get(key, default)

    def set_preference(self, tool_name, key, value):
        """Sets a specific preference value for a tool and saves it."""
        if tool_name not in self.preferences:
            self.preferences[tool_name] = {}
        self.preferences[tool_name][key] = value
        self.save_preferences(tool_name, self.preferences[tool_name])

    def load_all_preferences(self):
        """Loads all preference files found in the user's directory."""
        # This is a basic implementation. For a real app, you might list known tools
        # or have a manifest file.
        # For now, we'll rely on tools registering their default prefs upon initialization.
        pass

# --- Base Tool Class ---
class ToolBase(tk.Frame):
    """Base class for all tools to inherit from."""
    # master = DigitalToolBoxApp.main_content_frame, app_controller = DigitalToolBoxApp
    def __init__(self, master, app_controller, tool_name, default_prefs=None):
        super().__init__(master)
        self.app_controller = app_controller
        self.tool_name = tool_name
        self.default_prefs = default_prefs if default_prefs is not None else {}
        self.prefs = self.app_controller.user_prefs.load_preferences(self.tool_name, self.default_prefs)
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
        return self.app_controller.user_prefs.get_preference(self.tool_name, key, default)

    def on_show(self):
        """Called when the tool is shown. Override in subclasses if needed."""
        # Refresh preferences when shown, in case they were changed by another instance
        # or by direct file editing (less common for this app type)
        self.prefs = self.app_controller.user_prefs.load_preferences(self.tool_name, self.default_prefs)
        # print(f"{self.tool_name} shown. Current prefs: {self.prefs}")

    def on_hide(self):
        """Called when the tool is hidden. Override in subclasses if needed."""
        # print(f"{self.tool_name} hidden.")
        pass

# --- Tool Implementations ---
class CalculatorTool(ToolBase):
    def __init__(self, master, app_controller):
        default_prefs = {"last_result": 0, "window_size": "300x400"}
        super().__init__(master, app_controller, "Calculator", default_prefs)

    def build_ui(self):
        # super().destroy() # REMOVED as per previous fix
        
        self.expression = ""
        self.equation = tk.StringVar()

        # Entry field for display
        display_frame = ttk.Frame(self)
        display_frame.pack(pady=10, padx=10, fill="x")
        
        self.display_entry = ttk.Entry(display_frame, textvariable=self.equation, font=('arial', 20, 'bold'), state='readonly', justify='right')
        self.display_entry.pack(fill="x", expand=True)

        # Button grid
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(expand=True, fill="both", padx=5, pady=5)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
            ('=', 5, 0, 1, 4) # Spanning 4 columns
        ]

        for (text, row, col, *span) in buttons:
            action = lambda x=text: self.on_button_click(x)
            button = ttk.Button(buttons_frame, text=text, command=action, style="Calc.TButton")
            if span:
                button.grid(row=row, column=col, columnspan=span[1], sticky="nsew", padx=2, pady=2)
            else:
                button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        # Configure row/column weights for resizing
        for i in range(6): # 6 rows including display
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4): # 4 columns
            buttons_frame.grid_columnconfigure(i, weight=1)
            
        # Styling
        style = ttk.Style()
        style.configure("Calc.TButton", font=('arial', 14), padding=10)

        # Load last result if any
        last_res = self.get_pref("last_result", "")
        if last_res:
            self.equation.set(str(last_res))


    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.equation.set("")
        elif char == '=':
            try:
                # Avoid using eval directly in a real-world app due to security risks.
                # For this controlled environment, it's simpler.
                # A safer approach would be to parse and calculate the expression manually.
                result = str(eval(self.expression))
                self.equation.set(result)
                self.save_pref("last_result", result)
                self.expression = result # So user can continue calculation with the result
            except Exception as e:
                self.equation.set("Error")
                self.expression = ""
        else:
            self.expression += str(char)
            self.equation.set(self.expression)

    def on_show(self):
        super().on_show()
        # Example: Apply window size preference if stored
        # size = self.get_pref("window_size", "300x400")
        # self.app_controller.root.geometry(size) # This might be better handled at app level

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
        # super().destroy() # REMOVED as per previous fix
        
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

class SnakeGameTool(ToolBase):
    GAME_SPEED = 200
    GRID_SIZE = 20
    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 400
    SNAKE_COLOR = "green"
    FOOD_COLOR = "red"
    BG_COLOR = "black"

    def __init__(self, master, app_controller):
        default_prefs = {"high_score": 0, "snake_color": "green"}
        super().__init__(master, app_controller, "Snake Game", default_prefs)
        self.snake = []
        self.food = None
        self.direction = "Right"
        self.score = 0
        self.game_over_flag = False
        # self.canvas = None # Initialized in build_ui

    def build_ui(self):
        # super().destroy() # REMOVED as per previous fix

        self.score_label = ttk.Label(self, text=f"Score: 0  High Score: {self.get_pref('high_score', 0)}", font=("Arial", 14))
        self.score_label.pack(pady=5)

        self.canvas = tk.Canvas(self, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, bg=self.BG_COLOR, bd=0, highlightthickness=0)
        self.canvas.pack(pady=10)
        
        self.start_button = ttk.Button(self, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=5)

        # Bind arrow keys
        # Important: Binding needs to be on a widget that can take focus, or globally on the root.
        # For simplicity, we'll bind to the canvas and ensure it can get focus.
        self.canvas.focus_set() # Make canvas focusable
        self.canvas.bind("<KeyPress-Left>", lambda e: self.change_direction("Left"))
        self.canvas.bind("<KeyPress-Right>", lambda e: self.change_direction("Right"))
        self.canvas.bind("<KeyPress-Up>", lambda e: self.change_direction("Up"))
        self.canvas.bind("<KeyPress-Down>", lambda e: self.change_direction("Down"))
        
        # Instructions
        self.instructions_label = ttk.Label(self, text="Use arrow keys to control the snake. Press 'Start Game'.")
        self.instructions_label.pack(pady=5)

    def start_game(self):
        self.game_over_flag = False
        self.score = 0
        self.direction = "Right"
        self.snake = [(100, 100), (80, 100), (60, 100)] # Initial snake segments
        self.update_score_label()
        self.create_food()
        if self.canvas: # Ensure canvas exists
            self.canvas.delete("game_over") # Clear game over message
        self.start_button.config(state="disabled")
        self.instructions_label.config(text="Game in progress...")
        if self.canvas: # Ensure canvas exists
            self.canvas.focus_set() # Ensure canvas has focus for key bindings
        self.game_loop()

    def game_loop(self):
        if not self.winfo_exists() or self.game_over_flag : # Stop if widget is destroyed or game over
            if self.game_over_flag and self.winfo_exists(): # only show game over if widget still exists
                 self.show_game_over()
            if self.winfo_exists(): # only configure button if widget still exists
                self.start_button.config(state="normal")
                self.instructions_label.config(text="Game Over! Press 'Start Game' to play again.")
            return

        head_x, head_y = self.snake[0]
        if self.direction == "Left":
            new_head = (head_x - self.GRID_SIZE, head_y)
        elif self.direction == "Right":
            new_head = (head_x + self.GRID_SIZE, head_y)
        elif self.direction == "Up":
            new_head = (head_x, head_y - self.GRID_SIZE)
        elif self.direction == "Down":
            new_head = (head_x, head_y + self.GRID_SIZE)
        else: # Should not happen
            new_head = (head_x, head_y)


        self.snake.insert(0, new_head)

        # Check for collision with food
        if new_head == self.food:
            self.score += 1
            self.update_score_label()
            self.create_food()
        else:
            self.snake.pop() # Remove tail

        # Check for collisions (wall or self)
        if (new_head[0] < 0 or new_head[0] >= self.CANVAS_WIDTH or
            new_head[1] < 0 or new_head[1] >= self.CANVAS_HEIGHT or
            new_head in self.snake[1:]):
            self.game_over_flag = True
            if self.score > self.get_pref('high_score', 0):
                self.save_pref('high_score', self.score)
            self.update_score_label() # Update high score display immediately

        self.draw_elements()
        if self.winfo_exists(): # Check if widget exists before scheduling next call
            self.after(self.GAME_SPEED, self.game_loop)


    def create_food(self):
        while True:
            x = random.randrange(0, self.CANVAS_WIDTH // self.GRID_SIZE) * self.GRID_SIZE
            y = random.randrange(0, self.CANVAS_HEIGHT // self.GRID_SIZE) * self.GRID_SIZE
            self.food = (x, y)
            if self.food not in self.snake: # Ensure food doesn't spawn on snake
                break

    def draw_elements(self):
        if self.canvas and self.canvas.winfo_exists(): # Ensure canvas exists
            self.canvas.delete(tk.ALL) # Clear canvas
            # Draw snake
            snake_color_pref = self.get_pref("snake_color", self.SNAKE_COLOR)
            for x, y in self.snake:
                self.canvas.create_rectangle(x, y, x + self.GRID_SIZE, y + self.GRID_SIZE, fill=snake_color_pref, outline=self.BG_COLOR)
            # Draw food
            if self.food:
                self.canvas.create_oval(self.food[0], self.food[1], self.food[0] + self.GRID_SIZE, self.food[1] + self.GRID_SIZE, fill=self.FOOD_COLOR, outline=self.BG_COLOR)

    def change_direction(self, new_direction):
        # Prevent immediate reversal
        if new_direction == "Left" and self.direction != "Right":
            self.direction = new_direction
        elif new_direction == "Right" and self.direction != "Left":
            self.direction = new_direction
        elif new_direction == "Up" and self.direction != "Down":
            self.direction = new_direction
        elif new_direction == "Down" and self.direction != "Up":
            self.direction = new_direction
        # print(f"Direction changed to: {self.direction}") # For debugging

    def update_score_label(self):
        if self.score_label and self.score_label.winfo_exists():
            self.score_label.config(text=f"Score: {self.score}  High Score: {self.get_pref('high_score', 0)}")

    def show_game_over(self):
        if self.canvas and self.canvas.winfo_exists(): # Ensure canvas exists
            self.canvas.create_text(self.CANVAS_WIDTH / 2, self.CANVAS_HEIGHT / 2,
                                    text="GAME OVER", fill="white", font=("Arial", 30, "bold"), tags="game_over")

    def on_hide(self):
        super().on_hide()
        self.game_over_flag = True # Stop game loop if tool is switched

    def on_show(self):
        super().on_show()
        # Reset game state or just update labels if needed
        self.update_score_label()
        if self.canvas and self.canvas.winfo_exists(): # Ensure canvas exists
            self.canvas.focus_set() # Ensure focus when shown

    # +++ TOOL IMPLEMENTATION with a BORDER +++

class TestZoneTool(ToolBase):
    def __init__(self, master, app_controller):
        default_prefs = {"last_entry": "Hello, Grid!"}
        super().__init__(master, app_controller, "Test Zone", default_prefs)

    def build_ui(self):
        # --- Configure the main frame's grid ---
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # --- Create and configure a style for the border ---
        # 1. Create a Style object
        style = ttk.Style()
        # 2. Configure a new custom style.
        #    'Border.TFrame' is a custom name we invented. It inherits from TFrame.
        #    'borderwidth' is the width in pixels.
        #    'relief' is the visual style. 'solid' is a simple line. Other options:
        #    'sunken', 'raised', 'groove', 'ridge'.
        style.configure('Border.TFrame', borderwidth=9, relief='solid')

        # Create a container frame inside the main tool frame
        # Apply the new style using the 'style' option.
        container = ttk.Frame(self, padding="5", style='Border.TFrame')
        container.grid(row=0, column=0, sticky="nsew")

        # Configure the container's grid
        container.columnconfigure(0, weight=1)

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
        style.configure('Border.TFrame', borderwidth=1, relief='solid', background="red")

        # Create a container frame inside the main tool frame
        # Apply the new style using the 'style' option.
        container = ttk.Frame(self, padding="5", style='Border.TFrame')
        container.grid(column=0, row=0, sticky="nsew")

        # Configure the container's grid
        container.columnconfigure(0, weight=1)

        # --- Place Widgets using .grid() ---
        self.my_label = ttk.Label(container, relief='raised', text="This is the Test Zone!")
        self.my_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")

        self.my_button = ttk.Button(container, text="Click Me!", command=self.on_button_click)
        self.my_button.grid(column=0, row=1, padx=5, pady=10)
        
        button2Style = ttk.Style()
        button2Style.configure('button2Style.TButton', background="green")
        self.my_button2 = ttk.Button(container, text="Click Me!2", style='button2Style.TButton', command=self.on_button_click)
        self.my_button2.grid(column=0, row=2, padx=5, pady=10)

    def on_button_click(self):
        entered_text = "Hello World"
        messagebox.showinfo("Button Clicked", f"Hello from the Test Zone! You wrote:\n'{entered_text}'")

# --- Main Application ---
class DigitalToolboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Toolbox")
        # The size of a frame is determined by the size and layout of any widgets within it. 
        # In turn, this is controlled by the geometry manager that manages the contents of the frame itself.
        #self.root.geometry("500x500") # Initial size
        # No Initial Size = Frame will adapt to widgets within it

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
        file_menu.add_command(label="Exit", command=root.quit)

        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Calculator", command=lambda: self.show_tool(CalculatorTool))
        tools_menu.add_command(label="Clock", command=lambda: self.show_tool(ClockTool))
        tools_menu.add_command(label="Timezone Calculator", command=lambda: self.show_tool(TimezoneTool))
        tools_menu.add_command(label="Snake Game", command=lambda: self.show_tool(SnakeGameTool))
        tools_menu.add_command(label="Test Zone", command=lambda: self.show_tool(TestZoneTool))
        tools_menu.add_command(label="Button Command", command=lambda: self.show_tool(ButtonCommand))
        
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
        # padding & borderwidth on the *frame* control the 'padding' & 'border' (HTML)
        self.main_content_frame = ttk.Frame(root, borderwidth=10, relief="groove", padding="15")
        # padx & pady on the *Geometry Manager* control the 'Margin'
        self.main_content_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Show a default tool or welcome message
        self.show_tool(ButtonCommand) # Show's a default Tool on startup

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
            
            self.current_user = new_user.strip()
            self.user_prefs = UserPreferences(self.current_user) # Load/create new user's prefs
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
    # Create user data directory if it doesn't exist
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)

    root = tk.Tk()
    app = DigitalToolboxApp(root)
    root.mainloop()