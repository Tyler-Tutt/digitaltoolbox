import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Sidebar & Main Content Layout")
root.geometry("400x300")

# Configure the grid's responsiveness
root.rowconfigure(0, weight=1) # Make row 0 expandable
root.columnconfigure(0, weight=1) # Sidebar column
root.columnconfigure(1, weight=3) # Main content column (3x the sidebar)

# --- Widgets ---
# Use Frames as containers for different sections
sidebar = ttk.Frame(root, relief="solid", borderwidth=2)
main_content = ttk.Frame(root, relief="solid", borderwidth=2)

sidebar.grid(row=0, column=0, sticky="nsew") # Fill the cell completely
main_content.grid(row=0, column=1, sticky="nsew") # Fill the cell completely

# Add content inside the frames
ttk.Label(sidebar, text="Sidebar").pack(padx=10, pady=10)
ttk.Button(sidebar, text="Button 1").pack(padx=10, fill="x")
ttk.Button(sidebar, text="Button 2").pack(padx=10, fill="x")

ttk.Label(main_content, text="Main Content Area").pack(padx=10, pady=10)
ttk.Label(main_content, text="This area grows much faster!").pack(padx=10, pady=10)


root.mainloop()