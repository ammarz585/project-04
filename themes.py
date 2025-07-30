import tkinter as tk
import globals as g

LIGHT_THEME = {
    "bg": "#F0FDF4",                   # Mint cream
    "fg": "#1B4332",                   # Deep green text
    "button_bg": "#2C7A7B",            # Teal
    "button_fg": "#FFFFFF",            # White text
    "button_active_bg": "#285E61",     # Darker teal on hover
    "button_active_fg": "#FFFFFF",
    "highlight": "#C6F6D5",            # Pale mint
    "menu_bg": "#E6FFFA",              # Soft aqua background
    "menu_fg": "#1B4332",              # Match text color
    "error_bg": "#FED7D7",             # Soft rose
    "error_fg": "#C53030",             # Rich red
    "info_bg": "#B2F5EA",              # Cool aqua
    "info_fg": "#234E52",              # Deep teal
    "border_color": "#A0AEC0"          # Muted gray-blue border
}
DARK_THEME = {
    "bg": "#121417",                   # Deep gray-black
    "fg": "#E0F2F1",                   # Pale mint-gray text
    "button_bg": "#00838F",            # Dark cyan
    "button_fg": "#E0F7FA",            # Soft light cyan text
    "button_active_bg": "#006064",     # Deeper cyan
    "button_active_fg": "#E0F7FA",
    "highlight": "#00ACC1",            # Bright cyan highlight
    "menu_bg": "#1F2933",              # Charcoal navy
    "menu_fg": "#B2EBF2",              # Light aqua
    "error_bg": "#B71C1C",             # Vivid red
    "error_fg": "#FFEBEE",             # Light pink text
    "info_bg": "#0288D1",              # Bright blue info
    "info_fg": "#E1F5FE",              # Frosty blue text
    "border_color": "#4DD0E1"          # Cyan-teal border
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
