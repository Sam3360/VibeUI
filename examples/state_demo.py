import vibe as vi

win = vi.Window("State Demo", size=(360, 300), theme="dark")

name = vi.State("world")
count = vi.State(0)

win.add_heading("Reactive State", level=2)

# add_label(text=<callable>) automatically re-renders when `name` changes.
win.add_label(text=lambda: f"Hello, {name.value}!", size="lg", bold=True)

# add_input(value=<State>) is a two-way binding: typing updates `name`,
# and changing `name` elsewhere updates the input.
win.add_input(value=name)

win.add_spacer(16)
win.add_label(text=lambda: f"Clicked {count.value} times")
with win.row():
    win.add_button("+1", on_click=lambda: count.set(count.value + 1))
    win.add_button("Reset", variant="secondary", on_click=lambda: count.set(0))

win.run()
