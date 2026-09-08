from __future__ import annotations

import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, colorchooser

from .themes import get_theme

TOAST_COLORS = {
    "info": ("accent", "accent_fg"),
    "success": ("success", "#ffffff"),
    "warning": ("warning", "#1e1e1e"),
    "error": ("danger", "#ffffff"),
}

_active_toasts = {}


def alert(message, title="Alert"):
    messagebox.showinfo(title, message)


def confirm(message, title="Confirm"):
    return messagebox.askyesno(title, message)


def prompt(message, title="Input", password=False):
    if password:
        return simpledialog.askstring(title, message, show="*")
    return simpledialog.askstring(title, message)


def choose_file(title="Choose a file", filetypes=(("All files", "*.*"),)):
    path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    return path or None


def choose_folder(title="Choose a folder"):
    path = filedialog.askdirectory(title=title)
    return path or None


def save_file(title="Save file", default_ext="", filetypes=(("All files", "*.*"),)):
    path = filedialog.asksaveasfilename(title=title, defaultextension=default_ext, filetypes=filetypes)
    return path or None


def pick_color(default="#ffffff"):
    color = colorchooser.askcolor(color=default)
    return color[1]


def toast(message, duration=3000, type="info", parent=None):
    owner = parent.root if hasattr(parent, "root") else parent
    theme = parent.theme_colors if hasattr(parent, "theme_colors") else get_theme("dark")
    bg_key, fg_key = TOAST_COLORS.get(type, TOAST_COLORS["info"])
    bg = theme.get(bg_key, theme.get("accent", "#333333"))
    fg = theme.get(fg_key, fg_key)

    top = tk.Toplevel(owner) if owner else tk.Toplevel()
    top.overrideredirect(True)
    top.attributes("-topmost", True)

    icon = {"info": "ℹ", "success": "✔", "warning": "⚠", "error": "✕"}.get(type, "ℹ")
    tk.Label(top, text=f"{icon}  {message}", bg=bg, fg=fg, padx=16, pady=10,
             font=("Segoe UI", 10)).pack()
    top.update_idletasks()

    key = id(owner) if owner else "_screen_"
    stack = _active_toasts.setdefault(key, [])
    stack.append(top)

    def reposition():
        base_x = owner.winfo_x() + owner.winfo_width() if owner else top.winfo_screenwidth()
        base_y = owner.winfo_y() + owner.winfo_height() if owner else top.winfo_screenheight()
        y = base_y - 24
        for t in reversed(stack):
            if not t.winfo_exists():
                continue
            h = t.winfo_height()
            y -= h
            x = base_x - t.winfo_width() - 24
            t.geometry(f"+{x}+{y}")
            y -= 8

    reposition()

    def dismiss():
        if top in stack:
            stack.remove(top)
        if top.winfo_exists():
            top.destroy()
        reposition()

    top.after(duration, dismiss)
    return top
