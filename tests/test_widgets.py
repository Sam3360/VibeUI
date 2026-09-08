def test_input_get_set_clear(window):
    field = window.add_input("Name")
    assert field.get() == ""  # placeholder showing means empty
    field.set("Sam")
    assert field.get() == "Sam"
    field.clear()
    assert field.get() == ""


def test_input_password_masks(window):
    field = window.add_input("Password", password=True)
    field.set("secret")
    assert field.widget.cget("show") == "*"


def test_input_on_change_fires(window):
    field = window.add_input()
    field.widget.focus_force()
    window.root.update()
    seen = []
    field.on_change(lambda v: seen.append(v))
    field.widget.insert(0, "hi")
    field.widget.event_generate("<KeyRelease>")
    window.root.update()
    assert seen == ["hi"]


def test_textarea_get_set_clear(window):
    area = window.add_textarea()
    area.set("hello\nworld")
    assert area.get() == "hello\nworld"
    area.clear()
    assert area.get() == ""


def test_checkbox_get_set(window):
    box = window.add_checkbox("Agree", checked=False)
    assert box.get() is False
    box.set(True)
    assert box.get() is True


def test_checkbox_on_change(window):
    box = window.add_checkbox("Agree")
    seen = []
    box.on_change(lambda v: seen.append(v))
    box.set(True)
    assert seen == [True]


def test_switch_get_set(window):
    sw = window.add_switch("Enabled", checked=False)
    assert sw.get() is False
    sw.set(True)
    assert sw.get() is True


def test_radio_group_default_and_set(window):
    group = window.add_radio_group(["A", "B", "C"], default="B")
    assert group.get() == "B"
    group.set("C")
    assert group.get() == "C"


def test_slider_get_set(window):
    slider = window.add_slider(min_val=0, max_val=10, default=3)
    assert slider.get() == 3
    slider.set(7)
    assert slider.get() == 7


def test_spinbox_get_set_integer(window):
    box = window.add_spinbox(0, 10, default=5)
    assert box.get() == 5
    box.set(8)
    assert box.get() == 8
    assert isinstance(box.get(), int)


def test_dropdown_get_set(window):
    dd = window.add_dropdown(["X", "Y", "Z"], default="Y")
    assert dd.get() == "Y"
    dd.set("Z")
    assert dd.get() == "Z"


def test_listbox_get_selected(window):
    lb = window.add_listbox(["a", "b", "c"])
    lb.widget.selection_set(1)
    assert lb.get_selected() == ["b"]


def test_progressbar_set_get(window):
    bar = window.add_progressbar(value=10)
    bar.set(50)
    assert bar.get() == 50


def test_table_set_rows_and_selection(window):
    table = window.add_table(["Name", "Age"], rows=[("Sam", 20), ("Ana", 25)])
    children = table.widget.get_children()
    assert len(children) == 2
    table.widget.selection_set(children[0])
    assert table.get_selected() == [("Sam", "20")]
