# Layout

vibeUI never asks you to calculate pixel coordinates. Widgets flow into the
current **container**, and you switch containers with a `with` block.

## The default: vertical stacking

```python
win.add_label("First")
win.add_label("Second")   # appears below the first, automatically
```

## `row()` — left to right

```python
with win.row(gap=12, align="center"):
    win.add_button("Save")
    win.add_button("Cancel")
```

- `gap`: pixels between children (default 8).
- `align`: `"start"` (top), `"center"`, `"end"` (bottom), or `"stretch"`.
- `expand=True`: the row grows to fill leftover space in its parent (useful
  for a content area next to a fixed-width `sidebar()`).

## `column()` — top to bottom

Same options as `row()`. Rarely needed at the top level (that's already the
default), but useful to force a vertical stack *inside* a `row()`.

```python
with win.row():
    with win.column():
        win.add_label("Left column, line 1")
        win.add_label("Left column, line 2")
    win.add_label("Right side")
```

## `grid(columns=N)` — a responsive grid

```python
with win.grid(columns=3, gap=12):
    for i in range(9):
        with win.card():
            win.add_label(f"Card {i}")
```

Widgets fill left-to-right, wrapping to a new row every `columns` items.
Columns share space evenly and resize with the window.

## `card(title=..., padding=16)` — a visually grouped section

A bordered, surface-colored box. Great for settings sections, dashboard
tiles, or anything that should read as "one unit."

```python
with win.card(title="Preferences"):
    win.add_checkbox("Enable notifications")
    win.add_slider("Volume", 0, 100, default=60)
```

## `sidebar(width=200)` / `navbar(height=56)`

Fixed-size panels for app chrome:

```python
with win.navbar():
    win.add_heading("My App", level=3)

with win.row(expand=True):
    with win.sidebar(width=160):
        win.add_button("Dashboard")
        win.add_button("Settings")
    with win.column(expand=True):
        win.add_label("Main content")
```

## `modal(title=...)` — a blocking dialog window

```python
with win.modal("Confirm delete") as m:
    win.add_label("Are you sure? This can't be undone.")
    with win.row():
        win.add_button("Delete", variant="danger", on_click=m.close)
        win.add_button("Cancel", variant="secondary", on_click=m.close)
```

`with win.modal(...):` blocks until the modal is closed (via `m.close()`, the
window's close button, or your own logic) — the same way native dialogs do.

## `accordion(title, expanded=False)` — a collapsible section

```python
with win.accordion("Advanced settings"):
    win.add_checkbox("Enable experimental features")
```

## Nesting

Every container can be nested inside any other — a `row()` inside a `card()`
inside a `grid()` is perfectly normal. vibeUI keeps a stack internally so
`win.add_*` calls always land in whichever container you're currently inside.

## What "responsive" means here

Tkinter isn't a browser engine, so vibeUI's responsiveness is intentionally
scoped: `grid()` columns share space and resize with the window, `expand=True`
containers grow into available space, and cards/rows re-flow their children
naturally as the window resizes. It will not reflow a grid's *column count*
based on width (that's a deliberate simplicity trade-off) — pick a column
count that suits your window's expected size, or listen for `<Configure>`
yourself (see `examples/responsive_demo.py`) if you need that.
