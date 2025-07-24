import tkinter as tk
from tkinter import messagebox
import globals as g

def show_edit_remove_task(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    bg = g.current_theme["bg"]
    fg = g.current_theme["fg"]
    button_bg = g.current_theme["button_bg"]
    button_fg = g.current_theme["button_fg"]
    border_color = g.current_theme.get("border_color", bg)

    content_frame.config(bg=bg)

    tk.Label(content_frame, text="✏️ Edit / Remove Task",
             font=("Arial", 14, "bold"),
             bg=bg, fg=fg).pack(pady=10)

    # Frame to hold listbox and scrollbar
    listbox_frame = tk.Frame(content_frame, bg=bg)
    listbox_frame.pack(fill="x", padx=10, pady=5)

    listbox = tk.Listbox(listbox_frame, bg=bg, fg=fg,
                         highlightbackground=border_color, highlightthickness=1,
                         selectbackground=button_bg, selectforeground=button_fg,
                         height=8)  # set visible rows

    scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)

    listbox.pack(side="left", fill="x", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refresh_list():
        listbox.delete(0, tk.END)
        for t in g.tasks:
            listbox.insert(tk.END, f"{t['name']} (Cost: {t['cost']}, Value: {t['value']})")

    refresh_list()

    entries = {}
    fields = ["Name", "Cost", "Value", "Category", "Dependencies (comma separated)"]
    for field in fields:
        tk.Label(content_frame, text=field + ":",
                 anchor="w", bg=bg, fg=fg).pack(fill="x", padx=10)
        ent = tk.Entry(content_frame, bg=button_bg, fg=button_fg,
                       insertbackground=button_fg,  # cursor color
                       highlightbackground=border_color, highlightthickness=1)
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
        entries["Dependencies (comma separated)"].insert(0, ", ".join(t.get("dependencies", [])))

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

    btn_frame = tk.Frame(content_frame, bg=bg)
    btn_frame.pack(pady=10)

    btn_params = {
        "bg": button_bg,
        "fg": button_fg,
        "borderwidth": 0,
        "highlightthickness": 0,
        "relief": "flat",
        "width": 12,
    }

    tk.Button(btn_frame, text="Load", command=load_task, **btn_params).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Save", command=save_task, **btn_params).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Remove", command=remove_task, **btn_params).grid(row=0, column=2, padx=5)
