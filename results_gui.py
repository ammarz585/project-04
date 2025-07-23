import tkinter as tk

def open_results_window():
    window = tk.Toplevel()
    window.title("Scheduling Results")
    window.geometry("500x300")
    tk.Label(window, text="Results Window Coming Soon!", font=("Arial", 14)).pack(pady=100)
