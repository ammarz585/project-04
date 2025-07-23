import tkinter as tk
import globals as g

def open_results_window(parent):
    frame = tk.Frame(parent, bg=g.current_theme['bg'])  # Use theme bg color
    tk.Label(frame, text="Scheduling Results Page", font=("Arial", 16), bg=g.current_theme['bg']).pack(pady=50)
    
    # ... rest of results UI

    frame.pack(fill="both", expand=True)
    return frame
