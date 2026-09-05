# vibeUI

**vibeUI** is a beginner-friendly, professional Python GUI library built on top of Tkinter.
It lets you build clean, modern-looking desktop apps with a handful of lines of code —
no manual pixel positioning, no wrestling with `StringVar`s, no theming headaches.

> **v2.0.0** is a from-the-ground-up rewrite. See [CHANGELOG.md](CHANGELOG.md) for what
> changed and why — the short version: a real layout system, a proper theming engine,
> way more widgets, and a much nicer developer experience.

---

## Features

- **Automatic layout** — widgets stack top-to-bottom by default; use `with win.row():` to
  go left-to-right, `with win.card():` to group things visually. No `pos=(x, y)` math.
- **Theming** — built-in `light`, `dark`, and `ocean` themes, plus a custom `accent` color.
  Buttons get real hover/press states out of the box.
- **A much bigger widget set** — labels, buttons (4 variants), text inputs (with real
  placeholders), text areas, checkboxes, radio groups, sliders, dropdowns, listboxes,
  progress bars, images, tabs, menus, and a status bar.
- **Consistent widget API** — every interactive widget returns a small wrapper with
  `.get()` / `.set()` (and `.on_change(callback)` where it makes sense) instead of raw
  Tkinter variables.
- **Dialogs** — `alert`, `confirm`, `prompt`, `choose_file`, `choose_folder`, `save_file`,
  `pick_color`, and a non-blocking `toast(...)` notification.
- **Cross-platform** — Windows, macOS, Linux (anywhere Tkinter runs).

---

## Installation

```bash
pip install vibeUI
```

Optional, for resizable images (`add_image(..., width=..., height=...)`):

```bash
pip install vibeUI[images]
```

---

## Quick Start

```python
import vibe as vi

win = vi.Window("Vibe Demo", size=(500, 400), theme="dark", accent="#7c6cf5")

win.add_label("Hello, Vibe!", size="xl", bold=True)
name = win.add_input("Enter your name")

def greet():
    vi.alert(f"Hello {name.get() or 'friend'}!", title="Greeting")

win.add_button("Greet Me", on_click=greet)
win.run()
```

Run the full feature tour:

```bash
python examples/demo.py
```

---

## Layout in v2

v1 used absolute positioning (`pos=(x, y)`). v2 uses a simple flow layout instead —
it's a deliberate breaking change that makes apps look right on every screen size
without any manual math.

```python
win = vi.Window("Layout demo")

win.add_label("Stacks vertically by default")

with win.row():                      # left-to-right group
    win.add_button("Yes")
    win.add_button("No")

with win.card(title="Settings"):     # bordered, visually grouped section
    win.add_checkbox("Enable notifications")
    win.add_slider("Volume", 0, 100, default=60)

win.run()
```

---

## Widget reference (short version)

| Method | Returns | Notes |
|---|---|---|
| `add_label(text, size, bold, color)` | — | `size`: `sm`/`md`/`lg`/`xl` |
| `add_button(text, on_click, variant, size)` | — | `variant`: `primary`/`secondary`/`danger`/`ghost` |
| `add_input(placeholder, password, on_change)` | `TextInput` | `.get()` / `.set()` / `.clear()` |
| `add_textarea(rows, placeholder)` | `TextArea` | `.get()` / `.set()` / `.clear()` |
| `add_checkbox(text, checked, on_change)` | `Toggle` | `.get()` / `.set()` bool |
| `add_radio_group(options, default, on_change)` | `RadioGroup` | `.get()` / `.set()` |
| `add_slider(label, min_val, max_val, default, on_change)` | `Slider` | `.get()` / `.set()` |
| `add_dropdown(options, default, on_change)` | `Dropdown` | `.get()` / `.set()` |
| `add_listbox(items, multiple)` | `ListBox` | `.get_selected()` |
| `add_progressbar(value, max_val)` | `ProgressBar` | `.set(value)` |
| `add_image(path, width, height)` | — | resizing needs Pillow |
| `tabs(names)` | `TabGroup` | `with tabs.tab("Name"):` |
| `set_menu({...})` | — | nested dict → menu bar |
| `add_status_bar(text)` | Label | `.set(text)` |

Dialogs: `vi.alert()`, `vi.confirm()`, `vi.prompt()`, `vi.choose_file()`,
`vi.choose_folder()`, `vi.save_file()`, `vi.pick_color()`, `vi.toast()`.

---

## License

vibeUI is released under the MIT License.

## Author

Created and maintained by **Samarth Chugh** ([@Sam3360](https://github.com/Sam3360)).
