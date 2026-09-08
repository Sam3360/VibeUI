import vibe as vi

win = vi.Window("Settings", size=(560, 420), theme="dark", accent="#7c6cf5")

with win.navbar():
    win.add_heading("MyApp Settings", level=3)

with win.row(expand=True):
    with win.sidebar(width=140):
        win.add_button("General", variant="ghost")
        win.add_button("Appearance", variant="ghost")
        win.add_button("Notifications", variant="ghost")

    with win.column(expand=True):
        win.add_heading("Appearance", level=2)

        with win.row(gap=10):
            for theme_name in ["light", "dark", "ocean"]:
                win.add_button(theme_name.title(), variant="secondary",
                               on_click=lambda t=theme_name: win.set_theme(t))

        win.add_spacer(12)
        win.add_switch("Enable notifications", checked=True)
        win.add_switch("Auto-start on login", checked=False)
        win.add_slider("Interface scale", 80, 150, default=100)

win.run()
