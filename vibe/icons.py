ICONS = {
    "add": "➕", "remove": "➖", "close": "✕", "check": "✔", "cancel": "✕",
    "settings": "⚙", "search": "🔍", "save": "💾", "delete": "🗑", "edit": "✎",
    "home": "🏠", "menu": "☰", "back": "←", "forward": "→", "up": "↑", "down": "↓",
    "warning": "⚠", "info": "ℹ", "success": "✔", "error": "✕",
    "user": "👤", "lock": "🔒", "unlock": "🔓", "star": "★", "heart": "♥",
    "refresh": "↻", "download": "⬇", "upload": "⬆", "folder": "📁", "file": "📄",
    "chat": "💬", "mail": "✉", "calendar": "📅", "clock": "🕒", "link": "🔗",
}


def get_icon(name):
    if name in ICONS:
        return ICONS[name]
    print(f"vibeUI: no icon '{name}', have: {', '.join(sorted(ICONS))}")
    return ""


def register_icon(name, glyph):
    ICONS[name] = glyph
