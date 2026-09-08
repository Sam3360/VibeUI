import tkinter as tk

import pytest
import vibe as vi
from vibe.errors import InvalidValueError


def test_window_creates_and_has_theme(window):
    assert window.theme_name == "light"
    assert window.theme_colors["accent"]


def test_row_lays_out_children_horizontally(window):
    with window.row() as frame:
        a = window.add_button("A")
        b = window.add_button("B")
    assert a.pack_info()["side"] == "left"
    assert b.pack_info()["side"] == "left"
    assert a.master is frame
    assert b.master is frame


def test_column_lays_out_children_vertically(window):
    with window.column() as frame:
        a = window.add_label("A")
        b = window.add_label("B")
    assert a.pack_info()["side"] == "top"
    assert a.master is frame


def test_grid_places_widgets_in_rows_and_columns(window):
    with window.grid(columns=2):
        labels = [window.add_label(str(i)) for i in range(4)]
    positions = [(int(l.grid_info()["row"]), int(l.grid_info()["column"])) for l in labels]
    assert positions == [(0, 0), (0, 1), (1, 0), (1, 1)]


def test_card_creates_bordered_surface(window):
    with window.card(title="Settings") as body:
        lbl = window.add_label("inside")
    assert lbl.master is body
    assert body["bg"] == window.theme_colors["surface"]


def test_nested_row_in_column(window):
    with window.column():
        with window.row():
            window.add_button("X")
        window.add_label("below")
    # No exception means the container stack balanced correctly.
    assert len(window._stack) == 1


def test_sidebar_and_navbar_dont_crash(window):
    with window.navbar():
        window.add_label("Brand")
    with window.row():
        with window.sidebar(width=100):
            window.add_button("Home")
        with window.column():
            window.add_label("Content")
    assert len(window._stack) == 1


def test_accordion_starts_collapsed_by_default(window):
    with window.accordion("More") as acc:
        window.add_label("hidden")
    assert acc.expanded is False


def test_accordion_expanded_flag(window):
    with window.accordion("More", expanded=True) as acc:
        window.add_label("shown")
    assert acc.expanded is True


def test_slider_rejects_invalid_range(window):
    with pytest.raises(InvalidValueError):
        window.add_slider(min_val=10, max_val=5)


def test_bind_shortcut_parses_common_combos(window):
    assert window._parse_shortcut("Ctrl+S") == "<Control-s>"
    assert window._parse_shortcut("Ctrl+Shift+S") == "<Control-Shift-S>"
    assert window._parse_shortcut("Escape") == "<Escape>"
    assert window._parse_shortcut("Enter") == "<Return>"
    assert window._parse_shortcut("F1") == "<F1>"


def test_bind_shortcut_invokes_callback(window):
    calls = []
    window.bind_shortcut("Ctrl+S", lambda: calls.append(1))
    window.root.focus_force()
    window.root.update()
    window.root.event_generate("<Control-s>")
    window.root.update()
    assert calls == [1]


def test_center_does_not_raise(window):
    window.center((300, 300))


def test_set_min_max_size_do_not_raise(window):
    window.set_min_size(200, 200)
    window.set_max_size(800, 800)


def test_debug_layout_toggles_without_raising(window):
    window.add_label("x")
    window.debug_layout()
    assert window._debug_enabled is True
    window.debug_layout()
    assert window._debug_enabled is False
