import re
import tkinter as tk


class Validatable:
    _error_container = None
    _error_label = None

    def validate(self, *, required=False, min_length=None, max_length=None,
                 pattern=None, min_value=None, max_value=None, custom=None):
        self._rules = dict(required=required, min_length=min_length, max_length=max_length,
                            pattern=pattern, min_value=min_value, max_value=max_value, custom=custom)
        return self

    def check(self):
        rules = getattr(self, "_rules", None)
        if not rules:
            return []
        val = self.get()
        errs = []

        empty = val is None or val == "" or val is False
        if rules.get("required") and empty:
            errs.append("This field is required.")

        if isinstance(val, str) and val:
            if rules.get("min_length") is not None and len(val) < rules["min_length"]:
                errs.append(f"Must be at least {rules['min_length']} characters.")
            if rules.get("max_length") is not None and len(val) > rules["max_length"]:
                errs.append(f"Must be at most {rules['max_length']} characters.")
            if rules.get("pattern") and not re.match(rules["pattern"], val):
                errs.append("Doesn't match the required format.")

        if isinstance(val, (int, float)) and not isinstance(val, bool):
            if rules.get("min_value") is not None and val < rules["min_value"]:
                errs.append(f"Must be at least {rules['min_value']}.")
            if rules.get("max_value") is not None and val > rules["max_value"]:
                errs.append(f"Must be at most {rules['max_value']}.")

        if rules.get("custom"):
            res = rules["custom"](val)
            if isinstance(res, str):
                errs.append(res)
            elif res is False:
                errs.append("Invalid value.")

        return errs

    def is_valid(self):
        errs = self.check()
        self._set_error_state(bool(errs), errs[0] if errs else "")
        return not errs

    def _set_error_state(self, bad, msg=""):
        theme = getattr(self, "_theme", None) or {}
        danger = theme.get("danger", "#e5484d")
        border = theme.get("border", "#d8dbe0")
        accent = theme.get("accent", border)
        w = getattr(self, "_error_widget", None)
        if w is not None:
            try:
                w.config(highlightbackground=danger if bad else border,
                         highlightcolor=danger if bad else accent)
            except tk.TclError:
                pass
        if self._error_label is not None:
            self._error_label.destroy()
            self._error_label = None
        if bad and msg and self._error_container is not None:
            self._error_label = tk.Label(self._error_container, text=msg, fg=danger,
                                         bg=self._error_container["bg"],
                                         font=(theme.get("font_family", "Segoe UI"), 9), anchor="w")
            self._error_label.pack(side="top", fill="x", anchor="w", pady=(2, 0))


class TextInput(Validatable):
    def __init__(self, entry, placeholder="", theme=None, password=False):
        self._entry = entry
        self._error_widget = entry
        self._placeholder = placeholder
        self._theme = theme or {}
        self._password = password
        self._showing_placeholder = False

        if placeholder:
            self._show_placeholder()
            entry.bind("<FocusIn>", self._focus_in)
            entry.bind("<FocusOut>", self._focus_out)
        elif password:
            entry.config(show="*")

    def _show_placeholder(self):
        self._entry.config(show="")
        self._entry.delete(0, tk.END)
        self._entry.insert(0, self._placeholder)
        self._entry.config(fg=self._theme.get("muted", "#888888"))
        self._showing_placeholder = True

    def _focus_in(self, e=None):
        if self._showing_placeholder:
            self._entry.delete(0, tk.END)
            self._entry.config(fg=self._theme.get("fg", "#000000"))
            if self._password:
                self._entry.config(show="*")
            self._showing_placeholder = False

    def _focus_out(self, e=None):
        if not self._entry.get():
            self._show_placeholder()

    def get(self):
        return "" if self._showing_placeholder else self._entry.get()

    def set(self, val):
        self._showing_placeholder = False
        self._entry.config(fg=self._theme.get("fg", "#000000"))
        if self._password:
            self._entry.config(show="*")
        self._entry.delete(0, tk.END)
        self._entry.insert(0, val)

    def clear(self):
        self._entry.delete(0, tk.END)
        if self._placeholder:
            self._show_placeholder()

    def focus(self):
        self._entry.focus_set()

    def on_change(self, cb):
        self._entry.bind("<KeyRelease>", lambda e: cb(self.get()))

    @property
    def widget(self):
        return self._entry


class TextArea:
    def __init__(self, w):
        self._widget = w

    def get(self):
        return self._widget.get("1.0", "end-1c")

    def set(self, val):
        self._widget.delete("1.0", tk.END)
        self._widget.insert("1.0", val)

    def clear(self):
        self._widget.delete("1.0", tk.END)

    def on_change(self, cb):
        self._widget.bind("<KeyRelease>", lambda e: cb(self.get()))

    @property
    def widget(self):
        return self._widget


class Toggle:
    def __init__(self, var, w):
        self._var = var
        self._widget = w

    def get(self):
        return self._var.get()

    def set(self, val):
        self._var.set(bool(val))

    def on_change(self, cb):
        self._var.trace_add("write", lambda *a: cb(self.get()))

    @property
    def widget(self):
        return self._widget


class RadioGroup:
    def __init__(self, var, buttons):
        self._var = var
        self._buttons = buttons

    def get(self):
        return self._var.get()

    def set(self, val):
        self._var.set(val)

    def on_change(self, cb):
        self._var.trace_add("write", lambda *a: cb(self.get()))


class Slider:
    def __init__(self, var, w):
        self._var = var
        self._widget = w

    def get(self):
        return self._var.get()

    def set(self, val):
        self._var.set(val)

    def on_change(self, cb):
        self._widget.config(command=lambda v: cb(float(v)))

    @property
    def widget(self):
        return self._widget


class Dropdown:
    def __init__(self, var, w):
        self._var = var
        self._widget = w

    def get(self):
        return self._var.get()

    def set(self, val):
        self._var.set(val)

    def on_change(self, cb):
        self._widget.bind("<<ComboboxSelected>>", lambda e: cb(self.get()))

    @property
    def widget(self):
        return self._widget


class ListBox:
    def __init__(self, w, items):
        self._widget = w
        self._items = list(items)

    def get_selected(self):
        idxs = self._widget.curselection()
        return [self._items[i] for i in idxs]

    def set_items(self, items):
        self._items = list(items)
        self._widget.delete(0, tk.END)
        for it in self._items:
            self._widget.insert(tk.END, it)

    @property
    def widget(self):
        return self._widget


class ProgressBar:
    def __init__(self, var, w):
        self._var = var
        self._widget = w

    def set(self, val):
        self._var.set(val)

    def get(self):
        return self._var.get()

    @property
    def widget(self):
        return self._widget


class Switch(Validatable):
    def __init__(self, var, w):
        self._var = var
        self._widget = w
        self._error_widget = None
        self._theme = None

    def get(self):
        return self._var.get()

    def set(self, val):
        self._var.set(bool(val))

    def on_change(self, cb):
        self._var.trace_add("write", lambda *a: cb(self.get()))

    @property
    def widget(self):
        return self._widget


class Spinbox(Validatable):
    def __init__(self, var, w, is_float):
        self._var = var
        self._widget = w
        self._error_widget = w
        self._is_float = is_float
        self._theme = None

    def get(self):
        v = self._var.get()
        return v if self._is_float else int(v)

    def set(self, val):
        self._var.set(val)

    def on_change(self, cb):
        self._widget.config(command=lambda: cb(self.get()))
        self._widget.bind("<KeyRelease>", lambda e: cb(self.get()))

    @property
    def widget(self):
        return self._widget


class SearchInput(TextInput):
    def on_search(self, cb, debounce_ms=250):
        st = {"after_id": None}

        def fire():
            st["after_id"] = None
            cb(self.get())

        def on_key(e=None):
            if st["after_id"] is not None:
                self._entry.after_cancel(st["after_id"])
            st["after_id"] = self._entry.after(debounce_ms, fire)

        self._entry.bind("<KeyRelease>", on_key)


class TreeView:
    def __init__(self, w, columns):
        self._widget = w
        self._columns = list(columns)

    def set_rows(self, rows):
        self._widget.delete(*self._widget.get_children())
        for r in rows:
            self._widget.insert("", tk.END, values=list(r))

    def add_row(self, r):
        self._widget.insert("", tk.END, values=list(r))

    def get_selected(self):
        return [self._widget.item(i, "values") for i in self._widget.selection()]

    def clear(self):
        self._widget.delete(*self._widget.get_children())

    @property
    def widget(self):
        return self._widget
