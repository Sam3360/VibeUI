"""
vibeUI — a beginner-friendly, professional Python GUI library built on Tkinter.

    import vibe as vi

    win = vi.Window("My App", theme="dark")
    win.add_label("Hello, Vibe!", size="lg")
    win.add_button("Click me", on_click=lambda: vi.alert("Hi!"))
    win.run()

Author: Samarth Chugh (Sam3360)
License: MIT
"""

from .core import Window
from .dialogs import (
    alert, confirm, prompt, choose_file, choose_folder, save_file, pick_color, toast,
)
from .themes import THEMES

# Friendly alias for people who think in terms of "App" rather than "Window".
App = Window

__version__ = "2.0.0"

__all__ = [
    "Window", "App",
    "alert", "confirm", "prompt",
    "choose_file", "choose_folder", "save_file", "pick_color", "toast",
    "THEMES", "__version__",
]
