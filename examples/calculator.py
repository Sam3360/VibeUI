import vibe as vi

win = vi.Window("Calculator", size=(300, 400), theme="dark", accent="#00cc88")

display = vi.State("0")
win.add_label(text=lambda: display.value, size="xxl", bold=True)

state = {"expression": ""}


def press(key):
    if key == "C":
        state["expression"] = ""
    elif key == "=":
        try:
            state["expression"] = str(eval(state["expression"], {"__builtins__": {}}))
        except Exception:
            state["expression"] = "Error"
    else:
        state["expression"] += key
    display.set(state["expression"] or "0")


with win.grid(columns=4, gap=6):
    for key in ["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "C", "0", "=", "+"]:
        variant = "primary" if key == "=" else ("secondary" if key.isdigit() else "ghost")
        win.add_button(key, on_click=lambda k=key: press(k), variant=variant)

win.run()
