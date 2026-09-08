from .core import Window, TabGroup, Accordion
from .state import State
from .forms import Form
from .widget_base import Widget
from .errors import VibeUIError, InvalidValueError, ValidationError, UnknownThemeError
from .themes import THEMES, create_theme, list_themes
from .icons import get_icon, register_icon, ICONS
from .dialogs import (
    alert, confirm, prompt, choose_file, choose_folder, save_file, pick_color, toast,
)

App = Window

__version__ = "3.0.0"

__all__ = [
    "Window", "App", "TabGroup", "Accordion",
    "State", "Form", "Widget",
    "VibeUIError", "InvalidValueError", "ValidationError", "UnknownThemeError",
    "THEMES", "create_theme", "list_themes",
    "get_icon", "register_icon", "ICONS",
    "alert", "confirm", "prompt",
    "choose_file", "choose_folder", "save_file", "pick_color", "toast",
    "__version__",
]
