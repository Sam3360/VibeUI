import vibe as vi

win = vi.Window("Todo", size=(360, 460), theme="light", accent="#12b76a")

todos = []
count_label_text = vi.State("0 tasks")

win.add_heading("Todo", level=1)

with win.row():
    new_task = win.add_input("Add a task...")
    win.add_button("Add", on_click=lambda: add_task())

task_list = win.add_listbox([], height=12)
win.add_label(text=lambda: count_label_text.value, size="sm",
              color=win.theme_colors["muted"])


def refresh():
    task_list.set_items(todos)
    count_label_text.set(f"{len(todos)} task{'s' if len(todos) != 1 else ''}")


def add_task():
    text = new_task.get().strip()
    if text:
        todos.append(text)
        new_task.clear()
        refresh()


def remove_selected():
    for item in task_list.get_selected():
        todos.remove(item)
    refresh()


win.add_button("Remove selected", variant="danger", on_click=remove_selected)

win.run()
