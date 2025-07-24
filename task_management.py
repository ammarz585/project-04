import tkinter as tk
from tkinter import messagebox
import globals as g
from themes import apply_theme_to_widget

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
            "dependencies": dependencies
        })

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
            listbox.insert(tk.END, f"{t['name']} (Cost: {t['cost']}, Value: {t['value']})")

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

        g.tasks[index] = {
            "name": name,
            "cost": int(cost),
            "value": int(value),
            "category": category,
            "dependencies": dependencies
        }

        refresh_list()
        messagebox.showinfo("Success", "Task updated")

    def remove_task():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task first")
            return
        index = selected[0]
        del g.tasks[index]
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
