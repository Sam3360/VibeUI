from vibe.state import State


def test_state_get_set():
    s = State(1)
    assert s.get() == 1
    s.set(2)
    assert s.get() == 2


def test_state_value_property():
    s = State("a")
    assert s.value == "a"
    s.value = "b"
    assert s.value == "b"


def test_state_subscribe_fires_on_change():
    s = State(0)
    seen = []
    s.subscribe(lambda v: seen.append(v))
    s.set(1)
    s.set(2)
    assert seen == [1, 2]


def test_state_subscribe_does_not_fire_on_same_value():
    s = State(5)
    seen = []
    s.subscribe(lambda v: seen.append(v))
    s.set(5)
    assert seen == []


def test_state_unsubscribe_stops_callbacks():
    s = State(0)
    seen = []
    unsubscribe = s.subscribe(lambda v: seen.append(v))
    s.set(1)
    unsubscribe()
    s.set(2)
    assert seen == [1]


def test_label_auto_binds_to_state_and_updates(window):
    name = State("Sam")
    label = window.add_label(text=lambda: f"Hello {name.value}!")
    assert label.cget("text") == "Hello Sam!"
    name.set("Ana")
    window.root.update()
    assert label.cget("text") == "Hello Ana!"


def test_label_binding_cleans_up_on_destroy(window):
    name = State("Sam")
    label = window.add_label(text=lambda: f"Hi {name.value}")
    label.destroy()
    window.root.update()
    # Setting after destroy should not raise, since the subscription was cleaned up.
    name.set("Changed")


def test_input_two_way_state_binding(window):
    name = State("Sam")
    field = window.add_input(value=name)
    assert field.get() == "Sam"

    name.set("Ana")
    window.root.update()
    assert field.get() == "Ana"

    # Simulate the user typing, which fires on_change -> updates state.
    field.widget.focus_force()
    window.root.update()
    field.widget.delete(0, "end")
    field.widget.insert(0, "Typed2")
    field.widget.event_generate("<KeyRelease>")
    window.root.update()
    assert name.get() == "Typed2"
