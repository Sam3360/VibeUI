# vibeUI

**vibeUI** is a beginner-friendly, professional Python GUI library built on top of Tkinter.  
It allows you to create interactive, modern GUI applications with **minimal code**, making it perfect for learners, hobbyists, and educators.

---

## Features

- Create windows with custom titles, sizes, and themes (light/dark)
- Add labels, buttons, input fields, text areas
- Interactive widgets: checkboxes, sliders
- Popups: alerts, confirm dialogs, prompts
- Beginner-friendly, easy-to-use API
- Cross-platform: Windows, Mac, Linux

---

## Installation

Install directly from your local package (for development):

```bash
pip install vibeUI
```

---

# Quick Start
import vibe as vi

## Create a window
win = vi.Window("Vibe Demo", size=(500, 400), theme="light")

## Add a label
win.add_label("Hello Vibe!", pos=(50, 50), font_size=20)

## Add input field
name_input = win.add_input("Enter your name", pos=(50, 100))

## Add button with callback
def greet():
    vi.alert(f"Hello {name_input.get()}!", title="Greeting")

win.add_button("Greet Me", pos=(50, 150), command=greet)

## Run the GUI
win.run()

---

Advanced Usage

 - Checkbox and slider widgets

 - Customizable themes and colors

 - Alerts, confirmations, and prompt dialogs

 - Easy-to-extend for additional widgets

 - Supports multiple windows and interactive callbacks

 ---

# License

Vibe is released under the MIT License.