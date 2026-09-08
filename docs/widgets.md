# Widget reference

Every interactive widget below returns a small wrapper object. Wrappers give
you `.get()` / `.set()` (and `.on_change(callback)` where it makes sense)
instead of raw Tkinter `StringVar`/`BooleanVar`/`DoubleVar` objects. Reach the
underlying Tkinter widget with `.widget` if you ever need to.

| Method | Returns | Key options |
|---|---|---|
| `add_label(text, size, bold, color)` | `tk.Label` | `text` may be a callable bound to `State` |
| `add_heading(text, level)` | `tk.Label` | `level` 1 (largest) – 3 |
| `add_button(text, on_click, variant, size, icon)` | `tk.Button` | `variant`: primary/secondary/danger/ghost |
| `add_icon_button(icon, on_click, variant, tooltip)` | `tk.Button` | icon-only button |
| `add_input(placeholder, password, on_change, value)` | `TextInput` | `.get()/.set()/.clear()/.validate(...)` |
| `add_search_input(placeholder, on_search, debounce_ms)` | `SearchInput` | `.on_search(cb)` is debounced |
| `add_textarea(rows, placeholder)` | `TextArea` | `.get()/.set()/.clear()` |
| `add_checkbox(text, checked, on_change, value)` | `Toggle` | boolean `.get()/.set()` |
| `add_switch(text, checked, on_change, value)` | `Switch` | same shape as Toggle, drawn as an on/off pill |
| `add_radio_group(options, default, on_change)` | `RadioGroup` | `.get()/.set()` the selected option |
| `add_slider(label, min_val, max_val, default, on_change, value)` | `Slider` | numeric `.get()/.set()` |
| `add_spinbox(min_val, max_val, default, step, on_change)` | `Spinbox` | numeric, with up/down arrows |
| `add_dropdown` / `add_combobox(options, default, on_change, value)` | `Dropdown` | read-only select |
| `add_listbox(items, multiple, height)` | `ListBox` | `.get_selected()`, `.set_items(...)` |
| `add_table(columns, rows, height)` | `TreeView` | `.set_rows(...)`, `.get_selected()` |
| `add_progressbar(value, max_val)` | `ProgressBar` | `.set(value)` |
| `add_image(path, width, height)` | `tk.Label` | resizing needs `pip install vibeUI[images]` |
| `add_link(text, url, on_click)` | `tk.Label` | opens `url` in the browser if given |
| `add_badge(text, variant)` | `tk.Label` | variant: info/success/warning/danger |
| `add_separator()` | `ttk.Separator` | horizontal/vertical depending on container |
| `add_spacer(size)` | `tk.Frame` | blank space |
| `add_tooltip(widget, text, delay_ms)` | — | attach a hover tooltip to any returned widget |

## Containers / components

| Method | Notes |
|---|---|
| `row(gap, align, expand)` | left-to-right |
| `column(gap, align, expand)` | top-to-bottom |
| `grid(columns, gap, align)` | responsive grid |
| `card(title, padding, gap)` | bordered surface section |
| `sidebar(width)` | fixed-width vertical panel |
| `navbar(height)` | fixed-height horizontal bar |
| `modal(title, size, closable)` | blocking dialog window |
| `accordion(title, expanded)` | collapsible section |
| `tabs(names)` | `with tabs.tab("Name"):` |
| `set_menu({...})` | nested-dict menu bar |
| `add_status_bar(text)` | bottom status label with `.set(text)` |

## Dialogs (module-level, not on `Window`)

`vi.alert()`, `vi.confirm()`, `vi.prompt()`, `vi.choose_file()`,
`vi.choose_folder()`, `vi.save_file()`, `vi.pick_color()`, and
`vi.toast(message, type="info"|"success"|"warning"|"error", duration, parent)`.

## Validation

Any wrapper with `.validate(...)` (inputs, spinboxes, etc.) accepts:
`required`, `min_length`, `max_length`, `pattern` (regex), `min_value`,
`max_value`, `custom` (a function returning `True`, or an error string).
Call `.is_valid()` to check and show the error state, or `.check()` to just
get the list of messages without changing the widget's appearance.

See `docs/state.md` for `value=State(...)` bindings and `docs/custom_widgets.md`
for building your own widgets.
