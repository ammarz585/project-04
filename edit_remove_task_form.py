import tkinter as tk
from tkinter import messagebox
import globals as g

def show_edit_remove_task(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="✏️ Edit / Remove Task", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    listbox = tk.Listbox(content_frame)
    listbox.pack(fill="x", padx=10, pady=5)

    def refresh_list():
        listbox.delete(0, tk.END)
        for t in g.tasks:
            listbox.insert(tk.END, f"{t['name']} (Cost: {t['cost']}, Value: {t['value']})")

    refresh_list()

    entries = {}
    fields = ["Name", "Cost", "Value", "Category", "Dependencies (comma separated)"]
    for field in fields:
        tk.Label(content_frame, text=field + ":", anchor="w", bg="white").pack(fill="x", padx=10)
        ent = tk.Entry(content_frame)
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

    btn_frame = tk.Frame(content_frame, bg="white")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Load", command=load_task, width=12).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Save", command=save_task, width=12).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Remove", command=remove_task, width=12).grid(row=0, column=2, padx=5)
