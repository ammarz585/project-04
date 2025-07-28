import tkinter as tk
from tkinter import messagebox
import globals as g
from themes import apply_theme_to_widget
import json

def save_tasks_to_json(filepath="D:\\internship\\DSA\\projects\\project4(decision making simulator)\\import_data.json"):
    import os

    # Load existing data if available
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            try:
                existing = json.load(f)
                existing_tasks = existing.get("tasks", [])
                existing_constraints = existing.get("constraints", [])
            except json.JSONDecodeError:
                existing_tasks = []
                existing_constraints = []
    else:
        existing_tasks = []
        existing_constraints = []

    # Avoid duplicates based on task name
    existing_names = {task["name"] for task in existing_tasks}
    new_tasks = [task for task in g.tasks if task["name"] not in existing_names]

    # Merge constraints
    merged_constraints = list({json.dumps(c): c for c in (existing_constraints + getattr(g, "constraints", []))}.values())

    # Combine and save
    all_tasks = existing_tasks + new_tasks
    with open(filepath, 'w') as f:
        json.dump({
            "tasks": all_tasks,
            "constraints": merged_constraints
        }, f, indent=4)

    # Update global tasks and constraints
    g.tasks = all_tasks
    g.constraints = merged_constraints




def show_tasks(content_frame):
    # Clear previous widgets
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Title label
    tk.Label(content_frame, text="Loaded Tasks", font=("Arial", 14, "bold"),
             bg=g.current_theme.get("bg", "white"), fg=g.current_theme.get("fg", "black")).pack(pady=10)

    # Frame to hold listbox and scrollbar side by side
    listbox_frame = tk.Frame(content_frame, height=400)  # 👈 Increased height
    listbox_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Create listbox with increased height using height parameter
    listbox = tk.Listbox(listbox_frame, bg="white", fg="black", selectmode=tk.SINGLE,
                         font=("Arial", 11), height=20)  # 👈 More visible rows
    listbox.pack(side="left", fill="both", expand=True)

    # Create vertical scrollbar and link to listbox
    scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    # Function to populate listbox with tasks
    def refresh_list():
        listbox.delete(0, tk.END)
        for t in g.tasks:
            status = t.get("status", "Pending")
            listbox.insert(tk.END, f"{t['name']} (Cost: {t['cost']}, Value: {t['value']}, Status: {status})")

    refresh_list()

    

   

    
