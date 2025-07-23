import tkinter as tk
from task_form_gui import open_task_form
from results_gui import open_results_window
from graphs import open_graphs_window

def open_main_menu():
    root = tk.Tk()
    root.title("Decision-Based Task Scheduler")
    root.geometry("600x400")
    root.config(bg="#f2f2f2")

    tk.Label(root, text="Main Menu", font=("Arial", 20, "bold"), bg="#f2f2f2").pack(pady=20)

    tk.Button(root, text="➕ Add/Edit Projects & Tasks", width=30, command=open_task_form).pack(pady=10)
    tk.Button(root, text="📊 View Scheduling Results", width=30, command=open_results_window).pack(pady=10)
    tk.Button(root, text="📈 View Graphs", width=30, command=open_graphs_window).pack(pady=10)
    tk.Button(root, text="❌ Exit", width=30, command=root.quit).pack(pady=20)

    root.mainloop()
