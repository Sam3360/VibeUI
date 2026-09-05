"""
Core Window and layout system for vibeUI.

vibeUI v2 replaces v1's absolute-positioning API (pos=(x, y)) with a simple
flow layout: widgets stack top-to-bottom automatically, and you group things
with `with win.row():`, `with win.column():`, or `with win.card():`.
"""

from __future__ import annotations

import contextlib
import tkinter as tk
from tkinter import ttk

from .themes import get_theme, hover_color, press_color, FONT_SIZES
from .widgets import (
    TextInput, TextArea, Toggle, RadioGroup, Slider, Dropdown, ListBox,
    ProgressBar,
)

SPACING = 8
FONT_FAMILY = "Segoe UI"


class _Container:
    """Internal bookkeeping for a layout container: a frame plus its stacking direction."""
    __slots__ = ("frame", "direction")

    def __init__(self, frame, direction):
        self.frame = frame
        self.direction = direction  # "vertical" or "horizontal"


class TabGroup:
    """Returned by Window.tabs(); use `with tabs.tab("Name"):` to fill a tab."""

    def __init__(self, window: "Window", notebook: ttk.Notebook):
        self._window = window
        self._notebook = notebook
        self._frames: dict[str, tk.Frame] = {}

    def _get_or_create(self, name: str) -> tk.Frame:
        if name not in self._frames:
            frame = tk.Frame(self._notebook, bg=self._window.theme_colors["surface"])
            self._notebook.add(frame, text=name)
            self._frames[name] = frame
        return self._frames[name]

    @contextlib.contextmanager
    def tab(self, name: str):
        frame = self._get_or_create(name)
        self._window._push_container(frame, "vertical")
        try:
            yield frame
        finally:
            self._window._pop_container()


class Window:
    """
    The main application window, and the entry point for building a vibeUI app.

    Example:
        win = Window("My App", theme="dark")
        win.add_label("Hello!", size="lg")
        win.add_button("Click me", on_click=lambda: print("clicked"))
        win.run()
    """

    def __init__(self, title: str = "Vibe App", size=(500, 400), theme: str = "light",
                 accent: str | None = None, resizable: bool = True, center: bool = True):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{size[0]}x{size[1]}")
        self.root.resizable(resizable, resizable)

        self.theme_name = theme
        self.theme_colors = get_theme(theme, accent)
        self._style = ttk.Style(self.root)
        self._apply_theme()

        self._body = tk.Frame(self.root, bg=self.theme_colors["bg"])
        self._body.pack(fill="both", expand=True, padx=16, pady=16)
        self._stack = [_Container(self._body, "vertical")]

        if center:
            self._center_on_screen(size)

    # ------------------------------------------------------------------
    # Window-level behaviour
    # ------------------------------------------------------------------
    def _center_on_screen(self, size):
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = max((screen_w - size[0]) // 2, 0)
        y = max((screen_h - size[1]) // 2, 0)
        self.root.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

    def _apply_theme(self):
        c = self.theme_colors
        self.root.configure(bg=c["bg"])
        style = self._style
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Vibe.TCombobox", fieldbackground=c["surface"],
                         background=c["surface"], foreground=c["fg"])
        style.configure("Vibe.Horizontal.TProgressbar",
                         troughcolor=c["border"], background=c["accent"])
        style.configure("Vibe.TNotebook", background=c["bg"], borderwidth=0)
        style.configure("Vibe.TNotebook.Tab", background=c["surface"], foreground=c["fg"],
                         padding=(12, 6))
        style.map("Vibe.TNotebook.Tab",
                   background=[("selected", c["accent"])],
                   foreground=[("selected", c["accent_fg"])])

    def set_title(self, title: str):
        self.root.title(title)

    def set_icon(self, path: str):
        """Set the window icon. Accepts .ico on Windows, or .png/.gif elsewhere."""
        try:
            self.root.iconbitmap(path)
        except tk.TclError:
            try:
                img = tk.PhotoImage(file=path)
                self.root.iconphoto(True, img)
                self._icon_ref = img  # keep a reference so Tk doesn't garbage-collect it
            except tk.TclError:
                print(f"vibeUI: couldn't load icon '{path}' "
                      "(use a .ico on Windows, or .png/.gif elsewhere)")

    def on_close(self, callback):
        """Run `callback` when the user tries to close the window (instead of closing immediately)."""
        self.root.protocol("WM_DELETE_WINDOW", callback)

    def close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    # ------------------------------------------------------------------
    # Layout containers
    # ------------------------------------------------------------------
    def _push_container(self, frame, direction):
        self._stack.append(_Container(frame, direction))

    def _pop_container(self):
        self._stack.pop()

    def _current(self) -> _Container:
        return self._stack[-1]

    def _place(self, widget, fill_x: bool = True, pad: int | None = None):
        cur = self._current()
        p = SPACING // 2 if pad is None else pad
        if cur.direction == "horizontal":
            widget.pack(side="left", padx=(0, SPACING), pady=p, anchor="n")
        else:
            widget.pack(side="top", fill="x" if fill_x else "none", anchor="w", pady=p)
        return widget

    @contextlib.contextmanager
    def row(self):
        """Group widgets added inside this block left-to-right instead of top-to-bottom."""
        frame = tk.Frame(self._current().frame, bg=self._current().frame["bg"])
        self._place(frame)
        self._push_container(frame, "horizontal")
        try:
            yield frame
        finally:
            self._pop_container()

    @contextlib.contextmanager
    def column(self):
        """Explicitly stack widgets top-to-bottom (useful nested inside a row())."""
        frame = tk.Frame(self._current().frame, bg=self._current().frame["bg"])
        self._place(frame)
        self._push_container(frame, "vertical")
        try:
            yield frame
        finally:
            self._pop_container()

    @contextlib.contextmanager
    def card(self, title: str | None = None, padding: int = 16):
        """A bordered, surface-colored container for visually grouping related widgets."""
        c = self.theme_colors
        outer = tk.Frame(self._current().frame, bg=c["border"])
        self._place(outer)
        inner = tk.Frame(outer, bg=c["surface"])
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        pad_frame = tk.Frame(inner, bg=c["surface"])
        pad_frame.pack(fill="both", expand=True, padx=padding, pady=padding)
        self._push_container(pad_frame, "vertical")
        try:
            if title:
                self.add_label(title, size="lg", bold=True)
            yield pad_frame
        finally:
            self._pop_container()

    # ------------------------------------------------------------------
    # Fonts
    # ------------------------------------------------------------------
    def _font(self, size="md", bold: bool = False):
        pt = FONT_SIZES.get(size, size if isinstance(size, int) else FONT_SIZES["md"])
        return (FONT_FAMILY, pt, "bold" if bold else "normal")

    # ------------------------------------------------------------------
    # Basic widgets
    # ------------------------------------------------------------------
    def add_label(self, text: str, size="md", bold: bool = False, color: str | None = None):
        c = self.theme_colors
        lbl = tk.Label(self._current().frame, text=text, font=self._font(size, bold),
                       fg=color or c["fg"], bg=self._current().frame["bg"], justify="left")
        return self._place(lbl)

    def add_button(self, text: str, on_click=None, command=None, variant: str = "primary",
                    size="md"):
        """variant: 'primary' | 'secondary' | 'danger' | 'ghost'."""
        c = self.theme_colors
        on_click = on_click or command
        palette = {
            "primary": (c["accent"], c["accent_fg"]),
            "secondary": (c["surface"], c["fg"]),
            "danger": (c["danger"], "#ffffff"),
            "ghost": (self._current().frame["bg"], c["accent"]),
        }
        bg, fg = palette.get(variant, palette["primary"])
        btn = tk.Button(self._current().frame, text=text, command=on_click,
                        font=self._font(size, bold=True), bg=bg, fg=fg,
                        activeforeground=fg, relief="flat", bd=0, padx=16, pady=8,
                        cursor="hand2", highlightthickness=0)
        hover, press = hover_color(bg), press_color(bg)
        btn.config(activebackground=hover)
        btn.bind("<Enter>", lambda _e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda _e: btn.config(bg=bg))
        btn.bind("<ButtonPress-1>", lambda _e: btn.config(bg=press))
        btn.bind("<ButtonRelease-1>", lambda _e: btn.config(bg=hover))
        return self._place(btn, fill_x=False)

    def add_input(self, placeholder: str = "", password: bool = False, on_change=None):
        c = self.theme_colors
        entry = tk.Entry(self._current().frame, font=self._font("md"),
                         bg=c["surface"], fg=c["fg"], insertbackground=c["fg"],
                         relief="flat", highlightthickness=1,
                         highlightbackground=c["border"], highlightcolor=c["accent"])
        wrapper = TextInput(entry, placeholder=placeholder, theme=c, password=password)
        if on_change:
            wrapper.on_change(on_change)
        self._place(entry)
        return wrapper

    def add_textarea(self, rows: int = 5, placeholder: str = ""):
        c = self.theme_colors
        txt = tk.Text(self._current().frame, height=rows, font=self._font("md"),
                      bg=c["surface"], fg=c["fg"], insertbackground=c["fg"],
                      relief="flat", highlightthickness=1,
                      highlightbackground=c["border"], highlightcolor=c["accent"],
                      wrap="word")
        if placeholder:
            txt.insert("1.0", placeholder)
            txt.config(fg=c["muted"])

            def _focus_in(_e):
                if txt.get("1.0", "end-1c") == placeholder:
                    txt.delete("1.0", tk.END)
                    txt.config(fg=c["fg"])

            def _focus_out(_e):
                if not txt.get("1.0", "end-1c"):
                    txt.insert("1.0", placeholder)
                    txt.config(fg=c["muted"])

            txt.bind("<FocusIn>", _focus_in)
            txt.bind("<FocusOut>", _focus_out)
        self._place(txt)
        return TextArea(txt)

    def add_checkbox(self, text: str, checked: bool = False, on_change=None):
        c = self.theme_colors
        var = tk.BooleanVar(value=checked)
        bg = self._current().frame["bg"]
        chk = tk.Checkbutton(self._current().frame, text=text, variable=var,
                             bg=bg, fg=c["fg"], selectcolor=c["surface"],
                             activebackground=bg, activeforeground=c["fg"],
                             font=self._font("md"), cursor="hand2")
        self._place(chk, fill_x=False)
        wrapper = Toggle(var, chk)
        if on_change:
            wrapper.on_change(on_change)
        return wrapper

    def add_radio_group(self, options, default: str | None = None, on_change=None):
        c = self.theme_colors
        bg = self._current().frame["bg"]
        var = tk.StringVar(value=default or (options[0] if options else ""))
        buttons = []
        for opt in options:
            rb = tk.Radiobutton(self._current().frame, text=opt, variable=var, value=opt,
                                bg=bg, fg=c["fg"], selectcolor=c["surface"],
                                activebackground=bg, activeforeground=c["fg"],
                                font=self._font("md"), cursor="hand2")
            self._place(rb, fill_x=False)
            buttons.append(rb)
        wrapper = RadioGroup(var, buttons)
        if on_change:
            wrapper.on_change(on_change)
        return wrapper

    def add_slider(self, label: str | None = None, min_val=0, max_val=100,
                    default=None, on_change=None):
        if min_val >= max_val:
            raise ValueError("vibeUI: add_slider needs min_val < max_val")
        c = self.theme_colors
        if label:
            self.add_label(label, size="sm")
        var = tk.DoubleVar(value=default if default is not None else min_val)
        scale = tk.Scale(self._current().frame, from_=min_val, to=max_val, orient="horizontal",
                         variable=var, bg=self._current().frame["bg"], fg=c["fg"],
                         troughcolor=c["border"], highlightthickness=0,
                         activebackground=c["accent"], font=self._font("sm"), bd=0)
        self._place(scale)
        wrapper = Slider(var, scale)
        if on_change:
            wrapper.on_change(on_change)
        return wrapper

    def add_dropdown(self, options, default: str | None = None, on_change=None):
        options = list(options)
        var = tk.StringVar(value=default or (options[0] if options else ""))
        box = ttk.Combobox(self._current().frame, textvariable=var, values=options,
                           state="readonly", style="Vibe.TCombobox", font=self._font("md"))
        self._place(box, fill_x=False)
        wrapper = Dropdown(var, box)
        if on_change:
            wrapper.on_change(on_change)
        return wrapper

    def add_listbox(self, items, multiple: bool = False, height: int = 6):
        c = self.theme_colors
        items = list(items)
        listbox = tk.Listbox(self._current().frame, height=height,
                             selectmode="extended" if multiple else "browse",
                             bg=c["surface"], fg=c["fg"], relief="flat",
                             highlightthickness=1, highlightbackground=c["border"],
                             selectbackground=c["accent"], selectforeground=c["accent_fg"],
                             font=self._font("md"))
        for item in items:
            listbox.insert(tk.END, item)
        self._place(listbox)
        return ListBox(listbox, items)

    def add_progressbar(self, value: float = 0, max_val: float = 100):
        var = tk.DoubleVar(value=value)
        bar = ttk.Progressbar(self._current().frame, orient="horizontal", maximum=max_val,
                              variable=var, style="Vibe.Horizontal.TProgressbar")
        self._place(bar)
        return ProgressBar(var, bar)

    def add_image(self, path: str, width: int | None = None, height: int | None = None):
        """Displays an image. Install Pillow (`pip install pillow`) for resizing and JPEG support."""
        photo = None
        try:
            from PIL import Image, ImageTk
            img = Image.open(path)
            if width or height:
                img = img.resize((width or img.width, height or img.height))
            photo = ImageTk.PhotoImage(img)
        except ImportError:
            photo = tk.PhotoImage(file=path)
            if width or height:
                print("vibeUI: install Pillow (`pip install pillow`) to resize images")
        lbl = tk.Label(self._current().frame, image=photo, bg=self._current().frame["bg"])
        lbl.image = photo  # keep a reference alive so Tk doesn't garbage-collect it
        return self._place(lbl, fill_x=False)

    def add_separator(self):
        vertical_layout = self._current().direction == "vertical"
        sep = ttk.Separator(self._current().frame, orient="horizontal" if vertical_layout else "vertical")
        if vertical_layout:
            sep.pack(fill="x", pady=SPACING)
        else:
            sep.pack(side="left", fill="y", padx=SPACING)
        return sep

    def add_spacer(self, size: int = SPACING):
        bg = self._current().frame["bg"]
        spacer = tk.Frame(self._current().frame, bg=bg, width=size, height=size)
        spacer.pack(side="left" if self._current().direction == "horizontal" else "top")
        return spacer

    # ------------------------------------------------------------------
    # Tabs, menus, status bar
    # ------------------------------------------------------------------
    def tabs(self, names=None) -> TabGroup:
        notebook = ttk.Notebook(self._current().frame, style="Vibe.TNotebook")
        self._place(notebook)
        group = TabGroup(self, notebook)
        for name in (names or []):
            group._get_or_create(name)
        return group

    def set_menu(self, structure: dict):
        """
        Build a menu bar from a nested dict, e.g.:
            win.set_menu({
                "File": {"New": new_fn, "Open": open_fn, "-": None, "Exit": win.close},
                "Help": {"About": about_fn},
            })
        Use "-" (or a value of None) for a separator.
        """
        menubar = tk.Menu(self.root)
        for menu_name, items in structure.items():
            menu = tk.Menu(menubar, tearoff=0)
            for label, action in items.items():
                if label == "-" or action is None:
                    menu.add_separator()
                else:
                    menu.add_command(label=label, command=action)
            menubar.add_cascade(label=menu_name, menu=menu)
        self.root.config(menu=menubar)

    def add_status_bar(self, text: str = ""):
        c = self.theme_colors
        bar = tk.Label(self.root, text=text, anchor="w", bg=c["surface"], fg=c["muted"],
                      font=self._font("sm"), padx=10, pady=4)
        bar.pack(side="bottom", fill="x")

        def _set(new_text: str):
            bar.config(text=new_text)

        bar.set = _set  # small convenience so you can call bar.set("...") later
        return bar
