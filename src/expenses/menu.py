from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static


class Expenses(App[None]):
    TITLE = "Expense Tracker"
    SUB_TITLE = "Welcome to expense tracker"
    BINDINGS = [("q", "quit", "Quit application")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Welcome to Expense Tracker!")
        yield Static("Press q to quit.")
        yield Footer()

    def action_quit(self) -> None:
        self.exit()


def main() -> None:
    app = Expenses()
    app.run()
