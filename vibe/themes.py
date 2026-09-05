"""
Theme system for vibeUI.

Provides a few built-in color palettes and small helpers used to derive
hover/press shades for buttons, so widgets feel interactive without any
extra work from the person using the library.
"""

from __future__ import annotations


def _clamp(value: int) -> int:
    return max(0, min(255, value))


def _shade(hex_color: str, amount: int) -> str:
    """Lighten (positive amount) or darken (negative amount) a hex color."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = _clamp(r + amount), _clamp(g + amount), _clamp(b + amount)
    return f"#{r:02x}{g:02x}{b:02x}"


THEMES = {
    "light": {
        "bg": "#f5f6fa",
        "surface": "#ffffff",
        "fg": "#1e1e1e",
        "muted": "#6b7280",
        "border": "#d8dbe0",
        "accent": "#4f46e5",
        "accent_fg": "#ffffff",
        "danger": "#e5484d",
        "success": "#12b76a",
    },
    "dark": {
        "bg": "#1a1b1e",
        "surface": "#242528",
        "fg": "#f2f2f2",
        "muted": "#9aa0a6",
        "border": "#35363a",
        "accent": "#7c6cf5",
        "accent_fg": "#ffffff",
        "danger": "#ff6b6b",
        "success": "#2ecc71",
    },
    "ocean": {
        "bg": "#0f2436",
        "surface": "#153450",
        "fg": "#eaf4ff",
        "muted": "#8fb3d9",
        "border": "#25537a",
        "accent": "#00b4d8",
        "accent_fg": "#012a3a",
        "danger": "#ff6b6b",
        "success": "#4ade80",
    },
}

# Point sizes used by add_label(size=...), add_button(size=...), etc.
FONT_SIZES = {"sm": 10, "md": 12, "lg": 16, "xl": 22}


def get_theme(name: str, accent: str | None = None) -> dict:
    """Return a copy of a named theme's color palette, optionally overriding the accent color."""
    base = THEMES.get(name, THEMES["light"]).copy()
    if accent:
        base["accent"] = accent
    return base


def hover_color(hex_color: str) -> str:
    return _shade(hex_color, -18)


def press_color(hex_color: str) -> str:
    return _shade(hex_color, -32)
