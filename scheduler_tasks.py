import tkinter as tk
from tkinter import ttk
import globals as g
from scheduler import schedule_tasks  # import scheduling logic

def open_results_window(parent):
    frame = tk.Frame(parent, bg="white")

    options_frame = tk.Frame(frame, width=200, bg="#e0e0e0")
    options_frame.pack(side="left", fill="y", padx=5, pady=5)

    tk.Label(options_frame, text="Scheduling Strategy", bg="#e0e0e0", font=("Arial", 12, "bold")).pack(pady=10)

    strategy_var = tk.StringVar(value="cost")

    tk.Radiobutton(options_frame, text="Cost-Based", variable=strategy_var, value="cost", bg="#e0e0e0").pack(anchor="w", padx=15, pady=5)
    tk.Radiobutton(options_frame, text="Value-Based", variable=strategy_var, value="value", bg="#e0e0e0").pack(anchor="w", padx=15, pady=5)
    tk.Radiobutton(options_frame, text="Cost-to-Value Ratio", variable=strategy_var, value="ratio", bg="#e0e0e0").pack(anchor="w", padx=15, pady=5)

    run_btn = tk.Button(options_frame, text="Run Scheduler", bg="#4CAF50", fg="white", width=18, height=2)
    run_btn.pack(pady=20)

    results_frame = tk.Frame(frame, bg="white", bd=2, relief="sunken")
    results_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    canvas = tk.Canvas(results_frame, bg="white")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = tk.Frame(canvas, bg="white")
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
            tk.Label(inner_frame, text=f"Slot {i + 1}:", bg="white", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
            for task in slot:
                tk.Label(inner_frame, text=f"- {task['name']} (Cost: {task['cost']}, Value: {task['value']})", bg="white").pack(anchor="w", padx=30)

        tk.Label(inner_frame, text=f"\nTotal Cost: {total_cost}", bg="white", fg="blue", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(20, 0))
        tk.Label(inner_frame, text=f"Total Value: {total_value}", bg="white", fg="green", font=("Arial", 11, "bold")).pack(anchor="w", padx=10)
        tk.Label(inner_frame, text=f"Remaining Budget: {g.budget - total_cost}", bg="white", fg="red", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(0, 20))

    run_btn.config(command=run_scheduler)

    return frame
