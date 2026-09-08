from __future__ import annotations

# stack of sets - while a computed fn is running we track which State objs it reads
_collecting = []


class State:
    def __init__(self, initial=None):
        self._value = initial
        self._subs = []

    @property
    def value(self):
        if _collecting:
            _collecting[-1].add(self)
        return self._value

    @value.setter
    def value(self, v):
        self.set(v)

    def get(self):
        return self.value

    def set(self, v):
        if v == self._value:
            return
        self._value = v
        for cb in list(self._subs):
            cb(v)

    def subscribe(self, cb):
        self._subs.append(cb)

        def unsub():
            if cb in self._subs:
                self._subs.remove(cb)
        return unsub

    def __repr__(self):
        return f"State({self._value!r})"


def track(fn):
    deps = set()
    _collecting.append(deps)
    try:
        result = fn()
    finally:
        _collecting.pop()
    return result, deps


def bind_computed(widget, fn, apply):
    val, deps = track(fn)
    apply(val)

    def refresh(*_):
        new_val, _new_deps = track(fn)
        apply(new_val)

    unsubs = [d.subscribe(refresh) for d in deps]

    def cleanup(*_):
        for u in unsubs:
            u()

    widget.bind("<Destroy>", cleanup, add="+")
