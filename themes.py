# themes.py
import tkinter as tk
LIGHT_THEME = {
    "bg": "#f5f5f5",
    "fg": "#000000",
    "button_bg": "#ffffff",
    "button_fg": "#000000",
    "highlight": "#d9d9d9"
}

DARK_THEME = {
    "bg": "#2e2e2e",
    "fg": "#ffffff",
    "button_bg": "#444444",
    "button_fg": "#ffffff",
    "highlight": "#5e5e5e"
}

import globals as g

def toggle_theme():
    if g.current_theme == LIGHT_THEME:
        g.current_theme = DARK_THEME
    else:
        g.current_theme = LIGHT_THEME

import globals as g

def apply_theme_to_widget(widget):
    # Set background color if possible
    try:
        widget.config(bg=g.current_theme["bg"])
    except tk.TclError:
        pass
    
    # Set foreground color if possible
    try:
        widget.config(fg=g.current_theme["fg"])
    except tk.TclError:
        pass

    # Special widget types that have different bg/fg options
    widget_class = widget.winfo_class()
    if widget_class in ("Button", "Label", "Radiobutton", "Checkbutton"):
        try:
            widget.config(bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"])
        except tk.TclError:
            pass
    elif widget_class in ("Entry", "Text", "Listbox"):
        # Entries, Text widgets may need different bg/fg
        try:
            widget.config(bg=g.current_theme["bg"], fg=g.current_theme["fg"],
                          insertbackground=g.current_theme["fg"])  # Cursor color
        except tk.TclError:
            pass
    elif widget_class == "TFrame":  # ttk.Frame (if using ttk)
        pass  # ttk widgets usually styled differently

    # Recurse for all child widgets
    for child in widget.winfo_children():
        apply_theme_to_widget(child)

