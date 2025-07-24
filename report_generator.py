import globals as g
def save_results_to_report():
    from tkinter import messagebox
    try:
        with open("results_report.txt", "w") as f:
            f.write("Decision-Based Task Scheduler Report\n\n")
            for task in g.tasks:
                f.write(f"Task: {task['name']}, Cost: {task['cost']}, Value: {task['value']}\n")
        messagebox.showinfo("Success", "Results saved to results_report.txt")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save report:\n{e}")
