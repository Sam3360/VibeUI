import vibe as vi

win = vi.Window("Responsive Demo", size=(500, 400), theme="light", resizable=True)

size_text = vi.State("500 x 400")
win.add_label(text=lambda: f"Window size: {size_text.value}", size="sm")


def on_resize(event):
    if event.widget is win.root:
        size_text.set(f"{event.width} x {event.height}")


win.root.bind("<Configure>", on_resize)

with win.grid(columns=3, gap=10):
    for i in range(9):
        with win.card():
            win.add_label(f"Card {i + 1}")

win.run()
