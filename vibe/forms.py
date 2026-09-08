from __future__ import annotations


class Form:
    def __init__(self):
        self._fields = {}

    def add_field(self, name, widget, **rules):
        if rules:
            widget.validate(**rules)
        self._fields[name] = widget
        return widget

    def is_valid(self):
        ok = True
        for f in self._fields.values():
            if not f.is_valid():
                ok = False
        return ok

    @property
    def errors(self):
        out = {}
        for name, f in self._fields.items():
            e = f.check()
            if e:
                out[name] = e
        return out

    @property
    def values(self):
        return {name: f.get() for name, f in self._fields.items()}

    def reset(self):
        for f in self._fields.values():
            if hasattr(f, "clear"):
                f.clear()
