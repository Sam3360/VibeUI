import tkinter as tk

import vibe as vi


class _Divider(vi.Widget):
    def __init__(self):
        super().__init__()
        self.theme_changes = []
        self.destroyed = False

    def build(self, container, theme):
        return tk.Frame(container, bg=theme["border"], height=2)

    def on_theme_change(self, theme):
        self.theme_changes.append(theme["name"])

    def on_destroy(self):
        self.destroyed = True


def test_custom_widget_mounts_and_returns_tk_widget(window):
    divider = _Divider()
    tk_widget = window.add_widget(divider)
    assert isinstance(tk_widget, tk.Frame)
    assert divider.tk_widget is tk_widget
    assert divider.window is window


def test_custom_widget_receives_theme_change(window):
    divider = _Divider()
    window.add_widget(divider)
    window.set_theme("dark")
    assert divider.theme_changes == ["dark"]


def test_custom_widget_on_destroy_called(window):
    divider = _Divider()
    tk_widget = window.add_widget(divider)
    tk_widget.destroy()
    window.root.update()
    assert divider.destroyed is True


def test_build_must_return_a_widget(window):
    class Broken(vi.Widget):
        def build(self, container, theme):
            return None

    import pytest
    with pytest.raises(ValueError):
        window.add_widget(Broken())
