def show_page(index, current_page_index, pages, main_menu_btn_frame, title_label,
              btn_prev, btn_next, btn_main_menu, root, apply_theme_to_widget):
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

    apply_theme_to_widget(root)


def go_prev(current_page_index, pages, *args, **kwargs):
    if current_page_index[0] > 1:
        show_page(current_page_index[0] - 1, current_page_index, pages, *args, **kwargs)


def go_next(current_page_index, pages, *args, **kwargs):
    if 1 <= current_page_index[0] < len(pages) - 1:
        show_page(current_page_index[0] + 1, current_page_index, pages, *args, **kwargs)


def go_main_menu(current_page_index, pages, *args, **kwargs):
    show_page(0, current_page_index, pages, *args, **kwargs)


def on_key_press(event, current_page_index, pages, show_page_func, go_prev_func, go_next_func, go_main_menu_func):
    if event.state & 0x4:  # Ctrl pressed
        if event.keysym == 'Right':
            go_next_func(current_page_index, pages)
        elif event.keysym == 'Left':
            go_prev_func(current_page_index, pages)
    elif event.keysym.lower() == 'm':
        go_main_menu_func(current_page_index, pages)
