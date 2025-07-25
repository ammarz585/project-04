import tkinter as tk
import globals as g

LIGHT_THEME = {
    "bg": "#F9FAFF",                   # Very light blue-white
    "fg": "#2C3E50",                   # Slate/navy text
    "button_bg": "#7986CB",            # Lavender blue
    "button_fg": "#FFFFFF",            # White button text
    "button_active_bg": "#5C6BC0",     # Darker lavender on hover
    "button_active_fg": "#FFFFFF",
    "highlight": "#D1C4E9",            # Light purple highlight
    "menu_bg": "#ECEFF1",              # Cool light gray
    "menu_fg": "#2C3E50",
    "error_bg": "#FFCDD2",             # Soft pink
    "error_fg": "#C62828",             # Deep red
    "info_bg": "#BBDEFB",              # Light blue
    "info_fg": "#0D47A1",              # Navy blue
    "border_color": "#D6E4FF"          # Light blue-gray border
}

DARK_THEME = {
    "bg": "#1A1B27",                   # Rich indigo/black
    "fg": "#ECEFF1",                   # Light gray-blue text
    "button_bg": "#3949AB",            # Indigo button
    "button_fg": "#FFFFFF",            # White button text
    "button_active_bg": "#303F9F",     # Darker indigo on hover
    "button_active_fg": "#FFFFFF",
    "highlight": "#7C4DFF",            # Electric violet
    "menu_bg": "#2C2F3B",              # Dark blue-gray
    "menu_fg": "#BBDEFB",              # Light blue text
    "error_bg": "#B71C1C",             # Bold red
    "error_fg": "#FFCDD2",             # Light red text
    "info_bg": "#1565C0",              # Medium blue
    "info_fg": "#E3F2FD",              # Pale blue text
    "border_color": "#3F51B5"          # Visible indigo border
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
