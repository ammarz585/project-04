import tkinter as tk
import globals as g
from tkinter import messagebox
from task_management import show_add_task  # We'll also add populate_tasks_from_json below
from task_management import show_edit_remove_task
from constraints_management import show_constraints
from json_task_loader import load_tasks_to_frame
def open_task_form(parent):
    outer_frame = tk.Frame(parent, bg="white", width=1000)
    outer_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(outer_frame, bg="white", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

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

    # New helper function to populate tasks loaded from JSON
    def populate_tasks_from_json(tasks, parent_frame):
        clear_content()
        # Headers for columns
        headers = ["Task Name", "Value", "Cost", "Category"]
        for col, text in enumerate(headers):
            label = tk.Label(parent_frame, text=text, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", width=15)
            label.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)

        for row_idx, task in enumerate(tasks, start=1):
            # Create entries filled with JSON data
            e_name = tk.Entry(parent_frame)
            e_name.insert(0, task.get("name", ""))
            e_name.grid(row=row_idx, column=0, sticky="nsew", padx=2, pady=2)

            e_value = tk.Entry(parent_frame)
            e_value.insert(0, str(task.get("value", "")))
            e_value.grid(row=row_idx, column=1, sticky="nsew", padx=2, pady=2)

            e_cost = tk.Entry(parent_frame)
            e_cost.insert(0, str(task.get("cost", "")))
            e_cost.grid(row=row_idx, column=2, sticky="nsew", padx=2, pady=2)

            e_category = tk.Entry(parent_frame)
            e_category.insert(0, task.get("category", ""))
            e_category.grid(row=row_idx, column=3, sticky="nsew", padx=2, pady=2)

        # Make columns expand equally
        for col in range(len(headers)):
            parent_frame.grid_columnconfigure(col, weight=1)



    # Buttons on left menu
    tk.Button(menu_frame, text="Add Task", width=15, height=2, command=lambda: (clear_content(), show_add_task(content_frame))).pack(pady=10)
    tk.Button(menu_frame, text="Edit/Remove", width=15, height=2, command=lambda: (clear_content(), show_edit_remove_task(content_frame))).pack(pady=10)
    tk.Button(menu_frame, text="Constraints", width=15, height=2, command=lambda: (clear_content(), show_constraints(content_frame))).pack(pady=10)
    tk.Button(menu_frame, text="Load Data from JSON", width=15, height=2, command=lambda: load_tasks_to_frame(content_frame)).pack(pady=10)

    show_add_task(content_frame)  # Show Add Task page by default

    return outer_frame
