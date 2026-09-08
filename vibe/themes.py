from __future__ import annotations

from .errors import UnknownThemeError

REQUIRED = [
    "background", "surface", "text", "muted", "border",
    "accent", "hover", "pressed", "disabled", "danger", "success", "warning",
]

DEFAULTS = {
    "radius": 6,
    "spacing": 8,
    "font_family": "Segoe UI",
}


def _build(name, **tokens):
    t = {**DEFAULTS, **tokens}
    t["name"] = name
    missing = [k for k in REQUIRED if k not in t]
    if missing:
        raise ValueError(f"theme '{name}' missing: {', '.join(missing)}")
    t.setdefault("bg", t["background"])
    t.setdefault("fg", t["text"])
    t.setdefault("accent_fg", t.get("accent_fg", "#ffffff"))
    return t


THEMES = {
    "light": _build(
        "light",
        background="#f5f6fa", surface="#ffffff", text="#1e1e1e", muted="#6b7280",
        border="#d8dbe0", accent="#4f46e5", hover="#4338ca", pressed="#3730a3",
        disabled="#c7cad1", danger="#e5484d", success="#12b76a", warning="#f59e0b",
        accent_fg="#ffffff",
    ),
    "dark": _build(
        "dark",
        background="#1a1b1e", surface="#242528", text="#f2f2f2", muted="#9aa0a6",
        border="#35363a", accent="#7c6cf5", hover="#6a5ae0", pressed="#5847c9",
        disabled="#44454a", danger="#ff6b6b", success="#2ecc71", warning="#fbbf24",
        accent_fg="#ffffff",
    ),
    "ocean": _build(
        "ocean",
        background="#0f2436", surface="#153450", text="#eaf4ff", muted="#8fb3d9",
        border="#25537a", accent="#00b4d8", hover="#00a1c2", pressed="#0090ac",
        disabled="#1e4a63", danger="#ff6b6b", success="#4ade80",
        warning="#fbbf24", accent_fg="#012a3a",
    ),
}

FONT_SIZES = {"sm": 10, "md": 12, "lg": 16, "xl": 22, "xxl": 30}


def _clamp(v):
    return max(0, min(255, v))


def _shade(hexcol, amt):
    hexcol = hexcol.lstrip("#")
    r, g, b = (int(hexcol[i:i+2], 16) for i in (0, 2, 4))
    return f"#{_clamp(r+amt):02x}{_clamp(g+amt):02x}{_clamp(b+amt):02x}"


def hover_color(hexcol):
    return _shade(hexcol, -18)


def press_color(hexcol):
    return _shade(hexcol, -32)


def create_theme(name, *, background, surface, text, accent, muted="#8a8f98",
                  border="#33343a", hover=None, pressed=None, disabled="#555555",
                  danger="#e5484d", success="#12b76a", warning="#f59e0b",
                  accent_fg="#ffffff", spacing=8, radius=6, font_family="Segoe UI"):
    # lets you register a new theme at runtime, then use it in Window(theme=name)
    theme = _build(
        name, background=background, surface=surface, text=text, muted=muted,
        border=border, accent=accent, hover=hover or _shade(accent, -18),
        pressed=pressed or _shade(accent, -32), disabled=disabled, danger=danger,
        success=success, warning=warning, accent_fg=accent_fg, spacing=spacing,
        radius=radius, font_family=font_family,
    )
    THEMES[name] = theme
    return theme


def get_theme(name, accent=None):
    if name not in THEMES:
        raise UnknownThemeError(name, sorted(THEMES.keys()))
    t = THEMES[name].copy()
    if accent:
        t["accent"] = accent
        t["hover"] = _shade(accent, -18)
        t["pressed"] = _shade(accent, -32)
    return t


def list_themes():
    return sorted(THEMES.keys())
