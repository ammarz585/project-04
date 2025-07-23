import tkinter as tk
import globals as g

def open_graphs_window(parent):
    frame = tk.Frame(parent, bg=g.current_theme['bg'])  # Use background from current theme
    tk.Label(frame, text="Graphs Page", font=("Arial", 16), bg=g.current_theme['bg']).pack(pady=50)
    
    # ... rest of graphs UI

    frame.pack(fill="both", expand=True)
    return frame
