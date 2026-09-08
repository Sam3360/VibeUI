import vibe as vi


def test_toast_creates_a_visible_window(window):
    top = vi.toast("Saved!", type="success", duration=100000, parent=window)
    window.root.update()
    assert top.winfo_exists()
    top.destroy()


def test_multiple_toasts_stack_without_overlapping(window):
    t1 = vi.toast("First", duration=100000, parent=window)
    window.root.update()
    t2 = vi.toast("Second", duration=100000, parent=window)
    window.root.update()
    # Stacked toasts should not sit at the exact same y position.
    assert t1.winfo_y() != t2.winfo_y()
    t1.destroy()
    t2.destroy()


def test_toast_auto_dismisses_after_duration(window):
    top = vi.toast("Bye", duration=50, parent=window)
    window.root.after(150, window.root.quit)
    window.root.mainloop()
    assert not top.winfo_exists()
