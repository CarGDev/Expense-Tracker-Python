from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, DataTable, Footer, Header, Static

from expenses.tui.screens import AddExpenseScreen


class Expenses(App[None]):
    TITLE = "Expense Tracker"
    SUB_TITLE = "Welcome to expense tracker"
    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("q", "quit", "Quit application"),
        ("a", "add_expense", "Add expense"),
        ("d", "delete_expense", "Delete expense"),
    ]

    next_expense_id = 1

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("Expense Tracker", id="screen-title"),
            Horizontal(
                Button("Add", id="add", variant="success"),
                Button("Edit", id="edit", variant="primary"),
                Button("Delete", id="delete", variant="error"),
                id="action-row",
            ),
            DataTable(id="expenses-table"),
            id="main-container",
        )
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#expenses-table", DataTable)
        table.cursor_type = "row"
        table.add_columns("ID", "Category", "Subcategory", "Date", "Amount")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add":
            self.action_add_expense()
        elif event.button.id == "edit":
            self.notify("Edit will be added after the table flow works")
        elif event.button.id == "delete":
            self.action_delete_expense()

    def action_add_expense(self) -> None:
        self.push_screen(AddExpenseScreen(), self.add_expense_to_table)

    def add_expense_to_table(self, expense: tuple[str, str, str, str] | None) -> None:
        if expense is None:
            return

        category, subcategory, date, amount = expense
        table = self.query_one("#expenses-table", DataTable)
        table.add_row(
            str(self.next_expense_id),
            category,
            subcategory,
            date,
            amount,
        )
        self.next_expense_id += 1

    def action_delete_expense(self) -> None:
        table = self.query_one("#expenses-table", DataTable)

        if table.row_count == 0:
            self.notify("No expenses to delete", severity="warning")
            return

        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        table.remove_row(row_key)

    def action_quit(self) -> None:
        self.exit()
