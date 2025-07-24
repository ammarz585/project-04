from globals import current_theme
import tkinter as tk
def user_guide(parent):

    bg = current_theme["bg"]
    fg = current_theme["fg"]

    guide_frame = tk.Frame(parent, bg=bg)
    guide_frame.pack(fill="both", expand=True)

    guide_text = """
    📝 USER GUIDE

    1. Add Tasks:
       - Use the 'Add' button to create a task.
       - Enter the task name, cost, value, and dependencies.

    2. Remove Tasks:
       - Select a task from the list and press 'Remove'.

    3. Load/Save:
       - Use 'Load' to load saved task data from JSON file.
       - Use 'Save' to export current task data to JSON.

    4. Scheduling:
       - Click 'Scheduler' to run optimization based on cost-to-value ratio.

    5. Theme:
       - Use the 'Toggle Theme' button to switch between light/dark mode.

    Shortcuts:
    - Use Ctrl + → or ← to navigate pages quickly.
    """

    text_widget = tk.Text(guide_frame, wrap="word", bg=bg, fg=fg, font=("Segoe UI", 12), bd=0)
    text_widget.insert("1.0", guide_text)
    text_widget.config(state="disabled")  # Read-only
    text_widget.pack(padx=20, pady=20, fill="both", expand=True)

    return guide_frame
