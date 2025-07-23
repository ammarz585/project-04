import tkinter as tk

def open_graphs_window():
    window = tk.Toplevel()
    window.title("Graphs")
    window.geometry("500x300")
    tk.Label(window, text="Graphs GUI Coming Soon!", font=("Arial", 14)).pack(pady=100)
