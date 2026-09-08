import os
import vibe as vi

win = vi.Window("File Manager", size=(420, 380), theme="dark")

current_folder = vi.State(os.path.expanduser("~"))
win.add_label(text=lambda: f"Folder: {current_folder.value}", size="sm")

file_list = win.add_listbox([], height=12)


def refresh():
    try:
        entries = sorted(os.listdir(current_folder.value))
    except OSError as e:
        entries = [f"(couldn't read folder: {e})"]
    file_list.set_items(entries)


def pick_folder():
    folder = vi.choose_folder(title="Choose a folder")
    if folder:
        current_folder.set(folder)
        refresh()


def open_file():
    path = vi.choose_file(title="Open a file")
    if path:
        vi.toast(f"Selected: {os.path.basename(path)}", parent=win)


def save_copy():
    path = vi.save_file(title="Save as", default_ext=".txt")
    if path:
        vi.toast(f"Would save to: {path}", parent=win)


with win.row():
    win.add_button("Choose folder", on_click=pick_folder)
    win.add_button("Open file", variant="secondary", on_click=open_file)
    win.add_button("Save as...", variant="secondary", on_click=save_copy)

refresh()
win.run()
