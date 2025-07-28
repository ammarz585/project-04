import tkinter as tk
from tkinter import ttk
import globals as g
from scheduler import schedule_tasks  # import scheduling logic

def open_results_window(parent):
    frame = tk.Frame(parent, bg=g.current_theme["bg"])

    options_frame = tk.Frame(frame, width=200, bg=g.current_theme["button_bg"])
    options_frame.pack(side="left", fill="y", padx=5, pady=5)

    lbl_title = tk.Label(options_frame, text="Scheduling Strategy",
                         bg=g.current_theme["button_bg"],
                         fg=g.current_theme["button_fg"],
                         font=("Arial", 12, "bold"))
    lbl_title.pack(pady=10)

    strategy_var = tk.StringVar(value="cost")

    rb_cost = tk.Radiobutton(options_frame, text="Cost-Based", variable=strategy_var, value="cost",
                             bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"],
                             selectcolor=g.current_theme["bg"])
    rb_cost.pack(anchor="w", padx=15, pady=5)
    rb_value = tk.Radiobutton(options_frame, text="Value-Based", variable=strategy_var, value="value",
                              bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"],
                              selectcolor=g.current_theme["bg"])
    rb_value.pack(anchor="w", padx=15, pady=5)
    rb_ratio = tk.Radiobutton(options_frame, text="Cost-to-Value Ratio", variable=strategy_var, value="ratio",
                              bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"],
                              selectcolor=g.current_theme["bg"])
    rb_ratio.pack(anchor="w", padx=15, pady=5)

    run_btn = tk.Button(options_frame, text="Run OPTIMIZER",
                        bg=g.current_theme["button_bg"],
                        fg=g.current_theme["button_fg"],
                        width=18, height=2)
    run_btn.pack(pady=20)

    results_frame = tk.Frame(frame, bg=g.current_theme["bg"], bd=2, relief="sunken")
    results_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    canvas = tk.Canvas(results_frame, bg=g.current_theme["bg"], highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = tk.Frame(canvas, bg=g.current_theme["bg"])
    scrollable_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def resize_canvas(event):
        canvas.itemconfig(scrollable_window, width=event.width)

    inner_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", resize_canvas)

    # --- Mouse wheel scrolling support ---
    def _on_mousewheel(event):
        if event.delta:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")  # Windows/macOS
        elif event.num == 4:
            canvas.yview_scroll(-3, "units")  # Linux scroll up
        elif event.num == 5:
            canvas.yview_scroll(3, "units")   # Linux scroll down

    canvas.bind("<Enter>", lambda e: _bind_mousewheel(canvas))
    canvas.bind("<Leave>", lambda e: _unbind_mousewheel(canvas))

    def _bind_mousewheel(widget):
        widget.bind_all("<MouseWheel>", _on_mousewheel)        # Windows/macOS
        widget.bind_all("<Button-4>", _on_mousewheel)          # Linux up
        widget.bind_all("<Button-5>", _on_mousewheel)          # Linux down

    def _unbind_mousewheel(widget):
        widget.unbind_all("<MouseWheel>")
        widget.unbind_all("<Button-4>")
        widget.unbind_all("<Button-5>")

    def run_scheduler():
        for widget in inner_frame.winfo_children():
            widget.destroy()

        strategy = strategy_var.get()

        # Step 1: Reset all task statuses
        for task in g.tasks:
            task["status"] = "Pending"

        # Step 2: Run scheduling
        execution_slots, total_cost, total_value = schedule_tasks(strategy, g.tasks, g.budget, g.parallelism)

        # Step 3: Update task statuses to 'Executed'
        executed_names = {task['name'] for slot in execution_slots for task in slot}
        for task in g.tasks:
            if task["name"] in executed_names:
                task["status"] = "Executed"

        # Step 4: Show results
        for i, slot in enumerate(execution_slots):
            tk.Label(inner_frame, text=f"Slot {i + 1}:", bg=g.current_theme["bg"], fg=g.current_theme["fg"],
                     font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
            for task in slot:
                text = f"- {task['name']} (Cost: {task['cost']}, Value: {task['value']}, Status: {task['status']})"
                tk.Label(inner_frame, text=text, bg=g.current_theme["bg"], fg=g.current_theme["fg"]).pack(anchor="w", padx=30)

        tk.Label(inner_frame, text=f"\nTotal Cost: {total_cost}", bg=g.current_theme["bg"], fg="blue",
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(20, 0))
        tk.Label(inner_frame, text=f"Total Value: {total_value}", bg=g.current_theme["bg"], fg="green",
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=10)
        tk.Label(inner_frame, text=f"Remaining Budget: {g.budget - total_cost}", bg=g.current_theme["bg"], fg="red",
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(0, 20))

    run_btn.config(command=run_scheduler)

    def apply_theme():
        frame.config(bg=g.current_theme["bg"])
        options_frame.config(bg=g.current_theme["button_bg"])
        lbl_title.config(bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"])

        for rb in [rb_cost, rb_value, rb_ratio]:
            rb.config(bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"], selectcolor=g.current_theme["bg"])

        run_btn.config(bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"])
        results_frame.config(bg=g.current_theme["bg"])
        canvas.config(bg=g.current_theme["bg"])
        inner_frame.config(bg=g.current_theme["bg"])

        for child in inner_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=g.current_theme["bg"], fg=g.current_theme["fg"])

    frame.apply_theme = apply_theme
    return frame
