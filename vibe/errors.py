class VibeUIError(Exception):
    pass


class InvalidValueError(VibeUIError):
    def __init__(self, *, widget, prop, value, expected):
        self.widget = widget
        self.prop = prop
        self.value = value
        self.expected = expected
        msg = f"vibeUI: {widget}'s `{prop}` got {value!r}, that's not valid.\n  wanted: {expected}"
        super().__init__(msg)


class ValidationError(VibeUIError):
    pass


class UnknownThemeError(VibeUIError):
    def __init__(self, name, available):
        self.name = name
        self.available = available
        super().__init__(
            f"vibeUI: no theme called '{name}'. have: {', '.join(available)}\n"
            f"  make it first with vi.create_theme(name='{name}', ...)"
        )
