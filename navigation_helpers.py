from operator import index


def show_page(index, current_page_index, pages, main_menu_btn_frame, title_label,
              btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget):
    index = max(0, min(index, len(pages) - 1))
    current_page_index[0] = index

    if index == 0:
        # Show main menu buttons and hide other pages
        main_menu_btn_frame.pack(pady=(5, 20))
        for p in pages[1:]:
            p.place_forget()
        title_label.config(text="Decision-Based Task Scheduler")
        btn_prev.config(state="disabled")
        btn_next.config(state="disabled")
        btn_main_menu.config(state="disabled")

    else:
        # Hide main menu buttons and show the selected page
        main_menu_btn_frame.pack_forget()
        for p in pages[1:]:
            p.place(relwidth=1, relheight=1)
            p.lower()

        pages[index].lift()

        # If it's the graphs page and has refresh_graph method, call it to update plots
        if index == 3 and hasattr(pages[index], 'refresh_graph'):
            pages[index].refresh_graph()
        # If it's the report page (last page) and has generate_graph method, call it
        elif index == len(pages) - 1 and hasattr(pages[index], 'generate_graph'):
            pages[index].generate_graph()

        titles = [
            "",  # index 0 is main menu
            "➕ Tasks Management",
            "📊 Schedule Tasks",
            "📈 View Graphs",
            "📘 User Guide",
            "📄 Generate Report"
        ]

        title_label.config(text=titles[index] if index < len(titles) else "")
        btn_prev.config(state="normal" if index > 1 else "disabled")
        btn_next.config(state="normal" if index < len(pages) - 1 else "disabled")
        btn_main_menu.config(state="normal")

    apply_theme_to_widget(root)


def go_prev(current_page_index, pages, main_menu_btn_frame, title_label,
            btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget):
    if current_page_index[0] > 1:
        show_page(current_page_index[0] - 1, current_page_index, pages, main_menu_btn_frame,
                  title_label, btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget)


def go_next(current_page_index, pages, main_menu_btn_frame, title_label,
            btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget):
    if 1 <= current_page_index[0] < len(pages) - 1:
        show_page(current_page_index[0] + 1, current_page_index, pages, main_menu_btn_frame,
                  title_label, btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget)


def go_main_menu(current_page_index, pages, main_menu_btn_frame, title_label,
                 btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget):
    show_page(0, current_page_index, pages, main_menu_btn_frame,
              title_label, btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget)


def on_key_press(event, current_page_index, pages,
                 main_menu_btn_frame, title_label,
                 btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget):
    # Check if Ctrl is pressed (event.state & 0x4 is Ctrl on most platforms)
    if event.state & 0x4:
        key = event.keysym.lower()

        if key == 'right':
            go_next(current_page_index, pages,
                    main_menu_btn_frame, title_label,
                    btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget)

        elif key == 'left':
            go_prev(current_page_index, pages,
                    main_menu_btn_frame, title_label,
                    btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget)

        elif key == 'm':
            go_main_menu(current_page_index, pages,
                         main_menu_btn_frame, title_label,
                         btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget)
    return "break"  # Prevent default behavior of the key press