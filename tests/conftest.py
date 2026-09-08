# needs a display for tkinter. on linux without one: xvfb-run -a pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import vibe as vi


@pytest.fixture
def window():
    """A fresh Window per test, destroyed afterwards. No mainloop is run."""
    win = vi.Window("Test", size=(400, 400), theme="light", center=False)
    yield win
    if win.root.winfo_exists():
        win.root.destroy()


@pytest.fixture(autouse=True)
def _reset_active_theme_registry():
    """Prevent one test's custom `create_theme(...)` from leaking into another."""
    from vibe.themes import THEMES
    before = set(THEMES.keys())
    yield
    for name in set(THEMES.keys()) - before:
        del THEMES[name]
