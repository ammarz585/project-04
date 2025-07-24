import tkinter as tk
from tkinter import messagebox
import globals as g

def show_constraints(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Use theme colors from globals
    bg = g.current_theme["bg"]
    fg = g.current_theme["fg"]
    btn_bg =  "#2196F3"
    btn_fg = g.current_theme.get("button_fg", "white")

    content_frame.config(bg=bg)

    tk.Label(content_frame, text="⚙️ Modify Constraints", font=("Arial", 14, "bold"),
             bg=bg, fg=fg).pack(pady=10)

    budget_var = tk.IntVar(value=g.budget)
    parallel_var = tk.IntVar(value=g.parallelism)

    tk.Label(content_frame, text="Budget:", bg=bg, fg=fg).pack()
    tk.Spinbox(content_frame, from_=0, to=10000, textvariable=budget_var,
               width=15, bg=bg, fg=fg, insertbackground=fg).pack(pady=5)

    tk.Label(content_frame, text="Parallelism:", bg=bg, fg=fg).pack()
    tk.Spinbox(content_frame, from_=1, to=100, textvariable=parallel_var,
               width=15, bg=bg, fg=fg, insertbackground=fg).pack(pady=5)

    def save_constraints():
        g.budget = budget_var.get()
        g.parallelism = parallel_var.get()
        messagebox.showinfo("Saved", f"Budget: {g.budget}, Parallelism: {g.parallelism}")

    tk.Button(content_frame, text="Save", command=save_constraints,
              bg=btn_bg, fg=btn_fg, activebackground=g.current_theme.get("button_active_bg", btn_bg),
              activeforeground=g.current_theme.get("button_active_fg", btn_fg),
              width=20, height=2).pack(pady=10)
