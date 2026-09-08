# Themes

vibeUI ships three built-in themes — `light`, `dark`, `ocean` — and lets you
register your own with a set of design tokens.

## Using a built-in theme

```python
win = vi.Window("My App", theme="dark", accent="#7c6cf5")
```

`accent` is optional and overrides just the accent color of whichever theme
you picked, deriving matching hover/pressed shades automatically.

## Switching themes at runtime

```python
win.set_theme("ocean")
```

Every widget the window has created re-colors itself immediately — no
restart, no rebuild.

## Creating a custom theme

```python
vi.create_theme(
    name="cyber",
    background="#0b0b0f",
    surface="#15151c",
    text="#ffffff",
    accent="#00ffcc",
)

win.set_theme("cyber")
# or: win = vi.Window("My App", theme="cyber")
```

Required: `name`, `background`, `surface`, `text`, `accent`.
Optional (sensible defaults are derived if omitted): `muted`, `border`,
`hover`, `pressed`, `disabled`, `danger`, `success`, `warning`, `accent_fg`,
`spacing`, `radius`, `font_family`.

## Design tokens reference

| Token | Used for |
|---|---|
| `background` | The window's base background |
| `surface` | Cards, inputs, dropdowns, sidebars/navbars |
| `text` | Default text color |
| `muted` | Secondary/help text, status bar |
| `border` | Card borders, input outlines |
| `accent` | Primary buttons, links, focus outline |
| `hover` / `pressed` | Button interaction states (auto-derived if omitted) |
| `disabled` | Reserved for disabled-state styling |
| `danger` / `success` / `warning` | Badges, validation errors, notifications |
| `spacing` | Default gap used by layout containers |
| `radius` | Reserved for future canvas-rendered widgets — current widgets are flat rectangles, since native Tkinter widgets don't support real corner rounding |
| `font_family` | Default font family for text widgets |

## Notes on scope

vibeUI's theming re-colors every widget vibeUI created for you. If you reach
into `widget.widget` (the raw Tkinter object) and add your own child widgets
directly, those won't automatically follow theme changes — style them
yourself, or wrap them in a custom `vi.Widget` (see `docs/custom_widgets.md`)
and implement `on_theme_change`.
