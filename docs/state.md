# State (reactive data binding)

`vi.State` is a small observable value box. It exists so simple UIs — a
counter, a live-updating label, a two-way-bound input — don't need manual
wiring every time something changes.

## Basics

```python
count = vi.State(0)

count.value          # read
count.value = 5      # write
count.get()          # same as .value
count.set(5)         # same as .value = 5

unsubscribe = count.subscribe(lambda new_value: print("changed to", new_value))
unsubscribe()  # stop listening
```

Setting a `State` to its current value is a no-op — subscribers only fire on
an actual change.

## Automatic label binding

Pass a zero-argument callable (usually a `lambda`) as `text=` to `add_label`,
and vibeUI watches which `State`s it reads while evaluating it. Whenever any
of those change, the label re-renders:

```python
name = vi.State("Sam")
win.add_label(text=lambda: f"Hello, {name.value}!")

name.set("Ana")  # label updates to "Hello, Ana!" automatically
```

This works because reading `.value` inside a tracked callable registers a
subscription automatically — you don't call `.subscribe()` yourself for this
common case.

## Two-way input binding

```python
name = vi.State("Sam")
win.add_input(value=name)
```

Typing in the input updates `name`; setting `name` elsewhere updates the
input. The same `value=` pattern works on `add_checkbox`, `add_slider`, and
`add_dropdown`.

## Memory safety

- Label bindings clean up their subscription automatically when the label
  widget is destroyed (`<Destroy>` event), so long-running apps that add/remove
  widgets dynamically don't leak callbacks.
- `value=` bindings on inputs/checkboxes/sliders/dropdowns do the same.
- If you call `.subscribe()` yourself, you're responsible for calling the
  returned `unsubscribe()` function when you're done (e.g. in a custom
  widget's `on_destroy`).

## What State is *not*

It's intentionally not a full signals/computed-values framework. There's no
`vi.computed()` that memoizes a derived value across multiple widgets — if
you need the same computed string in two places, either call the same
`lambda` in both `add_label(text=...)` calls, or compute it yourself and
store it in a second `State`.
