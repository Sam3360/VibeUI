import vibe as vi

win = vi.Window("Dashboard", size=(700, 520), theme="dark", accent="#7c6cf5")

with win.navbar():
    win.add_heading("Acme Analytics", level=3)
    win.add_badge("Live", variant="success")

with win.grid(columns=3, gap=14):
    with win.card(title="Revenue"):
        win.add_label("$48,204", size="xxl", bold=True)
        win.add_badge("+12% this month", variant="success")

    with win.card(title="Active Users"):
        win.add_label("2,391", size="xxl", bold=True)
        win.add_progressbar(value=72)

    with win.card(title="Server Load"):
        win.add_label("41%", size="xxl", bold=True)
        win.add_badge("Healthy", variant="info")

with win.card(title="Recent Orders"):
    table = win.add_table(["Order", "Customer", "Status"])
    table.set_rows([
        ("#1042", "Priya Shah", "Shipped"),
        ("#1041", "Diego Ruiz", "Processing"),
        ("#1040", "Mei Tanaka", "Delivered"),
    ])

win.run()
