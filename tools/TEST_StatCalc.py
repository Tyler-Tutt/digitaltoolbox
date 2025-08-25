import tkinter as tk
from tkinter import ttk
from .toolbase import ToolBase

class StatCalculator(ToolBase):
    """A tool to demonstrate real-time UI updates without a button press."""
    def __init__(self, master, app_controller):
        super().__init__(master, app_controller, "Stat Modifier Calculator")

    def build_ui(self):
        # --- Variable Setup ---
        # 1. Create special Tkinter variables to hold the data.
        # These variables can be "observed" for changes.
        self.stat_score = tk.IntVar(value=10)
        self.modifier_text = tk.StringVar(value="+0")

        # 2. "Trace" the stat_score variable.
        # This registers the self.update_modifier function to be called
        # automatically whenever the stat_score variable is written to.
        self.stat_score.trace_add("write", self.update_modifier)

        # --- Widget Setup ---
        # Configure grid layout
        self.columnconfigure((0, 2), weight=1) # Add padding columns
        self.columnconfigure(1, weight=2)      # Main content column

        # Stat Score Label and Entry
        score_label = ttk.Label(self, text="Stat Score:")
        score_label.grid(row=0, column=1, sticky="sw", padx=10, pady=(10, 0))

        # 3. Link the Entry widget to the IntVar using 'textvariable'.
        # Now, when the user types, self.stat_score is updated automatically.
        score_entry = ttk.Entry(self, textvariable=self.stat_score, width=10)
        score_entry.grid(row=1, column=1, sticky="ew", padx=10)

        # Modifier Label
        modifier_title_label = ttk.Label(self, text="Stat Modifier:")
        modifier_title_label.grid(row=2, column=1, sticky="sw", padx=10, pady=(20, 0))

        # 4. Link the result Label to the StringVar.
        # When self.modifier_text is changed in our code, this label updates.
        modifier_result_label = ttk.Label(self, textvariable=self.modifier_text, font=("Helvetica", 24, "bold"))
        modifier_result_label.grid(row=3, column=1, sticky="n", padx=10)

    def update_modifier(self, *args):
        """
        This function is called automatically whenever self.stat_score changes.
        It performs the calculation and updates the result variable.
        """
        try:
            # Get the current value from the IntVar
            score = self.stat_score.get()
            
            # Perform the calculation (e.g., D&D 5e modifier formula)
            modifier = (score - 10) // 2
            
            # Format the result string with a '+' for positive numbers
            if modifier >= 0:
                result = f"+{modifier}"
            else:
                result = str(modifier)
            
            # 5. Update the StringVar, which automatically updates the linked Label.
            self.modifier_text.set(result)

        except tk.TclError:
            # This handles the case where the entry box is empty or invalid
            self.modifier_text.set("...")
