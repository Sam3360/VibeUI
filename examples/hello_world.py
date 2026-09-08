import vibe as vi

win = vi.Window("Hello, vibeUI!", size=(360, 200), theme="dark")

win.add_label("Hello, vibeUI!", size="xl", bold=True)
name = win.add_input("Enter your name")
win.add_button("Greet Me", on_click=lambda: vi.alert(f"Hello {name.get() or 'friend'}!"))

win.run()
