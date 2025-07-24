import tkinter as tk
from tkinter import messagebox
import globals as g

def show_constraints(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()
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
