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

    canvas = tk.Canvas(results_frame, bg=g.current_theme["bg"])
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = tk.Frame(canvas, bg=g.current_theme["bg"])
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner_frame.bind("<Configure>", on_frame_configure)

    def run_scheduler():
        for widget in inner_frame.winfo_children():
            widget.destroy()

        strategy = strategy_var.get()
        execution_slots, total_cost, total_value = schedule_tasks(strategy, g.tasks, g.budget, g.parallelism)

        for i, slot in enumerate(execution_slots):
            tk.Label(inner_frame, text=f"Slot {i + 1}:", bg=g.current_theme["bg"], fg=g.current_theme["fg"],
                     font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
            for task in slot:
                tk.Label(inner_frame, text=f"- {task['name']} (Cost: {task['cost']}, Value: {task['value']})",
                         bg=g.current_theme["bg"], fg=g.current_theme["fg"]).pack(anchor="w", padx=30)

        tk.Label(inner_frame, text=f"\nTotal Cost: {total_cost}", bg=g.current_theme["bg"], fg="blue",
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(20, 0))
        tk.Label(inner_frame, text=f"Total Value: {total_value}", bg=g.current_theme["bg"], fg="green",
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=10)
        tk.Label(inner_frame, text=f"Remaining Budget: {g.budget - total_cost}", bg=g.current_theme["bg"], fg="red",
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(0, 20))

    run_btn.config(command=run_scheduler)

    # Theme apply function to update colors dynamically
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

        # Update all labels inside inner_frame (if any)
        for child in inner_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=g.current_theme["bg"], fg=g.current_theme["fg"])

    frame.apply_theme = apply_theme  # Attach method for external calls

    return frame
