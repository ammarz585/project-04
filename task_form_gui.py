import tkinter as tk
from tkinter import messagebox
import globals as g  # Import globals module as g

def open_task_form(parent):
    outer_frame = tk.Frame(parent, bg="white", width=1000)
    outer_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(outer_frame, bg="white", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # Scrollbars
    v_scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    v_scrollbar.pack(side="right", fill="y")

    h_scrollbar = tk.Scrollbar(outer_frame, orient="horizontal", command=canvas.xview)
    h_scrollbar.pack(side="bottom", fill="x")

    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    content_container = tk.Frame(canvas, bg="white")
    canvas_window = canvas.create_window((0, 0), window=content_container, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content_container.bind("<Configure>", on_frame_configure)

    def resize_content_container(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind('<Configure>', resize_content_container)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_shift_mousewheel(event):
        canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)
    canvas.bind_all("<Shift-MouseWheel>", on_shift_mousewheel)

    frame = tk.Frame(content_container, bg="white", padx=10, pady=10)
    frame.pack(fill="both", expand=True)

    menu_frame = tk.Frame(frame, bg="#f0f0f0", width=150)
    menu_frame.pack(side="left", fill="y", padx=(0, 10), pady=5)

    content_frame = tk.Frame(frame, bg="white", bd=2, relief="groove")
    content_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    def show_add_task():
        clear_content()
        tk.Label(content_frame, text="➕ Add Task", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        entries = {}
        fields = ["Name", "Cost", "Value", "Category", "Dependencies (comma separated)"]
        for field in fields:
            tk.Label(content_frame, text=field + ":", anchor="w", bg="white").pack(fill="x", padx=10)
            ent = tk.Entry(content_frame)
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

        tk.Button(content_frame, text="Add Task", command=add_task, bg="#4CAF50", fg="white", width=20, height=2).pack(pady=15)

    def show_edit_remove_task():
        clear_content()
        tk.Label(content_frame, text="✏️ Edit  / Remove Task", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

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

        tk.Button(btn_frame, text="Load", command=load_task, width=12, height=1).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Save", command=save_task, width=12, height=1).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Remove", command=remove_task, width=12, height=1).grid(row=0, column=2, padx=5)

    def show_constraints():
        clear_content()
        tk.Label(content_frame, text="⚙️ Modify Constraints", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        budget_var = tk.IntVar(value=g.budget)
        parallel_var = tk.IntVar(value=g.parallelism)

        tk.Label(content_frame, text="Budget:", bg="white").pack()
        tk.Spinbox(content_frame, from_=0, to=10000, textvariable=budget_var, width=15).pack(pady=5)

        tk.Label(content_frame, text="Parallelism:", bg="white").pack()
        tk.Spinbox(content_frame, from_=1, to=100, textvariable=parallel_var, width=15).pack(pady=5)

        def save_constraints():
            g.budget = budget_var.get()
            g.parallelism = parallel_var.get()
            messagebox.showinfo("Saved", f"Budget: {g.budget}, Parallelism: {g.parallelism}")

        tk.Button(content_frame, text="Save", command=save_constraints, bg="#2196F3", fg="white", width=20, height=2).pack(pady=10)

    # Side menu buttons
    tk.Button(menu_frame, text="Add Task", width=15, height=2, command=show_add_task).pack(pady=10)
    tk.Button(menu_frame, text="Edit/Remove", width=15, height=2, command=show_edit_remove_task).pack(pady=10)
    tk.Button(menu_frame, text="Constraints", width=15, height=2, command=show_constraints).pack(pady=10)

    show_add_task()
    return outer_frame
