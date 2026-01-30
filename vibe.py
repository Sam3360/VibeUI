"""
Vibe – A beginner-friendly, professional Python GUI library
Author: [Your Name]
License: MIT
"""

import tkinter as tk
from tkinter import simpledialog, messagebox

# =========================
# Window Class
# =========================
class Window:
    def __init__(self, title="Vibe Window", size=(400, 300), theme="light"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{size[0]}x{size[1]}")
        self.widgets = []
        self.theme = theme
        self._apply_theme()
    
    def _apply_theme(self):
        if self.theme == "dark":
            self.root.configure(bg="#2e2e2e")
            self.default_bg = "#2e2e2e"
            self.default_fg = "#ffffff"
        else:
            self.root.configure(bg="#f0f0f0")
            self.default_bg = "#f0f0f0"
            self.default_fg = "#000000"

    def add_label(self, text, pos=(0,0), font_size=12, fg=None, bg=None):
        lbl = tk.Label(self.root, text=text, font=("Arial", font_size),
                       fg=fg or self.default_fg, bg=bg or self.default_bg)
        lbl.place(x=pos[0], y=pos[1])
        self.widgets.append(lbl)
        return lbl

    def add_button(self, text, pos=(0,0), command=None, font_size=12, fg=None, bg=None):
        btn = tk.Button(self.root, text=text, command=command,
                        font=("Arial", font_size),
                        fg=fg or self.default_fg, bg=bg or "#c0c0c0")
        btn.place(x=pos[0], y=pos[1])
        self.widgets.append(btn)
        return btn

    def add_input(self, placeholder="", pos=(0,0), width=20, password=False):
        var = tk.StringVar()
        ent = tk.Entry(self.root, textvariable=var, width=width,
                       show="*" if password else "")
        ent.insert(0, placeholder)
        ent.place(x=pos[0], y=pos[1])
        self.widgets.append(ent)
        return var

    def add_textarea(self, pos=(0,0), size=(30,5)):
        txt = tk.Text(self.root, width=size[0], height=size[1])
        txt.place(x=pos[0], y=pos[1])
        self.widgets.append(txt)
        return txt

    def add_checkbox(self, text, pos=(0,0)):
        var = tk.BooleanVar()
        chk = tk.Checkbutton(self.root, text=text, variable=var,
                             bg=self.default_bg, fg=self.default_fg)
        chk.place(x=pos[0], y=pos[1])
        self.widgets.append(chk)
        return var

    def add_slider(self, text, pos=(0,0), min_val=0, max_val=100, orient="horizontal"):
        lbl = self.add_label(text, pos=(pos[0], pos[1]-20))
        var = tk.DoubleVar()
        slider = tk.Scale(self.root, from_=min_val, to=max_val, orient=orient,
                          variable=var, bg=self.default_bg, fg=self.default_fg)
        slider.place(x=pos[0], y=pos[1])
        self.widgets.append(slider)
        return var

    def run(self):
        self.root.mainloop()

# =========================
# Dialogs / Alerts
# =========================
def alert(message, title="Alert"):
    messagebox.showinfo(title, message)

def confirm(message, title="Confirm"):
    return messagebox.askyesno(title, message)

def prompt(message, title="Input"):
    return simpledialog.askstring(title, message)