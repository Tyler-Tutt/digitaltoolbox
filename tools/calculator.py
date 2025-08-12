import tkinter as tk
from tkinter import ttk

from .toolbase import ToolBase

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
