import tkinter as tk
from tkinter import messagebox
import json
import globals as g

entries = []

def load_data_from_json(filepath="D:\\internship\\DSA\\projects\\project4(decision making simulator)\\import_data.json"):
    with open(filepath, 'r') as file:
        data = json.load(file)
    tasks = data.get('tasks', [])
    constraints = data.get('constraints', [])
    return tasks, constraints

def save_data_to_json(filepath="D:\\internship\\DSA\\projects\\project4(decision making simulator)\\import_data.json"):
    with open(filepath, 'w') as file:
        json.dump({"tasks": g.tasks, "constraints": g.constraints}, file, indent=4)

def create_entry_row(frame, task_data=None, row=None):
    name_var = tk.StringVar(value=task_data["name"] if task_data else "")
    value_var = tk.StringVar(value=str(task_data["value"]) if task_data else "")
    cost_var = tk.StringVar(value=str(task_data["cost"]) if task_data else "")
    category_var = tk.StringVar(value=task_data["category"] if task_data else "")
    status_var = tk.StringVar(value=task_data.get("status", "Pending") if task_data else "Pending")

    e1 = tk.Entry(frame, textvariable=name_var)
    e1.grid(row=row, column=0, padx=5, pady=2, sticky="ew")
    e2 = tk.Entry(frame, textvariable=value_var)
    e2.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
    e3 = tk.Entry(frame, textvariable=cost_var)
    e3.grid(row=row, column=2, padx=5, pady=2, sticky="ew")
    e4 = tk.Entry(frame, textvariable=category_var)
    e4.grid(row=row, column=3, padx=5, pady=2, sticky="ew")
    e5 = tk.Entry(frame, textvariable=status_var, state="readonly")  # Status is read-only
    e5.grid(row=row, column=4, padx=5, pady=2, sticky="ew")

    entries.append({
        "name": name_var,
        "value": value_var,
        "cost": cost_var,
        "category": category_var,
        "status": status_var
    })

def save_tasks():
    new_tasks = []
    for row in entries:
        name = row["name"].get().strip()
        if not name:
            continue
        try:
            value = int(row["value"].get())
        except ValueError:
            value = 0
        try:
            cost = int(row["cost"].get())
        except ValueError:
            cost = 0
        category = row["category"].get().strip()

        # Update status based on executed_tasks and removed_tasks sets
        if name in g.executed_tasks:
            status = "Executed"
        elif name in g.removed_tasks:
            status = "Removed"
        else:
            status = "Pending"

        new_tasks.append({
            "name": name,
            "value": value,
            "cost": cost,
            "category": category,
            "status": status
        })

    g.tasks = new_tasks
    save_data_to_json()
    messagebox.showinfo("Success", "Tasks saved to global list and JSON file.")

def load_tasks_to_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    entries.clear()

    tasks, constraints = load_data_from_json()
    g.tasks = tasks
    g.constraints = constraints

    # Heading row
    heading_frame = tk.Frame(frame, bg="white")
    heading_frame.pack(fill="x", padx=5, pady=(10, 2))

    for i in range(5):  # 5 columns: name, value, cost, category, status
        heading_frame.grid_columnconfigure(i, weight=1)

    tk.Label(heading_frame, text="Name", bg="white", anchor="w", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5, sticky="ew")
    tk.Label(heading_frame, text="Value", bg="white", anchor="w", font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=5, sticky="ew")
    tk.Label(heading_frame, text="Cost", bg="white", anchor="w", font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=5, sticky="ew")
    tk.Label(heading_frame, text="Category", bg="white", anchor="w", font=('Arial', 10, 'bold')).grid(row=0, column=3, padx=5, sticky="ew")
    tk.Label(heading_frame, text="Status", bg="white", anchor="w", font=('Arial', 10, 'bold')).grid(row=0, column=4, padx=5, sticky="ew")

    # Entries frame
    entries_frame = tk.Frame(frame, bg="white")
    entries_frame.pack(fill="both", expand=True, padx=5)

    for i in range(5):
        entries_frame.grid_columnconfigure(i, weight=1)

    for idx, task in enumerate(tasks):
        # To keep status synced with global sets:
        if task["name"] in g.executed_tasks:
            task["status"] = "Executed"
        elif task["name"] in g.removed_tasks:
            task["status"] = "Removed"
        else:
            task["status"] = task.get("status", "Pending")

        create_entry_row(entries_frame, task_data=task, row=idx)

    # Button row
    def add_new_entry():
        create_entry_row(entries_frame, row=len(entries))

    buttons_frame = tk.Frame(frame, bg="white")
    buttons_frame.pack(fill="x", pady=10)

    tk.Button(buttons_frame, text="Add New Entry", command=add_new_entry).pack(side="left", padx=10)
    tk.Button(buttons_frame, text="Save Tasks", command=save_tasks).pack(side="right", padx=10)
