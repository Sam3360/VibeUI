"""
vibeUI v2 demo — run this to see most of the widget library in one window.

    python examples/demo.py
"""

import vibe as vi


def main():
    win = vi.Window("vibeUI v2 Demo", size=(560, 640), theme="dark", accent="#7c6cf5")

    win.set_menu({
        "File": {"New": lambda: vi.toast("New!", parent=win), "-": None, "Exit": win.close},
        "Help": {"About": lambda: vi.alert("vibeUI v2\nBy Samarth Chugh", title="About")},
    })

    win.add_label("Welcome to vibeUI v2", size="xl", bold=True)
    win.add_label("A beginner-friendly GUI toolkit for Python", size="sm", color="#9aa0a6")
    win.add_separator()

    name = win.add_input("Enter your name")

    with win.row():
        win.add_button("Say hi", on_click=lambda: vi.alert(f"Hello {name.get() or 'friend'}!"))
        win.add_button("Toast", variant="secondary",
                        on_click=lambda: vi.toast("Just a quick note!", parent=win))
        win.add_button("Danger", variant="danger", on_click=lambda: vi.confirm("Are you sure?"))

    with win.card(title="Preferences"):
        newsletter = win.add_checkbox("Subscribe to updates", checked=True)
        plan = win.add_radio_group(["Free", "Pro", "Team"], default="Pro")
        volume = win.add_slider("Volume", 0, 100, default=60)

    with win.row():
        win.add_dropdown(["Light", "Dark", "Ocean"], default="Dark")
        win.add_progressbar(value=40)

    tabs = win.tabs(["Overview", "Details"])
    with tabs.tab("Overview"):
        win.add_label("This is the Overview tab.")
    with tabs.tab("Details"):
        win.add_textarea(rows=4, placeholder="Type some notes here...")

    win.add_status_bar("Ready")

    win.run()


if __name__ == "__main__":
    main()
