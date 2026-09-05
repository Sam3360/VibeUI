"""
Popup dialogs: alerts, confirmations, prompts, file/folder/color pickers, and toasts.
"""

import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, colorchooser


def alert(message: str, title: str = "Alert"):
    messagebox.showinfo(title, message)


def confirm(message: str, title: str = "Confirm") -> bool:
    return messagebox.askyesno(title, message)


def prompt(message: str, title: str = "Input", password: bool = False):
    if password:
        return simpledialog.askstring(title, message, show="*")
    return simpledialog.askstring(title, message)


def choose_file(title: str = "Choose a file", filetypes=(("All files", "*.*"),)):
    path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    return path or None


def choose_folder(title: str = "Choose a folder"):
    path = filedialog.askdirectory(title=title)
    return path or None


def save_file(title: str = "Save file", default_ext: str = "", filetypes=(("All files", "*.*"),)):
    path = filedialog.asksaveasfilename(title=title, defaultextension=default_ext,
                                        filetypes=filetypes)
    return path or None


def pick_color(default: str = "#ffffff"):
    """Opens the system color picker. Returns a hex string, or None if cancelled."""
    color = colorchooser.askcolor(color=default)
    return color[1]


def toast(message: str, duration: int = 2000, parent=None):
    """A small, borderless notification near the bottom-right of `parent` that disappears on its own."""
    owner = parent.root if hasattr(parent, "root") else parent
    top = tk.Toplevel(owner) if owner else tk.Toplevel()
    top.overrideredirect(True)
    top.attributes("-topmost", True)

    label = tk.Label(top, text=message, bg="#242528", fg="#ffffff", padx=16, pady=10,
                     font=("Segoe UI", 10))
    label.pack()
    top.update_idletasks()

    if owner:
        owner.update_idletasks()
        x = owner.winfo_x() + owner.winfo_width() - top.winfo_width() - 24
        y = owner.winfo_y() + owner.winfo_height() - top.winfo_height() - 24
    else:
        x = top.winfo_screenwidth() - top.winfo_width() - 24
        y = top.winfo_screenheight() - top.winfo_height() - 80
    top.geometry(f"+{x}+{y}")
    top.after(duration, top.destroy)
    return top
