# Building custom widgets

vibeUI covers a lot of ground, but you'll eventually want something it
doesn't have. Subclass `vi.Widget` instead of fighting the layout system from
outside:

```python
import tkinter as tk
import vibe as vi

class RatingStars(vi.Widget):
    def __init__(self, value=3, max_stars=5):
        super().__init__()
        self.value = value
        self.max_stars = max_stars
        self._star_labels = []

    def build(self, container, theme):
        frame = tk.Frame(container, bg=container["bg"])
        for i in range(self.max_stars):
            lbl = tk.Label(frame, text="★", font=("Segoe UI", 16),
                            fg=theme["accent"] if i < self.value else theme["border"],
                            bg=container["bg"], cursor="hand2")
            lbl.pack(side="left")
            lbl.bind("<Button-1>", lambda e, i=i: self._set_value(i + 1))
            self._star_labels.append(lbl)
        return frame

    def _set_value(self, value):
        self.value = value
        for i, lbl in enumerate(self._star_labels):
            lbl.config(fg=self.window.theme_colors["accent"] if i < value
                       else self.window.theme_colors["border"])

    def on_theme_change(self, theme):
        self._set_value(self.value)  # re-apply colors from the new theme


win = vi.Window("Custom Widget Demo")
win.add_widget(RatingStars(value=4))
win.run()
```

## Lifecycle

1. **`build(self, container, theme)`** — called once, when `win.add_widget(...)`
   mounts your widget. `container` is the Tk frame you should parent your
   widgets under. `theme` is the current theme's token dict. Return the single
   outermost Tk widget vibeUI should place in the layout.
2. **`on_theme_change(self, theme)`** *(optional)* — called whenever
   `win.set_theme(...)` runs. Re-apply colors here if your widget should
   follow theme changes.
3. **`on_destroy(self)`** *(optional)* — called when the underlying Tk widget
   is destroyed. Release timers, unsubscribe from `State`, etc. here.

## What you get automatically

- `self.window` — the owning `Window`, so you can call `self.window.add_button(...)`
  *inside* `build()` if you want to compose existing vibeUI widgets rather
  than raw Tkinter.
- `self.tk_widget` — the raw widget your `build()` returned, available after
  mounting.
- Placement — `win.add_widget(my_widget)` places the returned widget using
  the same layout rules (`row`/`column`/`grid`/etc.) as every built-in widget.

## Escape hatches, used carefully

Every vibeUI wrapper exposes `.widget` for the underlying Tkinter object, and
custom widgets get direct access to `container`/`theme` in `build()`. These
exist so you're never blocked — but reach for them only when a built-in
widget genuinely doesn't cover your case; anything you build directly won't
automatically pick up future vibeUI layout or theming improvements the way
built-in widgets do.
