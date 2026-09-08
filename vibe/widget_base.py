from __future__ import annotations

import tkinter as tk


class Widget:
    # subclass this to make your own component. implement build()
    def __init__(self):
        self.window = None
        self.tk_widget = None

    def build(self, container, theme):
        raise NotImplementedError("need to implement build(container, theme)")

    def on_theme_change(self, theme):
        pass

    def on_destroy(self):
        pass

    def _mount(self, window):
        self.window = window
        self.tk_widget = self.build(window._current().frame, window.theme_colors)
        if self.tk_widget is None:
            raise ValueError("build() has to return a widget, got None")
        self.tk_widget.bind("<Destroy>", lambda e: self.on_destroy(), add="+")
        window._register_theme_listener(lambda theme: self.on_theme_change(theme))
        return self.tk_widget
