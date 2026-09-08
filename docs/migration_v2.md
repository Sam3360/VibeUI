# Migrating from v2 to v3

v3 is additive for almost everything. Existing v2 code that avoided internal
attributes should keep working unchanged — the breaking changes are narrow
and listed below.

## Nothing changes for:

- `import vibe as vi`
- `Window(title, size, theme, accent, resizable, center)`
- `row()`, `column()`, `card()` (they gained new optional keyword args, all
  with backward-compatible defaults)
- `add_label`, `add_button` (`command=` still works alongside the newer
  `on_click=`), `add_input`, `add_textarea`, `add_checkbox`, `add_radio_group`,
  `add_slider`, `add_dropdown`, `add_listbox`, `add_progressbar`, `add_image`,
  `add_separator`, `add_spacer`, `tabs()`, `set_menu()`, `add_status_bar()`
- `alert`, `confirm`, `prompt`, `choose_file`, `choose_folder`, `save_file`,
  `pick_color`
- The `LICENSE`/author metadata

## Breaking changes

### `vi.toast(...)` gained a `type` parameter and changed its default duration

```python
# v2
vi.toast("Saved!", duration=2000, parent=win)

# v3 — same call still works; `type` is optional and defaults to "info"
vi.toast("Saved!", type="success", duration=3000, parent=win)
```
If you relied on the exact default duration (2000ms in v2, 3000ms in v3),
pass `duration=` explicitly.

### Theme color dict keys were renamed/expanded

If you read `win.theme_colors[...]` directly in v2 (rather than through
widget arguments), note the v3 token names are `background`/`surface`/`text`
instead of the shorter `bg`/`fg` v2 used internally. **Both still work** —
`bg` and `fg` are kept as aliases on every theme for exactly this reason —
but new code should prefer `background`/`surface`/`text` to match
`create_theme(...)`.

### Custom theme names must be unique across the process

`vi.create_theme(name=...)` registers into a shared registry (so
`win.set_theme("your-name")` can find it later). If you happen to reuse a
built-in name (`light`, `dark`, `ocean`), you'll overwrite it for the rest of
the program — pick a distinct name.

## New in v3 (opt-in, nothing to migrate)

- `grid()`, `sidebar()`, `navbar()`, `modal()`, `accordion()`
- `vi.State` and `value=` bindings
- `create_theme()` + `win.set_theme()` for runtime theme switching
- `add_switch`, `add_spinbox`, `add_search_input`, `add_table`, `add_link`,
  `add_badge`, `add_tooltip`, `add_icon_button`
- `.validate(...)` / `.is_valid()` on widgets, and `vi.Form` for grouping them
- `win.bind_shortcut(...)`, `win.maximize()/minimize()/fullscreen()/set_min_size()/set_max_size()`
- `win.debug_layout()`
- `vi.Widget` base class for custom components
- Clearer exceptions (`vi.InvalidValueError`, `vi.UnknownThemeError`, etc.)
  instead of raw Tkinter tracebacks for common mistakes

See `CHANGELOG.md` for the full list.
