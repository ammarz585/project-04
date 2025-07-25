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


def show_add_task(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()
    tk.Label(content_frame, text="➕ Add Task", font=("Arial", 14, "bold"),
             bg=g.current_theme["bg"], fg=g.current_theme["fg"]).pack(pady=10)

    entries = {}
    fields = ["Name", "Cost", "Value", "Category", "Dependencies (comma separated)"]
    for field in fields:
        tk.Label(content_frame, text=field + ":", anchor="w",
                 bg=g.current_theme["bg"], fg=g.current_theme["fg"]).pack(fill="x", padx=10)
        ent = tk.Entry(content_frame, bg="white", fg="black")
        ent.pack(fill="x", expand=True, padx=10, pady=5)
        entries[field] = ent

    def add_task():
        name = entries["Name"].get().strip()
        cost = entries["Cost"].get().strip()
        value = entries["Value"].get().strip()
        category = entries["Category"].get().strip()
        dependencies = [d.strip() for d in entries["Dependencies (comma separated)"].get().split(",") if d.strip()]

        if not name or not cost.isdigit() or not value.isdigit():
            messagebox.showerror("Error", "Please enter valid name, numeric cost and value.")
            return

        g.tasks.append({
            "name": name,
            "cost": int(cost),
            "value": int(value),
            "category": category,
            "dependencies": dependencies,
            "status": "Pending"  # <-- New status field
        })

        save_tasks_to_json()  # Save after adding task

        messagebox.showinfo("Success", f"Task '{name}' added!")
        for ent in entries.values():
            ent.delete(0, tk.END)

    btn = tk.Button(content_frame, text="Add Task", command=add_task,
                    bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"],
                    activebackground=g.current_theme["button_active_bg"],
                    activeforeground=g.current_theme["button_active_fg"],
                    width=20, height=2)
    apply_theme_to_widget(btn)
    btn.pack(pady=15)


def show_edit_remove_task(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="✏️ Edit / Remove Task", font=("Arial", 14, "bold"),
             bg=g.current_theme["bg"], fg=g.current_theme["fg"]).pack(pady=10)

    listbox = tk.Listbox(content_frame, bg="white", fg="black")
    listbox.pack(fill="x", padx=10, pady=5)

    def refresh_list():
        listbox.delete(0, tk.END)
        for t in g.tasks:
            status = t.get("status", "Pending")  # Display status
            listbox.insert(tk.END, f"{t['name']} (Cost: {t['cost']}, Value: {t['value']}, Status: {status})")

    refresh_list()

    entries = {}
    fields = ["Name", "Cost", "Value", "Category", "Dependencies (comma separated)"]
    for field in fields:
        tk.Label(content_frame, text=field + ":", anchor="w",
                 bg=g.current_theme["bg"], fg=g.current_theme["fg"]).pack(fill="x", padx=10)
        ent = tk.Entry(content_frame, bg="white", fg="black")
        ent.pack(fill="x", expand=True, padx=10, pady=5)
        entries[field] = ent

    def load_task():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task first")
            return
        index = selected[0]
        t = g.tasks[index]
        entries["Name"].delete(0, tk.END)
        entries["Name"].insert(0, t["name"])
        entries["Cost"].delete(0, tk.END)
        entries["Cost"].insert(0, str(t["cost"]))
        entries["Value"].delete(0, tk.END)
        entries["Value"].insert(0, str(t["value"]))
        entries["Category"].delete(0, tk.END)
        entries["Category"].insert(0, t["category"])
        entries["Dependencies (comma separated)"].delete(0, tk.END)
        entries["Dependencies (comma separated)"].insert(0, ", ".join(t["dependencies"]))

    def save_task():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task first")
            return
        index = selected[0]
        name = entries["Name"].get().strip()
        cost = entries["Cost"].get().strip()
        value = entries["Value"].get().strip()
        category = entries["Category"].get().strip()
        dependencies = [d.strip() for d in entries["Dependencies (comma separated)"].get().split(",") if d.strip()]

        if not name or not cost.isdigit() or not value.isdigit():
            messagebox.showerror("Error", "Enter valid values")
            return

        old_status = g.tasks[index].get("status", "Pending")  # Preserve existing status

        g.tasks[index] = {
            "name": name,
            "cost": int(cost),
            "value": int(value),
            "category": category,
            "dependencies": dependencies,
            "status": old_status  # Re-set previous status
        }

        save_tasks_to_json()  # Save after editing task

        refresh_list()
        messagebox.showinfo("Success", "Task updated")

    def remove_task():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task first")
            return
        index = selected[0]
        del g.tasks[index]

        save_tasks_to_json()  # Save after removing task

        refresh_list()
        messagebox.showinfo("Success", "Task removed")

    btn_frame = tk.Frame(content_frame, bg=g.current_theme["bg"],
                         highlightbackground=g.current_theme["bg"], highlightthickness=2)
    btn_frame.pack(pady=10)

    btns = [
        ("Load", load_task),
        ("Save", save_task),
        ("Remove", remove_task)
    ]

    for i, (label, cmd) in enumerate(btns):
        btn = tk.Button(btn_frame, text=label, command=cmd, width=12, height=1,
                        bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"],
                        activebackground=g.current_theme["button_active_bg"],
                        activeforeground=g.current_theme["button_active_fg"])
        apply_theme_to_widget(btn)
        btn.grid(row=0, column=i, padx=5)
