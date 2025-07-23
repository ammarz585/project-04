import tkinter as tk
from task_form_gui import open_task_form
from results_gui import open_results_window
from graphs import open_graphs_window
import globals as g
from themes import toggle_theme, apply_theme_to_widget  # Theme functions imported

def open_main_menu():
    root = tk.Tk()
    root.title("Decision-Based Task Scheduler")
    root.geometry("600x400")
    root.config(bg=g.current_theme["bg"])
    root.minsize(500, 350)

    current_page_index = [0]
    pages = [None]  # Placeholder for main menu page

    # Navigation frame top-left
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

    # Title label
    title_label = tk.Label(root, text="Decision-Based Task Scheduler",
                           font=("Arial", 20, "bold"),
                           bg=g.current_theme["bg"], fg=g.current_theme["fg"])
    title_label.pack(pady=(10, 5))

    # Container for pages
    container = tk.Frame(root, bg=g.current_theme["bg"])
    container.pack(fill="both", expand=True)

    # Create pages
    pages.extend([
        open_task_form(container),
        open_results_window(container),
        open_graphs_window(container)
    ])

    for page in pages[1:]:
        page.place(relwidth=1, relheight=1)
        page.place_forget()

    # Main menu buttons frame
    main_menu_btn_frame = tk.Frame(root, bg=g.current_theme["bg"])
    main_menu_btn_frame.pack(pady=(5, 20))  # Moved slightly up, more bottom padding

    # Show page function
    def show_page(index):
        index = max(0, min(index, len(pages) - 1))
        current_page_index[0] = index

        if index == 0:
            main_menu_btn_frame.pack(pady=(5, 20))
            for p in pages[1:]:
                p.place_forget()
            title_label.config(text="Decision-Based Task Scheduler")
            btn_prev.config(state="disabled")
            btn_next.config(state="disabled")
            btn_main_menu.config(state="disabled")
        else:
            main_menu_btn_frame.pack_forget()
            for p in pages[1:]:
                p.place(relwidth=1, relheight=1)
                p.lower()
            pages[index].lift()
            titles = ["", "Add/Edit Projects & Tasks", "Scheduling Results", "Graphs"]
            title_label.config(text=titles[index])
            btn_prev.config(state="normal" if index > 1 else "disabled")
            btn_next.config(state="normal" if index < len(pages) - 1 else "disabled")
            btn_main_menu.config(state="normal")

        apply_theme_to_widget(root)  # Refresh theme colors dynamically

    # Navigation handlers
    def go_prev():
        if current_page_index[0] > 1:
            show_page(current_page_index[0] - 1)

    def go_next():
        if 1 <= current_page_index[0] < len(pages) - 1:
            show_page(current_page_index[0] + 1)

    def go_main_menu():
        show_page(0)

    btn_prev.config(command=go_prev)
    btn_next.config(command=go_next)
    btn_main_menu.config(command=go_main_menu)

    # Theme toggle handler
    def on_toggle_theme():
        toggle_theme()         # Change global theme variable
        apply_theme_to_widget(root)  # Update all widgets colors

    btn_toggle_theme.config(command=on_toggle_theme)

    # Main menu buttons with bigger size and padding
    button_params = {
        "width": 35,
        "height": 2,
        "bg": g.current_theme["button_bg"],
        "fg": g.current_theme["button_fg"],
        "padx": 5,
        "pady": 8,
    }

    tk.Button(main_menu_btn_frame, text="➕ Add/Edit Projects & Tasks", command=lambda: show_page(1), **button_params).pack(pady=5)
    tk.Button(main_menu_btn_frame, text="📊 View Scheduling Results", command=lambda: show_page(2), **button_params).pack(pady=5)
    tk.Button(main_menu_btn_frame, text="📈 View Graphs", command=lambda: show_page(3), **button_params).pack(pady=5)
    tk.Button(main_menu_btn_frame, text="❌ Exit", command=root.quit, **button_params).pack(pady=10)

    # Keyboard shortcuts: Ctrl + Left/Right for navigation, M for main menu
    def on_key_press(event):
        if event.state & 0x4:  # Ctrl pressed
            if event.keysym == 'Right':
                go_next()
            elif event.keysym == 'Left':
                go_prev()
        elif event.keysym.lower() == 'm':
            go_main_menu()

    root.bind_all('<KeyPress>', on_key_press)

    show_page(0)  # Start at main menu
    root.mainloop()
