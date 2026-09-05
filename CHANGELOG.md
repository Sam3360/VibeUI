# Changelog

## v2.0.0

Full rewrite. This is a breaking release — v1 code using `pos=(x, y)` will need
small updates (see below).

### Added
- Automatic flow layout: widgets stack top-to-bottom by default.
- `with win.row():` / `with win.column():` / `with win.card(title=...):` layout containers.
- Theming engine: `light`, `dark`, `ocean` built-in themes, plus custom `accent` color.
  Buttons now have real hover/press states.
- New widgets: radio groups, dropdowns, listboxes, progress bars, images, tabs,
  a menu bar (`set_menu`), and a status bar.
- New dialogs: `choose_file`, `choose_folder`, `save_file`, `pick_color`, `toast`.
- Every interactive widget now returns a small wrapper object with a consistent
  `.get()` / `.set()` (and `.on_change(callback)` where relevant) API, replacing
  raw `StringVar`/`BooleanVar`/`DoubleVar` access.
- Real placeholder text on inputs and text areas (not just pre-filled text).
- `Window.center()` on screen by default, `set_icon()`, `on_close()`, `App` alias for `Window`.
- Package reorganized into `vibe/core.py`, `vibe/widgets.py`, `vibe/themes.py`,
  `vibe/dialogs.py` (import path `import vibe as vi` is unchanged).

### Changed / Breaking
- **Removed `pos=(x, y)` absolute positioning.** Widgets now flow automatically;
  use `with win.row():` to place things side by side instead of manual coordinates.
- `add_button(..., command=...)` still works, but the new preferred keyword is `on_click=`.
- `Window(theme=...)` now also accepts an `accent=` color.

### Migration from v1
```python
# v1
win.add_label("Hi", pos=(50, 50))
win.add_button("Go", pos=(50, 100), command=go)

# v2
win.add_label("Hi")
win.add_button("Go", on_click=go)
```

## v1.0.0
- Initial release: `Window`, labels, buttons, inputs, text areas, checkboxes,
  sliders, and `alert`/`confirm`/`prompt` dialogs, using absolute `pos=(x, y)` placement.
