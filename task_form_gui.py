import tkinter as tk
import globals as g
from task_management import show_add_task, show_edit_remove_task
from constraints_management import show_constraints

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

    # Buttons call imported functions with content_frame as argument
    tk.Button(menu_frame, text="Add Task", width=15, height=2, command=lambda: show_add_task(content_frame)).pack(pady=10)
    tk.Button(menu_frame, text="Edit/Remove", width=15, height=2, command=lambda: show_edit_remove_task(content_frame)).pack(pady=10)
    tk.Button(menu_frame, text="Constraints", width=15, height=2, command=lambda: show_constraints(content_frame)).pack(pady=10)

    show_add_task(content_frame)  # Show Add Task by default

    return outer_frame
