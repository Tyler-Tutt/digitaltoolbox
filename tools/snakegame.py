import tkinter as tk
from tkinter import ttk
from .toolbase import ToolBase
import random

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