# vibeUI

vibeUI is a python gui lib built on top of tkinter, made to actually be easy to use.

v1 was just some helper functions. v2 added a real layout system and theming. v3 (this one) adds reactive state, a bigger widget set, forms/validation, custom themes you can switch at runtime, and a bunch of other stuff. basically trying to make it feel less like "raw tkinter" and more like an actual framework.

```python
import vibe as vi

win = vi.Window("My App", theme="dark", accent="#7c6cf5")

name = vi.State("world")
win.add_label(text=lambda: f"Hello, {name.value}!", size="xl", bold=True)
win.add_input(value=name)

with win.row():
    win.add_button("Say hi", on_click=lambda: vi.alert(f"Hi {name.value}!"))
    win.add_button("Reset", variant="secondary", on_click=lambda: name.set("world"))

win.run()
```

## install

```
pip install vibeUI
```

if you want image resizing (needs Pillow):
```
pip install vibeUI[images]
```

tkinter should already be installed with python. on some linux distros you might need `sudo apt install python3-tk`.

## quick start

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

check the `examples/` folder, theres a bunch: hello_world, calculator, login, settings, todo, dashboard, form, file_manager, chat, theme_demo, responsive_demo, state_demo. just run any of them with `python examples/whatever.py`

## layout

widgets stack top to bottom by default. use `row()`, `column()`, `grid()`, `card()`, `sidebar()`, `navbar()`, `modal()`, `accordion()` to group stuff.

```python
with win.row(gap=12, align="center"):
    win.add_button("Save")
    win.add_button("Cancel")

with win.grid(columns=3, gap=12):
    for i in range(6):
        with win.card(title=f"Item {i}"):
            win.add_label("...")
```

more detail in `docs/layout.md`

## state

```python
count = vi.State(0)
win.add_label(text=lambda: f"Clicked {count.value} times")
win.add_button("+1", on_click=lambda: count.set(count.value + 1))
```

labels with a lambda for `text=` auto update when the state changes. inputs/checkboxes/sliders/dropdowns can also take `value=some_state` for two way binding. more in `docs/state.md`

## themes

```python
vi.create_theme(name="cyber", background="#0b0b0f", surface="#15151c",
                 text="#ffffff", accent="#00ffcc")
win.set_theme("cyber")  # updates everything live, no restart needed
```

built in themes: light, dark, ocean. more in `docs/themes.md`

## forms

```python
form = vi.Form()
email = win.add_input("Email")
form.add_field("email", email, required=True, pattern=r".+@.+\..+")

if form.is_valid():
    ...
else:
    print(form.errors)
```

## widgets

labels, headings, buttons (4 variants + icons), text inputs, search inputs (real placeholders, password masking), textareas, checkboxes, switches, radio groups, sliders, spinboxes, dropdowns, listboxes, a basic table, progress bars, images, links, badges, tooltips, tabs, menu bar, status bar. every widget returns a wrapper with `.get()`/`.set()`/`.on_change()`. full list in `docs/widgets.md`

## dialogs

`vi.alert()`, `vi.confirm()`, `vi.prompt()`, `vi.choose_file()`, `vi.choose_folder()`, `vi.save_file()`, `vi.pick_color()`, and `vi.toast(msg, type="success")` for notifications (non blocking, stacks properly if you fire a bunch).

## shortcuts

```python
win.bind_shortcut("Ctrl+S", save)
win.bind_shortcut("Escape", win.close)
```

## window stuff

```python
win.center(); win.maximize(); win.minimize(); win.fullscreen()
win.set_min_size(400, 300); win.on_close(confirm_before_closing)
```

## custom widgets

```python
class RatingStars(vi.Widget):
    def build(self, container, theme):
        ...  # build your tk widgets, return the outer one

win.add_widget(RatingStars())
```

more in `docs/custom_widgets.md`

## debugging layout

```python
win.debug_layout()  # draws borders around every container so u can see whats nesting where
```

off by default, doesnt do anything unless you call it.

## platforms

works on windows/mac/linux, wherever tkinter runs. maximize() has a fallback since it doesnt always behave the same on every linux window manager, but everything else should just work.

## migrating from v2

check `docs/migration_v2.md`, most stuff is backwards compatible, only a couple small breaking changes.

## running tests

```
pip install pytest
pytest
```
on linux without a display: `xvfb-run -a pytest`

## license

MIT

## author

Samarth Chugh ([@Sam3360](https://github.com/Sam3360))
