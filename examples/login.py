import vibe as vi

win = vi.Window("Login", size=(360, 320), theme="dark", accent="#4f46e5")
form = vi.Form()

win.add_heading("Welcome back", level=2)
win.add_label("Sign in to continue", size="sm", color=win.theme_colors["muted"])
win.add_spacer(16)

email = win.add_input("Email")
form.add_field("email", email, required=True, pattern=r".+@.+\..+")

password = win.add_input("Password", password=True)
form.add_field("password", password, required=True, min_length=6)

win.add_spacer(8)


def submit():
    if form.is_valid():
        vi.toast(f"Welcome, {email.get()}!", type="success", parent=win)
    else:
        vi.toast("Please fix the highlighted fields.", type="error", parent=win)


win.add_button("Sign In", on_click=submit)
win.add_link("Forgot password?", on_click=lambda: vi.alert("Check your email for a reset link."))

win.run()
