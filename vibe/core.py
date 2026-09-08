from __future__ import annotations

import contextlib
import re
import tkinter as tk
from tkinter import ttk

from .themes import get_theme, hover_color, press_color, FONT_SIZES
from .state import State, bind_computed
from .icons import get_icon
from .errors import InvalidValueError
from .widgets import (
    TextInput, TextArea, Toggle, RadioGroup, Slider, Dropdown, ListBox,
    ProgressBar, Switch, Spinbox, SearchInput, TreeView,
)

GAP = 8
DEBUG_COLORS = ["#ff5d5d", "#5db8ff", "#5dff9c", "#ffd75d", "#c95dff"]


class _Container:
    def __init__(self, frame, direction, gap=GAP, align="start", columns=None, role="bg"):
        self.frame = frame
        self.direction = direction
        self.gap = gap
        self.align = align
        self.columns = columns
        self.next_index = 0
        self.role = role


class TabGroup:
    def __init__(self, win, notebook):
        self._win = win
        self._nb = notebook
        self._frames = {}

    def _get_or_make(self, name):
        if name not in self._frames:
            f = tk.Frame(self._nb, bg=self._win.theme_colors["surface"])
            self._nb.add(f, text=name)
            self._frames[name] = f
            self._win._track_frame(f, role="surface")
        return self._frames[name]

    @contextlib.contextmanager
    def tab(self, name):
        f = self._get_or_make(name)
        self._win._push_container(f, "vertical", role="surface")
        try:
            yield f
        finally:
            self._win._pop_container()


class Accordion:
    def __init__(self, header_btn, body_frame, expanded):
        self._header = header_btn
        self._body = body_frame
        self._expanded = expanded

    def toggle(self):
        self.set_expanded(not self._expanded)

    def set_expanded(self, val):
        self._expanded = val
        if val:
            self._body.pack(side="top", fill="x")
        else:
            self._body.pack_forget()

    @property
    def expanded(self):
        return self._expanded


class Window:
    def __init__(self, title="Vibe App", size=(500, 400), theme="light",
                 accent=None, resizable=True, center=True):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{size[0]}x{size[1]}")
        self.root.resizable(resizable, resizable)

        self.theme_name = theme
        self.theme_colors = get_theme(theme, accent)
        self._style = ttk.Style(self.root)
        self._theme_listeners = []
        self._all_frames = []
        self._debug_enabled = False
        self._debug_saved = {}
        self._shortcuts = {}

        self._apply_theme()

        self._body = tk.Frame(self.root, bg=self.theme_colors["bg"])
        self._body.pack(fill="both", expand=True, padx=16, pady=16)
        self._track_frame(self._body, role="bg")
        self._stack = [_Container(self._body, "vertical")]

        if center:
            self.center(size)

    def center(self, size=None):
        self.root.update_idletasks()
        w, h = size if size else (self.root.winfo_width(), self.root.winfo_height())
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = max((sw - w) // 2, 0)
        y = max((sh - h) // 2, 0)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def maximize(self):
        try:
            self.root.state("zoomed")
        except tk.TclError:
            try:
                self.root.attributes("-zoomed", True)
            except tk.TclError:
                w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
                self.root.geometry(f"{w}x{h}+0+0")

    def minimize(self):
        self.root.iconify()

    def fullscreen(self, enabled=True):
        self.root.attributes("-fullscreen", enabled)

    def set_min_size(self, w, h):
        self.root.minsize(w, h)

    def set_max_size(self, w, h):
        self.root.maxsize(w, h)

    def resizable(self, w=True, h=True):
        self.root.resizable(w, h)

    def _apply_theme(self):
        c = self.theme_colors
        self.root.configure(bg=c["bg"])
        s = self._style
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        s.configure("Vibe.TCombobox", fieldbackground=c["surface"], background=c["surface"], foreground=c["fg"])
        s.configure("Vibe.Horizontal.TProgressbar", troughcolor=c["border"], background=c["accent"])
        s.configure("Vibe.TNotebook", background=c["bg"], borderwidth=0)
        s.configure("Vibe.TNotebook.Tab", background=c["surface"], foreground=c["fg"], padding=(12, 6))
        s.map("Vibe.TNotebook.Tab", background=[("selected", c["accent"])], foreground=[("selected", c["accent_fg"])])
        s.configure("Vibe.Treeview", background=c["surface"], fieldbackground=c["surface"],
                    foreground=c["fg"], bordercolor=c["border"], borderwidth=0)
        s.configure("Vibe.Treeview.Heading", background=c["surface"], foreground=c["muted"])
        s.map("Vibe.Treeview", background=[("selected", c["accent"])], foreground=[("selected", c["accent_fg"])])

    def set_theme(self, name, accent=None):
        self.theme_name = name
        self.theme_colors = get_theme(name, accent)
        self._apply_theme()
        for frame, role in self._all_frames:
            try:
                frame.configure(bg=self.theme_colors["surface" if role == "surface" else "bg"])
            except tk.TclError:
                pass
        for fn in self._theme_listeners:
            fn(self.theme_colors)
        if self._debug_enabled:
            self._apply_debug_borders()

    def set_title(self, title):
        self.root.title(title)

    def set_icon(self, path):
        try:
            self.root.iconbitmap(path)
        except tk.TclError:
            try:
                img = tk.PhotoImage(file=path)
                self.root.iconphoto(True, img)
                self._icon_ref = img
            except tk.TclError:
                print(f"vibeUI: couldn't load icon '{path}', use .ico on windows or .png/.gif elsewhere")

    def on_close(self, cb):
        self.root.protocol("WM_DELETE_WINDOW", cb)

    def close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    def bind_shortcut(self, combo, cb):
        seq = self._parse_shortcut(combo)
        self.root.bind_all(seq, lambda e: cb())
        self._shortcuts[combo] = seq
        return seq

    @staticmethod
    def _parse_shortcut(combo):
        parts = [p.strip() for p in combo.split("+") if p.strip()]
        if not parts:
            raise InvalidValueError(widget="bind_shortcut", prop="combo", value=combo,
                                     expected="something like 'Ctrl+S' or 'Escape'")
        *mods_raw, key = parts
        mods = []
        for p in mods_raw:
            low = p.lower()
            if low == "ctrl":
                mods.append("Control")
            elif low == "shift":
                mods.append("Shift")
            elif low == "alt":
                mods.append("Alt")
            else:
                mods.append(p)
        special = {"escape": "Escape", "enter": "Return", "return": "Return", "tab": "Tab",
                   "space": "space", "delete": "Delete", "backspace": "BackSpace"}
        klow = key.lower()
        if klow in special:
            kname = special[klow]
        elif re.match(r"^[Ff](1[0-2]|[1-9])$", key):
            kname = key.upper()
        elif len(key) == 1:
            kname = key if mods and "Shift" in mods else key.lower()
        else:
            kname = key
        return "<" + "-".join(mods + [kname]) + ">"

    def _push_container(self, frame, direction, gap=None, align="start", columns=None, role="bg"):
        self._stack.append(_Container(frame, direction, gap or GAP, align, columns, role))

    def _pop_container(self):
        self._stack.pop()

    def _current(self):
        return self._stack[-1]

    def _track_frame(self, frame, role):
        depth = len(self._all_frames)
        self._all_frames.append((frame, role))
        if self._debug_enabled:
            self._apply_debug_border(frame, depth)

    def _register_theme_listener(self, fn):
        self._theme_listeners.append(fn)

    def _place(self, widget, fill_x=True):
        cur = self._current()
        gap = cur.gap
        if cur.direction == "horizontal":
            anchor = {"start": "n", "center": "center", "end": "s", "stretch": "n"}.get(cur.align, "n")
            widget.pack(side="left", padx=(0, gap), pady=gap // 2, anchor=anchor)
        elif cur.direction == "grid":
            cols = cur.columns or 1
            idx = cur.next_index
            cur.next_index += 1
            row, col = divmod(idx, cols)
            widget.grid(row=row, column=col, padx=gap // 2, pady=gap // 2, sticky="nsew")
        else:
            anchor = {"start": "w", "center": "center", "end": "e", "stretch": "w"}.get(cur.align, "w")
            fill = "both" if cur.align == "stretch" else ("x" if fill_x else "none")
            widget.pack(side="top", fill=fill, anchor=anchor, pady=gap // 2)
        return widget

    @contextlib.contextmanager
    def row(self, gap=GAP, align="start", expand=False):
        f = tk.Frame(self._current().frame, bg=self._current().frame["bg"])
        self._place(f, fill_x=expand)
        if expand:
            f.pack_configure(fill="both", expand=True)
        self._track_frame(f, role=self._current().role)
        self._push_container(f, "horizontal", gap=gap, align=align, role=self._current().role)
        try:
            yield f
        finally:
            self._pop_container()

    @contextlib.contextmanager
    def column(self, gap=GAP, align="start", expand=False):
        f = tk.Frame(self._current().frame, bg=self._current().frame["bg"])
        self._place(f, fill_x=expand)
        if expand:
            f.pack_configure(fill="both", expand=True)
        self._track_frame(f, role=self._current().role)
        self._push_container(f, "vertical", gap=gap, align=align, role=self._current().role)
        try:
            yield f
        finally:
            self._pop_container()

    @contextlib.contextmanager
    def grid(self, columns=2, gap=GAP, align="stretch"):
        f = tk.Frame(self._current().frame, bg=self._current().frame["bg"])
        self._place(f)
        for col in range(columns):
            f.columnconfigure(col, weight=1)
        self._track_frame(f, role=self._current().role)
        self._push_container(f, "grid", gap=gap, align=align, columns=columns, role=self._current().role)
        try:
            yield f
        finally:
            self._pop_container()

    @contextlib.contextmanager
    def card(self, title=None, padding=16, gap=GAP):
        c = self.theme_colors
        outer = tk.Frame(self._current().frame, bg=c["border"])
        self._place(outer)
        self._track_frame(outer, role="bg")
        inner = tk.Frame(outer, bg=c["surface"])
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        self._track_frame(inner, role="surface")
        pad = tk.Frame(inner, bg=c["surface"])
        pad.pack(fill="both", expand=True, padx=padding, pady=padding)
        self._track_frame(pad, role="surface")
        self._push_container(pad, "vertical", gap=gap, role="surface")
        try:
            if title:
                self.add_label(title, size="lg", bold=True)
            yield pad
        finally:
            self._pop_container()

    @contextlib.contextmanager
    def sidebar(self, width=200, gap=GAP):
        c = self.theme_colors
        f = tk.Frame(self._current().frame, bg=c["surface"], width=width)
        f.pack_propagate(False)
        if self._current().direction == "horizontal":
            f.pack(side="left", fill="y", padx=(0, self._current().gap))
        else:
            f.pack(side="left", fill="y")
        self._track_frame(f, role="surface")
        self._push_container(f, "vertical", gap=gap, role="surface")
        try:
            yield f
        finally:
            self._pop_container()

    @contextlib.contextmanager
    def navbar(self, height=56, gap=GAP, align="center"):
        c = self.theme_colors
        f = tk.Frame(self._current().frame, bg=c["surface"], height=height)
        f.pack_propagate(False)
        f.pack(side="top", fill="x", pady=(0, self._current().gap))
        self._track_frame(f, role="surface")
        self._push_container(f, "horizontal", gap=gap, align=align, role="surface")
        try:
            yield f
        finally:
            self._pop_container()

    @contextlib.contextmanager
    def modal(self, title="", size=(360, 220), closable=True):
        c = self.theme_colors
        top = tk.Toplevel(self.root, bg=c["bg"])
        top.title(title)
        top.geometry(f"{size[0]}x{size[1]}")
        top.transient(self.root)
        top.grab_set()
        body = tk.Frame(top, bg=c["bg"])
        body.pack(fill="both", expand=True, padx=16, pady=16)
        self._track_frame(body, role="bg")

        handle = _ModalHandle(top)
        if closable:
            top.protocol("WM_DELETE_WINDOW", handle.close)

        self._push_container(body, "vertical")
        try:
            if title:
                self.add_label(title, size="lg", bold=True)
            yield handle
        finally:
            self._pop_container()

        top.update_idletasks()
        self.root.wait_window(top)

    @contextlib.contextmanager
    def accordion(self, title, expanded=False, padding=12):
        c = self.theme_colors
        outer = tk.Frame(self._current().frame, bg=c["border"])
        self._place(outer)
        self._track_frame(outer, role="bg")
        inner = tk.Frame(outer, bg=c["surface"])
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        self._track_frame(inner, role="surface")

        state = {"open": expanded}
        body = tk.Frame(inner, bg=c["surface"])
        self._track_frame(body, role="surface")

        header = tk.Button(inner, bg=c["surface"], fg=c["fg"], relief="flat", bd=0,
                           anchor="w", padx=padding, pady=padding // 2, cursor="hand2",
                           font=(c.get("font_family", "Segoe UI"), FONT_SIZES["md"], "bold"))

        def label():
            return f"{'▾' if state['open'] else '▸'}  {title}"

        def toggle():
            state["open"] = not state["open"]
            header.config(text=label())
            if state["open"]:
                body.pack(side="top", fill="x", padx=padding, pady=(0, padding))
            else:
                body.pack_forget()

        header.config(text=label(), command=toggle)
        header.pack(side="top", fill="x")
        self._register_theme_listener(lambda t: header.config(bg=t["surface"], fg=t["fg"]))
        if state["open"]:
            body.pack(side="top", fill="x", padx=padding, pady=(0, padding))

        self._push_container(body, "vertical", role="surface")
        try:
            yield Accordion(header, body, expanded)
        finally:
            self._pop_container()

    def _font(self, size="md", bold=False):
        pt = FONT_SIZES.get(size, size if isinstance(size, int) else FONT_SIZES["md"])
        return (self.theme_colors.get("font_family", "Segoe UI"), pt, "bold" if bold else "normal")

    def add_label(self, text="", size="md", bold=False, color=None):
        c = self.theme_colors
        bg = self._current().frame["bg"]
        lbl = tk.Label(self._current().frame, font=self._font(size, bold),
                       fg=color or c["fg"], bg=bg, justify="left")
        if callable(text):
            bind_computed(lbl, text, lambda v: lbl.config(text=v))
        else:
            lbl.config(text=text)
        if color is None:
            self._register_theme_listener(lambda t: lbl.config(fg=t["fg"]))
        return self._place(lbl)

    def add_heading(self, text, level=1):
        size = {1: "xxl", 2: "xl", 3: "lg"}.get(level, "lg")
        return self.add_label(text, size=size, bold=True)

    def add_button(self, text, on_click=None, command=None, variant="primary", size="md", icon=None):
        c = self.theme_colors
        on_click = on_click or command
        container_bg = self._current().frame["bg"]

        def palette(t):
            return {
                "primary": (t["accent"], t["accent_fg"]),
                "secondary": (t["surface"], t["fg"]),
                "danger": (t["danger"], "#ffffff"),
                "ghost": (container_bg, t["accent"]),
            }.get(variant, (t["accent"], t["accent_fg"]))

        bg, fg = palette(c)
        text2 = f"{get_icon(icon)}  {text}".strip() if icon else text
        btn = tk.Button(self._current().frame, text=text2, command=on_click,
                        font=self._font(size, bold=True), bg=bg, fg=fg,
                        activeforeground=fg, relief="flat", bd=0, padx=16, pady=8,
                        cursor="hand2", highlightthickness=0)
        st = {"bg": bg}
        btn.config(activebackground=hover_color(bg))
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color(st["bg"])))
        btn.bind("<Leave>", lambda e: btn.config(bg=st["bg"]))
        btn.bind("<ButtonPress-1>", lambda e: btn.config(bg=press_color(st["bg"])))
        btn.bind("<ButtonRelease-1>", lambda e: btn.config(bg=hover_color(st["bg"])))

        def restyle(t):
            nbg, nfg = palette(t)
            st["bg"] = nbg
            btn.config(bg=nbg, fg=nfg, activeforeground=nfg, activebackground=hover_color(nbg))

        self._register_theme_listener(restyle)
        return self._place(btn, fill_x=False)

    def add_icon_button(self, icon, on_click=None, variant="ghost", size="md", tooltip=None):
        btn = self.add_button(get_icon(icon), on_click=on_click, variant=variant, size=size)
        if tooltip:
            self.add_tooltip(btn, tooltip)
        return btn

    def add_input(self, placeholder="", password=False, on_change=None, value=None):
        c = self.theme_colors
        entry = tk.Entry(self._current().frame, font=self._font("md"),
                         bg=c["surface"], fg=c["fg"], insertbackground=c["fg"],
                         relief="flat", highlightthickness=1,
                         highlightbackground=c["border"], highlightcolor=c["accent"])
        w = TextInput(entry, placeholder=placeholder, theme=c, password=password)
        w._error_container = self._current().frame
        if on_change:
            w.on_change(on_change)
        if isinstance(value, State):
            w.set(value.get())
            unsub = value.subscribe(lambda v: w.set(v) if w.get() != v else None)
            w.on_change(lambda v: value.set(v))
            entry.bind("<Destroy>", lambda e: unsub(), add="+")

        def restyle(t):
            w._theme = t
            entry.config(bg=t["surface"], fg=t["fg"], insertbackground=t["fg"],
                        highlightbackground=t["border"], highlightcolor=t["accent"])

        self._register_theme_listener(restyle)
        self._place(entry)
        return w

    def add_search_input(self, placeholder="Search...", on_search=None, debounce_ms=250):
        c = self.theme_colors
        entry = tk.Entry(self._current().frame, font=self._font("md"), bg=c["surface"], fg=c["fg"],
                         insertbackground=c["fg"], relief="flat", highlightthickness=1,
                         highlightbackground=c["border"], highlightcolor=c["accent"])
        w = SearchInput(entry, placeholder=placeholder, theme=c)
        w._error_container = self._current().frame
        if on_search:
            w.on_search(on_search, debounce_ms=debounce_ms)
        self._register_theme_listener(lambda t: entry.config(
            bg=t["surface"], fg=t["fg"], insertbackground=t["fg"],
            highlightbackground=t["border"], highlightcolor=t["accent"]))
        self._place(entry)
        return w

    def add_textarea(self, rows=5, placeholder=""):
        c = self.theme_colors
        txt = tk.Text(self._current().frame, height=rows, font=self._font("md"),
                      bg=c["surface"], fg=c["fg"], insertbackground=c["fg"],
                      relief="flat", highlightthickness=1,
                      highlightbackground=c["border"], highlightcolor=c["accent"],
                      wrap="word")
        if placeholder:
            txt.insert("1.0", placeholder)
            txt.config(fg=c["muted"])

            def fin(e):
                if txt.get("1.0", "end-1c") == placeholder:
                    txt.delete("1.0", tk.END)
                    txt.config(fg=c["fg"])

            def fout(e):
                if not txt.get("1.0", "end-1c"):
                    txt.insert("1.0", placeholder)
                    txt.config(fg=c["muted"])

            txt.bind("<FocusIn>", fin)
            txt.bind("<FocusOut>", fout)
        self._register_theme_listener(lambda t: txt.config(
            bg=t["surface"], fg=t["fg"], insertbackground=t["fg"],
            highlightbackground=t["border"], highlightcolor=t["accent"]))
        self._place(txt)
        return TextArea(txt)

    def add_checkbox(self, text, checked=False, on_change=None, value=None):
        c = self.theme_colors
        bg = self._current().frame["bg"]
        var = tk.BooleanVar(value=checked if value is None else bool(value.get()))
        chk = tk.Checkbutton(self._current().frame, text=text, variable=var,
                             bg=bg, fg=c["fg"], selectcolor=c["surface"],
                             activebackground=bg, activeforeground=c["fg"],
                             font=self._font("md"), cursor="hand2")
        self._place(chk, fill_x=False)
        w = Toggle(var, chk)
        if on_change:
            w.on_change(on_change)
        if isinstance(value, State):
            unsub = value.subscribe(lambda v: w.set(v) if w.get() != v else None)
            w.on_change(lambda v: value.set(v))
            chk.bind("<Destroy>", lambda e: unsub(), add="+")
        self._register_theme_listener(lambda t: chk.config(
            fg=t["fg"], selectcolor=t["surface"], activeforeground=t["fg"]))
        return w

    def add_switch(self, text="", checked=False, on_change=None, value=None):
        c = self.theme_colors
        bg = self._current().frame["bg"]
        var = tk.BooleanVar(value=checked if value is None else bool(value.get()))

        def glyph():
            return "🟢 ON " if var.get() else "⚪ OFF"

        row = tk.Frame(self._current().frame, bg=bg)
        self._place(row, fill_x=False)
        toggle_lbl = tk.Label(row, text=glyph(), font=self._font("sm", bold=True),
                              bg=bg, fg=c["fg"], cursor="hand2", padx=4)
        toggle_lbl.pack(side="left")
        if text:
            tk.Label(row, text=text, font=self._font("md"), bg=bg, fg=c["fg"]).pack(side="left", padx=(6, 0))

        def flip(e=None):
            var.set(not var.get())

        toggle_lbl.bind("<Button-1>", flip)

        def redraw(*a):
            toggle_lbl.config(text=glyph())

        var.trace_add("write", redraw)
        w = Switch(var, toggle_lbl)
        if on_change:
            w.on_change(on_change)
        if isinstance(value, State):
            unsub = value.subscribe(lambda v: w.set(v) if w.get() != v else None)
            w.on_change(lambda v: value.set(v))
            toggle_lbl.bind("<Destroy>", lambda e: unsub(), add="+")
        self._register_theme_listener(lambda t: toggle_lbl.config(bg=t["bg"], fg=t["fg"]))
        return w

    def add_radio_group(self, options, default=None, on_change=None):
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
            self._register_theme_listener(lambda t, w=rb: w.config(
                fg=t["fg"], selectcolor=t["surface"], activeforeground=t["fg"]))
            buttons.append(rb)
        w = RadioGroup(var, buttons)
        if on_change:
            w.on_change(on_change)
        return w

    def add_slider(self, label=None, min_val=0, max_val=100, default=None, on_change=None, value=None):
        if min_val >= max_val:
            raise InvalidValueError(widget="add_slider", prop="min_val/max_val",
                                     value=(min_val, max_val), expected="min_val < max_val")
        c = self.theme_colors
        if label:
            self.add_label(label, size="sm")
        initial = default if default is not None else min_val
        if isinstance(value, State):
            initial = value.get()
        var = tk.DoubleVar(value=initial)
        scale = tk.Scale(self._current().frame, from_=min_val, to=max_val, orient="horizontal",
                         variable=var, bg=self._current().frame["bg"], fg=c["fg"],
                         troughcolor=c["border"], highlightthickness=0,
                         activebackground=c["accent"], font=self._font("sm"), bd=0)
        self._place(scale)
        w = Slider(var, scale)
        if on_change:
            w.on_change(on_change)
        if isinstance(value, State):
            unsub = value.subscribe(lambda v: w.set(v) if w.get() != v else None)
            w.on_change(lambda v: value.set(v))
            scale.bind("<Destroy>", lambda e: unsub(), add="+")
        self._register_theme_listener(lambda t: scale.config(
            fg=t["fg"], troughcolor=t["border"], activebackground=t["accent"]))
        return w

    def add_spinbox(self, min_val=0, max_val=100, default=None, step=1, on_change=None):
        c = self.theme_colors
        is_float = isinstance(step, float) or isinstance(min_val, float) or isinstance(max_val, float)
        var = (tk.DoubleVar if is_float else tk.IntVar)(value=default if default is not None else min_val)
        box = tk.Spinbox(self._current().frame, from_=min_val, to=max_val, increment=step,
                         textvariable=var, font=self._font("md"), bg=c["surface"], fg=c["fg"],
                         relief="flat", highlightthickness=1, highlightbackground=c["border"],
                         highlightcolor=c["accent"], buttonbackground=c["surface"])
        self._place(box, fill_x=False)
        w = Spinbox(var, box, is_float)
        if on_change:
            w.on_change(on_change)
        self._register_theme_listener(lambda t: box.config(
            bg=t["surface"], fg=t["fg"], highlightbackground=t["border"],
            highlightcolor=t["accent"], buttonbackground=t["surface"]))
        return w

    def add_dropdown(self, options, default=None, on_change=None, value=None):
        options = list(options)
        initial = default or (options[0] if options else "")
        if isinstance(value, State):
            initial = value.get()
        var = tk.StringVar(value=initial)
        box = ttk.Combobox(self._current().frame, textvariable=var, values=options,
                           state="readonly", style="Vibe.TCombobox", font=self._font("md"))
        self._place(box, fill_x=False)
        w = Dropdown(var, box)
        if on_change:
            w.on_change(on_change)
        if isinstance(value, State):
            unsub = value.subscribe(lambda v: w.set(v) if w.get() != v else None)
            w.on_change(lambda v: value.set(v))
            box.bind("<Destroy>", lambda e: unsub(), add="+")
        return w

    add_combobox = add_dropdown

    def add_listbox(self, items, multiple=False, height=6):
        c = self.theme_colors
        items = list(items)
        lb = tk.Listbox(self._current().frame, height=height,
                        selectmode="extended" if multiple else "browse",
                        bg=c["surface"], fg=c["fg"], relief="flat",
                        highlightthickness=1, highlightbackground=c["border"],
                        selectbackground=c["accent"], selectforeground=c["accent_fg"],
                        font=self._font("md"))
        for it in items:
            lb.insert(tk.END, it)
        self._place(lb)
        self._register_theme_listener(lambda t: lb.config(
            bg=t["surface"], fg=t["fg"], highlightbackground=t["border"],
            selectbackground=t["accent"], selectforeground=t["accent_fg"]))
        return ListBox(lb, items)

    def add_table(self, columns, rows=None, height=8):
        columns = list(columns)
        tree = ttk.Treeview(self._current().frame, columns=columns, show="headings",
                            height=height, style="Vibe.Treeview")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="w")
        self._place(tree)
        w = TreeView(tree, columns)
        if rows:
            w.set_rows(rows)
        return w

    def add_progressbar(self, value=0, max_val=100):
        var = tk.DoubleVar(value=value)
        bar = ttk.Progressbar(self._current().frame, orient="horizontal", maximum=max_val,
                              variable=var, style="Vibe.Horizontal.TProgressbar")
        self._place(bar)
        return ProgressBar(var, bar)

    def add_image(self, path, width=None, height=None):
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
                print("vibeUI: pip install vibeUI[images] to resize images")
        lbl = tk.Label(self._current().frame, image=photo, bg=self._current().frame["bg"])
        lbl.image = photo
        return self._place(lbl, fill_x=False)

    def add_separator(self):
        vert = self._current().direction != "horizontal"
        sep = ttk.Separator(self._current().frame, orient="horizontal" if vert else "vertical")
        if vert:
            sep.pack(fill="x", pady=GAP)
        else:
            sep.pack(side="left", fill="y", padx=GAP)
        return sep

    def add_spacer(self, size=GAP):
        bg = self._current().frame["bg"]
        sp = tk.Frame(self._current().frame, bg=bg, width=size, height=size)
        sp.pack(side="left" if self._current().direction == "horizontal" else "top")
        return sp

    def add_link(self, text, url=None, on_click=None):
        c = self.theme_colors
        bg = self._current().frame["bg"]
        lbl = tk.Label(self._current().frame, text=text, font=self._font("md"),
                       fg=c["accent"], bg=bg, cursor="hand2")

        def click(e=None):
            if url:
                import webbrowser
                webbrowser.open(url)
            if on_click:
                on_click()

        lbl.bind("<Button-1>", click)
        self._register_theme_listener(lambda t: lbl.config(fg=t["accent"]))
        return self._place(lbl, fill_x=False)

    def add_badge(self, text, variant="info"):
        c = self.theme_colors
        key = {"info": "accent", "success": "success", "warning": "warning", "danger": "danger"}.get(variant, "accent")
        bg = c[key]
        lbl = tk.Label(self._current().frame, text=text, font=self._font("sm", bold=True),
                       fg="#ffffff", bg=bg, padx=8, pady=2)

        def restyle(t):
            lbl.config(bg=t[key])

        self._register_theme_listener(restyle)
        return self._place(lbl, fill_x=False)

    def add_tooltip(self, widget, text, delay_ms=500):
        st = {"after_id": None, "tip": None}

        def show():
            if st["tip"] is not None:
                return
            c = self.theme_colors
            x = widget.winfo_rootx() + 12
            y = widget.winfo_rooty() + widget.winfo_height() + 6
            tip = tk.Toplevel(self.root)
            tip.overrideredirect(True)
            tip.attributes("-topmost", True)
            tip.geometry(f"+{x}+{y}")
            tk.Label(tip, text=text, bg=c["surface"], fg=c["fg"], font=self._font("sm"),
                    padx=8, pady=4, relief="solid", bd=1).pack()
            st["tip"] = tip

        def schedule(e=None):
            st["after_id"] = widget.after(delay_ms, show)

        def cancel(e=None):
            if st["after_id"] is not None:
                widget.after_cancel(st["after_id"])
                st["after_id"] = None
            if st["tip"] is not None:
                st["tip"].destroy()
                st["tip"] = None

        widget.bind("<Enter>", schedule, add="+")
        widget.bind("<Leave>", cancel, add="+")
        widget.bind("<Destroy>", cancel, add="+")

    def add_widget(self, widget):
        tkw = widget._mount(self)
        return self._place(tkw)

    def tabs(self, names=None):
        nb = ttk.Notebook(self._current().frame, style="Vibe.TNotebook")
        self._place(nb)
        group = TabGroup(self, nb)
        for n in (names or []):
            group._get_or_make(n)
        return group

    def set_menu(self, structure):
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

    def add_status_bar(self, text=""):
        c = self.theme_colors
        bar = tk.Label(self.root, text=text, anchor="w", bg=c["surface"], fg=c["muted"],
                      font=self._font("sm"), padx=10, pady=4)
        bar.pack(side="bottom", fill="x")
        self._track_frame(bar, role="surface")

        def setter(new_text):
            bar.config(text=new_text)

        bar.set = setter
        self._register_theme_listener(lambda t: bar.config(fg=t["muted"]))
        return bar

    def _apply_debug_border(self, frame, depth):
        try:
            if frame not in self._debug_saved:
                self._debug_saved[frame] = (frame.cget("highlightthickness"), frame.cget("highlightbackground"))
            color = DEBUG_COLORS[depth % len(DEBUG_COLORS)]
            frame.configure(highlightthickness=1, highlightbackground=color)
        except tk.TclError:
            pass

    def _apply_debug_borders(self):
        for depth, (frame, role) in enumerate(self._all_frames):
            self._apply_debug_border(frame, depth)

    def _restore_debug_borders(self):
        for frame, (thickness, color) in self._debug_saved.items():
            try:
                frame.configure(highlightthickness=thickness, highlightbackground=color)
            except tk.TclError:
                pass
        self._debug_saved.clear()

    def enable_debug(self):
        self._debug_enabled = True
        self._apply_debug_borders()

    def disable_debug(self):
        self._debug_enabled = False
        self._restore_debug_borders()

    def debug_layout(self):
        self.disable_debug() if self._debug_enabled else self.enable_debug()


class _ModalHandle:
    def __init__(self, top):
        self.window = top

    def close(self):
        self.window.destroy()
