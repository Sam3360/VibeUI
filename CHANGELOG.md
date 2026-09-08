# Changelog

## v3.0.0

A major upgrade: from "make Tkinter modern" to "make building desktop
applications pleasant." Almost entirely additive — see Breaking below for
the short list of exceptions.

### Added — Layout
- `grid(columns=N)` — a responsive grid container.
- `gap`, `align` ("start"/"center"/"end"/"stretch"), and `expand` options on
  `row()` and `column()`.
- `sidebar(width)`, `navbar(height)`, `modal(title)`, `accordion(title)` —
  application-shell components built on the same container system.

### Added — Reactive state
- `vi.State`: an observable value box with `.get()/.set()/.value/.subscribe()`.
- `add_label(text=<callable>)` auto-tracks and re-renders on state change.
- `value=state` two-way binding on `add_input`, `add_checkbox`, `add_slider`,
  `add_dropdown`.

### Added — Theming
- Design-token theme system (`background`, `surface`, `text`, `muted`,
  `border`, `accent`, `hover`, `pressed`, `disabled`, `danger`, `success`,
  `warning`, `spacing`, `radius`, `font_family`).
- `vi.create_theme(name=..., ...)` to register custom themes.
- `win.set_theme(name)` — runtime theme switching; every existing widget
  re-colors itself immediately.

### Added — Widgets & components
- `add_switch`, `add_spinbox`, `add_search_input` (debounced), `add_table`
  (a simple `ttk.Treeview`-backed data grid), `add_link`, `add_badge`,
  `add_tooltip`, `add_icon_button`, `add_heading`.
- `icon=` support on `add_button`, backed by a dependency-free Unicode icon
  registry (`vi.get_icon` / `vi.register_icon`).
- `add_combobox` as an explicit alias for `add_dropdown`.

### Added — Forms & validation
- `.validate(required=, min_length=, max_length=, pattern=, min_value=,
  max_value=, custom=)` and `.is_valid()` / `.check()` on input-like widgets,
  with a visual error border and optional inline error message.
- `vi.Form` for aggregating fields: `.is_valid()`, `.errors`, `.values`, `.reset()`.

### Added — Window management & shortcuts
- `win.center()`, `win.maximize()`, `win.minimize()`, `win.fullscreen()`,
  `win.set_min_size()`, `win.set_max_size()`, `win.resizable()`.
- `win.bind_shortcut("Ctrl+S", callback)` with Ctrl/Shift/Alt, function keys,
  and common named keys (Escape, Enter, Tab, Space, Delete, Backspace).

### Added — Developer experience
- `win.debug_layout()` — outlines every layout container (off by default,
  zero cost unless called).
- `vi.Widget` — a documented base class for building custom components with
  theme-change and destroy lifecycle hooks (`docs/custom_widgets.md`).
- Custom exceptions (`vi.InvalidValueError`, `vi.UnknownThemeError`, etc.)
  replace confusing raw Tkinter tracebacks for common mistakes.
- Notifications: `vi.toast(message, type="info"|"success"|"warning"|"error")`,
  now non-blocking *and* stacking (multiple toasts no longer overlap).
- A real test suite (58 tests) covering layout, widgets, state, theming,
  forms, dialogs, and custom widgets.
- Twelve runnable examples in `examples/`: `hello_world`, `calculator`,
  `login`, `settings`, `todo`, `dashboard`, `form`, `file_manager`, `chat`,
  `theme_demo`, `responsive_demo`, `state_demo`.
- New docs: `docs/layout.md`, `docs/themes.md`, `docs/state.md`,
  `docs/widgets.md`, `docs/custom_widgets.md`, `docs/migration_v2.md`.

### Changed / Breaking
- `vi.toast()`'s default `duration` changed from 2000ms to 3000ms, and it
  gained a `type=` parameter. Existing calls still work; pass `duration=`
  explicitly if you relied on the old default.
- Internal theme dict keys were renamed to `background`/`surface`/`text`
  (from `bg`/`fg`); both old and new keys are present on every theme, so
  existing code reading `theme_colors["bg"]`/`["fg"]` still works.
- Custom theme names share one process-wide registry — reusing a built-in
  name (`light`/`dark`/`ocean`) overwrites it.

Full migration notes: [`docs/migration_v2.md`](docs/migration_v2.md).

### Known limitations
- `grid()`'s column *count* is fixed at creation time — it does not
  reflow based on window width (see `docs/layout.md` for the rationale and
  a `<Configure>`-based workaround).
- `radius` is a reserved design token; current widgets are flat rectangles,
  since native Tkinter widgets don't support real corner rounding without
  custom Canvas rendering.
- `maximize()` falls back gracefully but isn't guaranteed pixel-perfect on
  every Linux window manager.
- Accessibility support covers keyboard shortcuts, focus-visible native Tk
  widgets, and Tkinter's default tab order; there is no custom screen-reader
  layer.

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
