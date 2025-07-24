import tkinter as tk
import globals as g
from themes import toggle_theme, apply_theme_to_widget
from pages_load import load_task_form, load_results_window, load_graphs_window
import navigation_helpers as nav

def save_results_to_report():
    # Placeholder function to save results.
    # You can replace this with your actual report generation logic.
    # For example, gather data from globals or results page and write to a file.
    from tkinter import messagebox
    try:
        # Dummy example: write tasks to a text file as report
        with open("results_report.txt", "w") as f:
            f.write("Decision-Based Task Scheduler Report\n\n")
            for task in g.tasks:
                f.write(f"Task: {task['name']}, Cost: {task['cost']}, Value: {task['value']}\n")
        messagebox.showinfo("Success", "Results saved to results_report.txt")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save report:\n{e}")

def open_main_menu():
    root = tk.Tk()
    root.title("Decision-Based Task Scheduler")
    root.geometry("600x400")
    root.config(bg=g.current_theme["bg"])
    root.minsize(500, 350)

    current_page_index = [0]
    pages = [None]

    nav_frame = tk.Frame(root, bg=g.current_theme["bg"])
    nav_frame.pack(side="top", anchor="nw", pady=5, padx=5)

    btn_prev = tk.Button(nav_frame, text="⬅", width=3,
                         bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"])
    btn_prev.pack(side="left", padx=2)

    btn_next = tk.Button(nav_frame, text="➡", width=3,
                         bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"])
    btn_next.pack(side="left", padx=2)

    btn_main_menu = tk.Button(nav_frame, text="Main Menu", width=12,
                              bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"])
    btn_main_menu.pack(side="left", padx=10)

    btn_toggle_theme = tk.Button(nav_frame, text="🌓", width=3,
                                 bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"])
    btn_toggle_theme.pack(side="left", padx=2)

    title_label = tk.Label(root, text="Decision-Based Task Scheduler",
                           font=("Arial", 20, "bold"),
                           bg=g.current_theme["bg"], fg=g.current_theme["fg"])
    title_label.pack(pady=(10, 5))

    container = tk.Frame(root, bg=g.current_theme["bg"])
    container.pack(fill="both", expand=True)

    pages.extend([
        load_task_form(container),
        load_results_window(container),
        load_graphs_window(container)
    ])

    for page in pages[1:]:
        page.place(relwidth=1, relheight=1)
        page.place_forget()

    main_menu_btn_frame = tk.Frame(root, bg=g.current_theme["bg"])
    main_menu_btn_frame.pack(pady=(5, 20))

    btn_prev.config(command=lambda: nav.go_prev(current_page_index, pages, main_menu_btn_frame,
                                               title_label, btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget))
    btn_next.config(command=lambda: nav.go_next(current_page_index, pages, main_menu_btn_frame,
                                               title_label, btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget))
    btn_main_menu.config(command=lambda: nav.go_main_menu(current_page_index, pages, main_menu_btn_frame,
                                                         title_label, btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget))

    def on_toggle_theme():
        toggle_theme()
        apply_theme_to_widget(root)

    btn_toggle_theme.config(command=on_toggle_theme)

    button_params = {
        "width": 35,
        "height": 2,
        "bg": g.current_theme["button_bg"],
        "fg": g.current_theme["button_fg"],
        "padx": 5,
        "pady": 8,
    }

    tk.Button(main_menu_btn_frame, text="➕ Add/Edit Projects & Tasks", command=lambda: nav.show_page(1, current_page_index, pages,
                                                                                                main_menu_btn_frame, title_label,
                                                                                                btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget),
              **button_params).pack(pady=5)

    tk.Button(main_menu_btn_frame, text="📊 View Scheduling Results", command=lambda: nav.show_page(2, current_page_index, pages,
                                                                                                   main_menu_btn_frame, title_label,
                                                                                                   btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget),
              **button_params).pack(pady=5)

    tk.Button(main_menu_btn_frame, text="📈 View Graphs", command=lambda: nav.show_page(3, current_page_index, pages,
                                                                                        main_menu_btn_frame, title_label,
                                                                                        btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget),
              **button_params).pack(pady=5)

    # New Save Results button
    tk.Button(main_menu_btn_frame, text="💾 Save Results to Report", command=save_results_to_report, **button_params).pack(pady=5)

    tk.Button(main_menu_btn_frame, text="❌ Exit", command=root.quit, **button_params).pack(pady=10)

    root.bind_all('<KeyPress>', lambda e: nav.on_key_press(e, current_page_index, pages,
                                                          lambda idx, ci, p, mmf, tl, bp, bn, bm, r, atw: nav.show_page(idx, ci, p, mmf, tl, bp, bn, bm, r, atw),
                                                          lambda ci, p: nav.go_prev(ci, p, main_menu_btn_frame, title_label, btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget),
                                                          lambda ci, p: nav.go_next(ci, p, main_menu_btn_frame, title_label, btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget),
                                                          lambda ci, p: nav.go_main_menu(ci, p, main_menu_btn_frame, title_label, btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget)
                                                          ))

    nav.show_page(0, current_page_index, pages, main_menu_btn_frame, title_label, btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget)

    root.mainloop()
