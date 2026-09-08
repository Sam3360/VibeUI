import vibe as vi

vi.create_theme(
    name="cyber",
    background="#0b0b0f", surface="#15151c", text="#ffffff", accent="#00ffcc",
)

win = vi.Window("Theme Demo", size=(420, 320), theme="light")

win.add_heading("Theme Demo", level=1)
win.add_label("Click a button to switch themes instantly — nothing restarts.", size="sm")
win.add_spacer(12)

with win.row(gap=10):
    for theme_name in vi.list_themes():
        win.add_button(theme_name.title(), variant="secondary",
                       on_click=lambda t=theme_name: win.set_theme(t))

win.add_spacer(16)
with win.card(title="Preview"):
    win.add_label("This card follows whatever theme is active.")
    win.add_button("Primary action")
    win.add_badge("Badge", variant="info")

win.run()
