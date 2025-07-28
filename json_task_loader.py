import tkinter as tk
from tkinter import messagebox
import json
import globals as g
import os
import sys
entries = []
selected_vars = {}  # maps row idx to BooleanVar for checkbox selection
current_frame = None
ui_extra_entries = 0  # number of unsaved empty new rows in UI
JSON_PATH = "import_data.json" 
def resource_path(relative_path):
    """ Get absolute path to resource, works for development and for PyInstaller .exe """
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this in onefile mode
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_data_from_json(filepath=None):
    if filepath is None:
        filepath = resource_path("import_data.json")
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        tasks = data.get('tasks', [])
        constraints = data.get('constraints', [])
        return tasks, constraints
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load JSON:\n{e}")
        return [], []

def save_data_to_json(filepath=JSON_PATH):
    try:
        with open(filepath, 'w') as file:
            json.dump({"tasks": g.tasks, "constraints": g.constraints}, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save JSON:\n{e}")

def create_entry_row(frame, task_data, row, select_vars, is_extra=False):
    name_var = tk.StringVar(value=task_data.get("name", ""))
    value_var = tk.StringVar(value=str(task_data.get("value", "")))
    cost_var = tk.StringVar(value=str(task_data.get("cost", "")))
    category_var = tk.StringVar(value=task_data.get("category", ""))
    status_var = tk.StringVar(value=task_data.get("status", "Pending"))

    cb = tk.Checkbutton(frame, variable=select_vars[row])
    if is_extra:
        # Disable checkbox on new empty rows so user can't delete them by mistake
        cb.configure(state="disabled")
    cb.grid(row=row, column=0, padx=3, pady=2)

    e_name = tk.Entry(frame, textvariable=name_var)
    e_name.grid(row=row, column=1, padx=3, pady=2, sticky="ew")

    e_value = tk.Entry(frame, textvariable=value_var)
    e_value.grid(row=row, column=2, padx=3, pady=2, sticky="ew")

    e_cost = tk.Entry(frame, textvariable=cost_var)
    e_cost.grid(row=row, column=3, padx=3, pady=2, sticky="ew")

    e_category = tk.Entry(frame, textvariable=category_var)
    e_category.grid(row=row, column=4, padx=3, pady=2, sticky="ew")

    e_status = tk.Entry(frame, textvariable=status_var, state="readonly")
    e_status.grid(row=row, column=5, padx=3, pady=2, sticky="ew")

    # Save vars for access when saving
    entries.append({
        "name": name_var,
        "value": value_var,
        "cost": cost_var,
        "category": category_var,
        "status": status_var
    })

def save_tasks():
    global entries, ui_extra_entries
    new_tasks = []
    for row_vars in entries:
        name = row_vars["name"].get().strip()
        if not name:
            continue
        try:
            value = int(row_vars["value"].get())
        except:
            value = 0
        try:
            cost = int(row_vars["cost"].get())
        except:
            cost = 0
        category = row_vars["category"].get().strip()

        # Status depends on external global lists (executed, removed)
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
    ui_extra_entries = 0  # clear extra empty rows after save
    save_data_to_json()
    messagebox.showinfo("Success", "Tasks saved successfully.")
    # Reload UI with saved tasks to reflect changes and clear extras
    if current_frame:
        load_tasks_to_frame(current_frame)

def load_json_to_globals():
    global current_frame, ui_extra_entries
    tasks, constraints = load_data_from_json()
    g.tasks = tasks
    g.constraints = constraints
    ui_extra_entries = 0  # Reset extras on load
    messagebox.showinfo("Loaded", "Data loaded into global variables.")
    if current_frame:
        load_tasks_to_frame(current_frame, load_into_globals=True)

def show_existing_data():
    global current_frame
    tasks, _ = load_data_from_json()
    if current_frame:
        load_tasks_to_frame(current_frame, tasks=tasks, load_into_globals=False)
    

def delete_selected_entries(select_vars):
    global current_frame
    # Only allow deletion for indices within actual tasks (not extra UI rows)
    valid_indices = [idx for idx in select_vars if idx < len(g.tasks)]
    selected_rows = [idx for idx in valid_indices if select_vars[idx].get()]
    if not selected_rows:
        messagebox.showwarning("Warning", "Please select one or more entries to delete.")
        return

    selected_rows.sort(reverse=True)  # Delete from end so indices don't shift

    for idx in selected_rows:
        g.tasks.pop(idx)

    save_data_to_json()
    messagebox.showinfo("Deleted", f"Deleted {len(selected_rows)} selected entries.")
    # Reload UI to reflect deletion
    if current_frame:
        load_tasks_to_frame(current_frame)

def load_tasks_to_frame(frame, tasks=None, load_into_globals=True):
    global current_frame, entries, selected_vars, ui_extra_entries
    current_frame = frame
    entries.clear()

    if tasks is None:
        tasks = g.tasks

    if load_into_globals:
        g.tasks = tasks

    total_rows = len(tasks) + ui_extra_entries
    selected_vars = {i: tk.BooleanVar(value=False) for i in range(total_rows)}

    # Clear frame contents
    for widget in frame.winfo_children():
        widget.destroy()

    # Header row
    heading_frame = tk.Frame(frame, bg="white")
    heading_frame.pack(fill="x", padx=5, pady=(10, 2))

    headings = ["Select", "Name", "Value", "Cost", "Category", "Status"]
    for col, text in enumerate(headings):
        lbl = tk.Label(heading_frame, text=text, font=("Arial", 10, "bold"), bg="white")
        lbl.grid(row=0, column=col, sticky="ew", padx=3, pady=2)
        heading_frame.grid_columnconfigure(col, weight=1)

    # Scrollable frame container (fixed height so buttons stay visible)
    container = tk.Frame(frame, height=350)  # adjust height as needed
    container.pack(fill="both", expand=False, padx=5, pady=5)

    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scrollable_frame = tk.Frame(canvas)
    scrollable_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def resize_canvas(event):
        canvas.itemconfig(scrollable_window, width=event.width)

    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", resize_canvas)

    # === Add mouse wheel scrolling support here ===
    def _on_mousewheel(event):
        # For Windows and MacOS
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux_up(event):
        canvas.yview_scroll(-1, "units")

    def _on_mousewheel_linux_down(event):
        canvas.yview_scroll(1, "units")

    # Bind mouse wheel to canvas scroll
    canvas.bind_all("<MouseWheel>", _on_mousewheel)          # Windows and MacOS
    canvas.bind_all("<Button-4>", _on_mousewheel_linux_up)   # Linux scroll up
    canvas.bind_all("<Button-5>", _on_mousewheel_linux_down) # Linux scroll down

    # Task rows
    for idx, task in enumerate(tasks):
        if task["name"] in g.executed_tasks:
            task["status"] = "Executed"
        elif task["name"] in g.removed_tasks:
            task["status"] = "Removed"
        else:
            task["status"] = task.get("status", "Pending")
        create_entry_row(scrollable_frame, task, idx, selected_vars, is_extra=False)

    # Extra entry rows
    for i in range(ui_extra_entries):
        empty_task = {
            "name": "",
            "value": 0,
            "cost": 0,
            "category": "",
            "status": "Pending"
        }
        entry_widgets = create_entry_row(scrollable_frame, empty_task, len(tasks) + i, selected_vars, is_extra=True)

    # Button panel (always visible)
    buttons_frame = tk.Frame(frame, bg="white")
    buttons_frame.pack(fill="x", padx=5, pady=5)

    def add_new_entry():
        global ui_extra_entries
        ui_extra_entries += 1
        save_current_ui_to_globals()
        load_tasks_to_frame(current_frame)
        frame.after(100, lambda: entries[-1]["name"].focus_set())

    def save_current_ui_to_globals():
        global entries
        temp_tasks = []
        for row_vars in entries:
            name = row_vars["name"].get().strip()
            if not name:
                continue
            try:
                value = int(row_vars["value"].get())
            except:
                value = 0
            try:
                cost = int(row_vars["cost"].get())
            except:
                cost = 0
            category = row_vars["category"].get().strip()

            if name in g.executed_tasks:
                status = "Executed"
            elif name in g.removed_tasks:
                status = "Removed"
            else:
                status = "Pending"

            temp_tasks.append({
                "name": name,
                "value": value,
                "cost": cost,
                "category": category,
                "status": status
            })
        g.tasks = temp_tasks

    tk.Button(buttons_frame, text="Add New Entry", command=add_new_entry).pack(side="left", padx=5)
    tk.Button(buttons_frame, text="Delete Selected Entries", command=lambda: delete_selected_entries(selected_vars)).pack(side="left", padx=5)
    tk.Button(buttons_frame, text="Show Existing Data", command=show_existing_data).pack(side="left", padx=5)
    tk.Button(buttons_frame, text="Load to System", command=load_json_to_globals).pack(side="left", padx=5)
    tk.Button(buttons_frame, text="Save Changes", command=save_tasks).pack(side="right", padx=5)

    def on_resize(event):
        canvas.configure(width=event.width)

    frame.bind("<Configure>", on_resize)
