import vibe as vi


def test_required_validation(window):
    field = window.add_input()
    field.validate(required=True)
    assert field.is_valid() is False
    field.set("something")
    assert field.is_valid() is True


def test_pattern_validation(window):
    field = window.add_input()
    field.validate(required=True, pattern=r".+@.+\..+")
    field.set("not-an-email")
    assert field.is_valid() is False
    field.set("me@example.com")
    assert field.is_valid() is True


def test_length_validation(window):
    field = window.add_input()
    field.validate(min_length=3, max_length=6)
    field.set("ab")
    assert field.is_valid() is False
    field.set("abcdefgh")
    assert field.is_valid() is False
    field.set("abcd")
    assert field.is_valid() is True


def test_custom_validator(window):
    field = window.add_input()
    field.validate(custom=lambda v: v == "sam" or "must be 'sam'")
    field.set("someone-else")
    assert field.is_valid() is False
    assert "must be 'sam'" in field.check()
    field.set("sam")
    assert field.is_valid() is True


def test_invalid_field_shows_error_border(window):
    field = window.add_input()
    field.validate(required=True)
    field.is_valid()
    assert field.widget.cget("highlightbackground") == window.theme_colors["danger"]
    field.set("ok")
    field.is_valid()
    assert field.widget.cget("highlightbackground") != window.theme_colors["danger"]


def test_form_aggregates_multiple_fields(window):
    form = vi.Form()
    email = window.add_input()
    age = window.add_spinbox(0, 120, default=0)
    form.add_field("email", email, required=True, pattern=r".+@.+\..+")
    form.add_field("age", age, min_value=13)

    assert form.is_valid() is False
    assert "email" in form.errors

    email.set("me@example.com")
    age.set(20)
    assert form.is_valid() is True
    assert form.errors == {}
    assert form.values == {"email": "me@example.com", "age": 20}


def test_form_reset_clears_fields(window):
    form = vi.Form()
    email = window.add_input()
    form.add_field("email", email)
    email.set("me@example.com")
    form.reset()
    assert email.get() == ""
