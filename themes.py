import tkinter as tk
import globals as g

LIGHT_THEME = {
    "bg": "#F0F4F3",
    "fg": "#000000",                 # Black text
    "button_bg": "#83B184",
    "button_fg": "#000000",          # Black button text
    "button_active_bg": "#5B875B",
    "button_active_fg": "#000000",   # Black active button text
    "highlight": "#A7D0A7",
    "menu_bg": "#D9EAD3",
    "menu_fg": "#000000",            # Black menu text
    "error_bg": "#FFD6D6",
    "error_fg": "#000000",           # Black error text
    "info_bg": "#D6E6FF",
    "info_fg": "#000000",            # Black info text
    "border_color": "#F0F4F3"        # Same as background (invisible)
}

DARK_THEME = {
    "bg": "#1B2B1B",
    "fg": "#260AF8",                 # Black text
    "button_bg": "#5B875B",
    "button_fg": "#000000",          # Black button text
    "button_active_bg": "#83B184",
    "button_active_fg": "#000000",   # Black active button text
    "highlight": "#A7D0A7",
    "menu_bg": "#102110",
    "menu_fg": "#000000",            # Black menu text
    "error_bg": "#7A0000",
    "error_fg": "#000000",           # Black error text
    "info_bg": "#003166",
    "info_fg": "#000000",            # Black info text
    "border_color": "#1B2B1B"        # Same as background (invisible)
}

def toggle_theme():
    if g.current_theme == LIGHT_THEME:
        g.current_theme = DARK_THEME
    else:
        g.current_theme = LIGHT_THEME

def apply_theme_to_widget(widget):
    try:
        widget.config(bg=g.current_theme["bg"])
    except tk.TclError:
        pass
    
    try:
        widget.config(fg=g.current_theme["fg"])
    except tk.TclError:
        pass

    widget_class = widget.winfo_class()

    if widget_class == "Button":
        try:
            widget.config(
                bg=g.current_theme["button_bg"],
                fg=g.current_theme["button_fg"],
                activebackground=g.current_theme.get("button_active_bg", g.current_theme["button_bg"]),
                activeforeground=g.current_theme.get("button_active_fg", g.current_theme["button_fg"])
            )
        except tk.TclError:
            pass
    elif widget_class in ("Label", "Radiobutton", "Checkbutton"):
        try:
            widget.config(bg=g.current_theme["bg"], fg=g.current_theme["fg"])
        except tk.TclError:
            pass
    elif widget_class in ("Entry", "Text", "Listbox", "Spinbox"):
        try:
            widget.config(
                bg=g.current_theme["bg"],
                fg=g.current_theme["fg"],
                insertbackground=g.current_theme["fg"]
            )
        except tk.TclError:
            pass

    for child in widget.winfo_children():
        apply_theme_to_widget(child)
