import tkinter as tk
import functools
import globals as g
from themes import toggle_theme, apply_theme_to_widget
from pages_load import load_task_form, load_results_window, load_graphs_window, load_user_guide
import navigation_helpers as nav
from report_generator import save_results_to_report

def open_main_menu():
    root = tk.Tk()
    root.title("Decision-Based Task Scheduler")
    root.geometry("600x400")
    root.config(bg=g.current_theme["bg"])
    root.minsize(600, 550)
    root.bind("<Escape>", lambda e: root.quit())

    current_page_index = [0]
    pages = [None]  # index 0 = main menu

    def btn_colors():
        return {
            "bg": g.current_theme["button_bg"],
            "fg": g.current_theme["button_fg"],
            "activebackground": g.current_theme.get("button_active_bg", g.current_theme["button_bg"]),
            "activeforeground": g.current_theme.get("button_active_fg", g.current_theme["button_fg"]),
            "highlightbackground": g.current_theme["border_color"],
            "highlightthickness": 1,
            "relief": "flat"
        }

    nav_frame = tk.Frame(root, bg=g.current_theme["bg"],
                         highlightbackground=g.current_theme["border_color"], highlightthickness=1)
    nav_frame.pack(side="top", anchor="nw", pady=5, padx=5)

    btn_prev = tk.Button(nav_frame, text="⭠", width=3, **btn_colors())
    btn_prev.pack(side="left", padx=2)

    btn_next = tk.Button(nav_frame, text="➡", width=3, **btn_colors())
    btn_next.pack(side="left", padx=2)

    btn_main_menu = tk.Button(nav_frame, text="Main Menu", width=12, **btn_colors())
    btn_main_menu.pack(side="left", padx=10)

    btn_toggle_theme = tk.Button(nav_frame, text="🌃", width=3, **btn_colors())
    btn_toggle_theme.pack(side="left", padx=2)

    title_label = tk.Label(root, text="COMPLEX DECISION MAKING SIMULATOR",
                           font=("Arial", 20, "bold"),
                           bg=g.current_theme["bg"],
                           fg=g.current_theme["fg"])
    title_label.pack(pady=(10, 5))

    container = tk.Frame(root, bg=g.current_theme["bg"],
                         highlightbackground=g.current_theme["border_color"], highlightthickness=1)
    container.pack(fill="both", expand=True)

    pages.extend([
        load_task_form(container),
        load_results_window(container),
        load_graphs_window(container),
        load_user_guide(container)
    ])

    for page in pages[1:]:
        page.place(relwidth=1, relheight=1)
        page.place_forget()

    main_menu_btn_frame = tk.Frame(root, bg=g.current_theme["bg"],
                                   highlightbackground=g.current_theme["border_color"], highlightthickness=1)
    main_menu_btn_frame.pack(pady=(5, 20))

    button_params = btn_colors()
    button_params.update({
        "width": 35,
        "height": 2,
        "padx": 5,
        "pady": 8
    })

    # Bind navigation button commands using functools.partial
    btn_prev.config(command=functools.partial(nav.go_prev, current_page_index, pages,
                                             main_menu_btn_frame, title_label,
                                             btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget))
    btn_next.config(command=functools.partial(nav.go_next, current_page_index, pages,
                                             main_menu_btn_frame, title_label,
                                             btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget))
    btn_main_menu.config(command=functools.partial(nav.go_main_menu, current_page_index, pages,
                                                   main_menu_btn_frame, title_label,
                                                   btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget))

    def on_toggle_theme():
        toggle_theme()
        apply_theme_to_widget(root)
        nav_frame.config(bg=g.current_theme["bg"],
                         highlightbackground=g.current_theme["border_color"])
        container.config(bg=g.current_theme["bg"],
                         highlightbackground=g.current_theme["border_color"])
        main_menu_btn_frame.config(bg=g.current_theme["bg"],
                                   highlightbackground=g.current_theme["border_color"])
        title_label.config(bg=g.current_theme["bg"], fg=g.current_theme["fg"])

        for btn in [btn_prev, btn_next, btn_main_menu, btn_toggle_theme]:
            btn.config(**btn_colors())

        for widget in main_menu_btn_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(**button_params)

    btn_toggle_theme.config(command=on_toggle_theme)

    # Main Menu Buttons
    tk.Button(main_menu_btn_frame, text="➕  TASKS MANAGEMENT",
              command=functools.partial(nav.show_page, 1, current_page_index, pages,
                                        main_menu_btn_frame, title_label,
                                        btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget),
              **button_params).pack(pady=5)

    tk.Button(main_menu_btn_frame, text="📊 SCHEDULE TASKS",
              command=functools.partial(nav.show_page, 2, current_page_index, pages,
                                        main_menu_btn_frame, title_label,
                                        btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget),
              **button_params).pack(pady=5)

    tk.Button(main_menu_btn_frame, text="📈 VIEW GRAPHS",
              command=functools.partial(nav.show_page, 3, current_page_index, pages,
                                        main_menu_btn_frame, title_label,
                                        btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget),
              **button_params).pack(pady=5)

    tk.Button(main_menu_btn_frame, text="📘 USER GUIDE",
              command=functools.partial(nav.show_page, 4, current_page_index, pages,
                                        main_menu_btn_frame, title_label,
                                        btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget),
              **button_params).pack(pady=5)

    tk.Button(main_menu_btn_frame, text="💾 GENERATE RESULTS REPORT",
              command=save_results_to_report, **button_params).pack(pady=5)

    tk.Button(main_menu_btn_frame, text="❌ Exit", command=root.quit,
              **button_params).pack(pady=10)

    # Keyboard navigation: pass all needed args using partial
    root.bind_all('<KeyPress>', lambda e: nav.on_key_press(
        e, current_page_index, pages,
        main_menu_btn_frame, title_label,
        btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget
    ))

    nav.show_page(0, current_page_index, pages, main_menu_btn_frame,
                  title_label, btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget)

    root.mainloop()
