import vibe as vi

win = vi.Window("Sign Up", size=(380, 480), theme="light")
form = vi.Form()

win.add_heading("Create an account", level=2)

username = win.add_input("Username")
form.add_field("username", username, required=True, min_length=3, max_length=20)

email = win.add_input("Email")
form.add_field("email", email, required=True, pattern=r".+@.+\..+")

age = win.add_spinbox(0, 120, default=18)
form.add_field("age", age, min_value=13, max_value=120)

password = win.add_input("Password", password=True)
form.add_field("password", password, required=True, min_length=8)

confirm = win.add_input("Confirm password", password=True)
form.add_field("confirm", confirm, custom=lambda v: v == password.get() or "Passwords don't match")

win.add_spacer(10)


def submit():
    if form.is_valid():
        vi.alert(f"Welcome, {username.get()}!")
    else:
        messages = [msg for errs in form.errors.values() for msg in errs]
        vi.alert("\n".join(messages), title="Please fix these issues")


win.add_button("Create account", on_click=submit)

win.run()
