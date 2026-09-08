import pytest
from vibe.themes import get_theme, create_theme, list_themes
from vibe.errors import UnknownThemeError


def test_builtin_themes_exist():
    for name in ("light", "dark", "ocean"):
        theme = get_theme(name)
        assert theme["accent"]
        assert theme["background"]


def test_unknown_theme_raises_helpful_error():
    with pytest.raises(UnknownThemeError):
        get_theme("does-not-exist")


def test_create_theme_registers_and_is_usable():
    create_theme(name="cyber-test", background="#0b0b0f", surface="#15151c",
                 text="#ffffff", accent="#00ffcc")
    assert "cyber-test" in list_themes()
    theme = get_theme("cyber-test")
    assert theme["accent"] == "#00ffcc"
    # hover/pressed should be auto-derived since they weren't given explicitly.
    assert theme["hover"] != theme["accent"]


def test_get_theme_accent_override():
    theme = get_theme("light", accent="#ff0000")
    assert theme["accent"] == "#ff0000"


def test_set_theme_updates_window_colors(window):
    original_accent = window.theme_colors["accent"]
    window.set_theme("dark")
    assert window.theme_name == "dark"
    assert window.theme_colors["accent"] != original_accent


def test_set_theme_restyles_existing_button(window):
    btn = window.add_button("Click", variant="primary")
    light_bg = btn.cget("bg")
    window.set_theme("dark")
    window.root.update()
    assert btn.cget("bg") != light_bg


def test_set_theme_restyles_existing_frame_bg(window):
    with window.card(title="Card") as body:
        pass
    light_surface = body.cget("bg")
    window.set_theme("dark")
    window.root.update()
    assert body.cget("bg") != light_surface
