"""
Widget wrapper classes for vibeUI.

Raw Tkinter makes you juggle StringVar / BooleanVar / DoubleVar and remember
which widget method reads which one. Every vibeUI widget instead returns one
of these small wrappers with a consistent `.get()` / `.set()` API.
"""

import tkinter as tk


class TextInput:
    """Wraps an Entry widget, with optional placeholder text and password masking."""

    def __init__(self, entry: tk.Entry, placeholder: str = "", theme: dict | None = None,
                 password: bool = False):
        self._entry = entry
        self._placeholder = placeholder
        self._theme = theme or {}
        self._password = password
        self._showing_placeholder = False

        if placeholder:
            self._show_placeholder()
            entry.bind("<FocusIn>", self._on_focus_in)
            entry.bind("<FocusOut>", self._on_focus_out)
        elif password:
            entry.config(show="*")

    def _show_placeholder(self):
        self._entry.config(show="")
        self._entry.delete(0, tk.END)
        self._entry.insert(0, self._placeholder)
        self._entry.config(fg=self._theme.get("muted", "#888888"))
        self._showing_placeholder = True

    def _on_focus_in(self, _event=None):
        if self._showing_placeholder:
            self._entry.delete(0, tk.END)
            self._entry.config(fg=self._theme.get("fg", "#000000"))
            if self._password:
                self._entry.config(show="*")
            self._showing_placeholder = False

    def _on_focus_out(self, _event=None):
        if not self._entry.get():
            self._show_placeholder()

    def get(self) -> str:
        return "" if self._showing_placeholder else self._entry.get()

    def set(self, value: str):
        self._showing_placeholder = False
        self._entry.config(fg=self._theme.get("fg", "#000000"))
        if self._password:
            self._entry.config(show="*")
        self._entry.delete(0, tk.END)
        self._entry.insert(0, value)

    def clear(self):
        self._entry.delete(0, tk.END)
        if self._placeholder:
            self._show_placeholder()

    def focus(self):
        self._entry.focus_set()

    def on_change(self, callback):
        self._entry.bind("<KeyRelease>", lambda _e: callback(self.get()))

    @property
    def widget(self):
        return self._entry


class TextArea:
    """Wraps a multi-line Text widget."""

    def __init__(self, text_widget: tk.Text):
        self._widget = text_widget

    def get(self) -> str:
        return self._widget.get("1.0", "end-1c")

    def set(self, value: str):
        self._widget.delete("1.0", tk.END)
        self._widget.insert("1.0", value)

    def clear(self):
        self._widget.delete("1.0", tk.END)

    def on_change(self, callback):
        self._widget.bind("<KeyRelease>", lambda _e: callback(self.get()))

    @property
    def widget(self):
        return self._widget


class Toggle:
    """Wraps a checkbox's BooleanVar."""

    def __init__(self, var: tk.BooleanVar, widget: tk.Checkbutton):
        self._var = var
        self._widget = widget

    def get(self) -> bool:
        return self._var.get()

    def set(self, value: bool):
        self._var.set(bool(value))

    def on_change(self, callback):
        self._var.trace_add("write", lambda *_args: callback(self.get()))

    @property
    def widget(self):
        return self._widget


class RadioGroup:
    """Wraps a group of Radiobuttons sharing one StringVar."""

    def __init__(self, var: tk.StringVar, buttons: list):
        self._var = var
        self._buttons = buttons

    def get(self) -> str:
        return self._var.get()

    def set(self, value: str):
        self._var.set(value)

    def on_change(self, callback):
        self._var.trace_add("write", lambda *_args: callback(self.get()))


class Slider:
    """Wraps a Scale widget's DoubleVar."""

    def __init__(self, var: tk.DoubleVar, widget: tk.Scale):
        self._var = var
        self._widget = widget

    def get(self) -> float:
        return self._var.get()

    def set(self, value: float):
        self._var.set(value)

    def on_change(self, callback):
        self._widget.config(command=lambda v: callback(float(v)))

    @property
    def widget(self):
        return self._widget


class Dropdown:
    """Wraps a ttk.Combobox."""

    def __init__(self, var: tk.StringVar, widget):
        self._var = var
        self._widget = widget

    def get(self) -> str:
        return self._var.get()

    def set(self, value: str):
        self._var.set(value)

    def on_change(self, callback):
        self._widget.bind("<<ComboboxSelected>>", lambda _e: callback(self.get()))

    @property
    def widget(self):
        return self._widget


class ListBox:
    """Wraps a Listbox and keeps track of the items shown, for easy selection lookup."""

    def __init__(self, widget: tk.Listbox, items):
        self._widget = widget
        self._items = list(items)

    def get_selected(self):
        indices = self._widget.curselection()
        return [self._items[i] for i in indices]

    def set_items(self, items):
        self._items = list(items)
        self._widget.delete(0, tk.END)
        for item in self._items:
            self._widget.insert(tk.END, item)

    @property
    def widget(self):
        return self._widget


class ProgressBar:
    """Wraps a ttk.Progressbar's DoubleVar."""

    def __init__(self, var: tk.DoubleVar, widget):
        self._var = var
        self._widget = widget

    def set(self, value: float):
        self._var.set(value)

    def get(self) -> float:
        return self._var.get()

    @property
    def widget(self):
        return self._widget
