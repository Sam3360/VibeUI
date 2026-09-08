import vibe as vi

win = vi.Window("Chat", size=(380, 480), theme="dark", accent="#00b4d8")

messages = []

with win.navbar():
    win.add_heading("#general", level=3)

message_box = win.add_textarea(rows=12, placeholder="Messages will appear here...")
message_box.widget.config(state="disabled")

with win.row(expand=True):
    draft = win.add_input("Type a message...")
    win.add_button("Send", on_click=lambda: send())


def send():
    text = draft.get().strip()
    if not text:
        return
    messages.append(f"You: {text}")
    message_box.widget.config(state="normal")
    message_box.set("\n".join(messages))
    message_box.widget.config(state="disabled")
    draft.clear()

    # simulate a canned reply so the UI feels alive
    win.root.after(400, lambda: reply(f"Echo: {text}"))


def reply(text):
    messages.append(text)
    message_box.widget.config(state="normal")
    message_box.set("\n".join(messages))
    message_box.widget.config(state="disabled")


win.run()
