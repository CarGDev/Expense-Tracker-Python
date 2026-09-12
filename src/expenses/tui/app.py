from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, DataTable, Footer, Header, Static

from expenses.constants.app import BINDINGS, CSS_PATH, SUB_TITLE, TITLE
from expenses.memory.types import ExpenseRecord
from expenses.tui.controllers import ExpenseControllers
from expenses.tui.state import ExpenseState


class Expenses(App[None]):
    BINDINGS = BINDINGS
    CSS_PATH = CSS_PATH
    SUB_TITLE = SUB_TITLE
    TITLE = TITLE

    def __init__(self) -> None:
        super().__init__()
        self.state = ExpenseState()
        self.controllers = ExpenseControllers(self)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("Expense Tracker", id="screen-title"),
            Horizontal(
                Vertical(
                    Static("Expenses", id="summary-title"),
                    Static("Item: 0", id="summary-count"),
                    Static("Total: $0.00", id="summary-total"),
                    id="expenses-summary",
                ),
                Horizontal(
                    Button("󰐕", id="add", variant="success"),
                    Button("󰈲", id="filter", variant="primary"),
                    Button("󰆴", id="delete", variant="error", classes="hidden"),
                    id="action-row",
                ),
                id="summary-action-row",
            ),
            DataTable(id="expenses-table"),
            id="main-container",
        )
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#expenses-table", DataTable)
        table.cursor_type = "row"
        table.add_columns("", "ID", "Category", "Subcategory", "Date", "Amount")
        self.refresh_expenses_view()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.controllers.navigator.on_button_pressed(event)

    def action_add_expense(self) -> None:
        self.controllers.add.action_add_expense()

    def add_expense_to_table(self, expense: ExpenseRecord | None) -> None:
        self.controllers.add.add_expense_to_table(expense)

    def action_delete_expense(self) -> None:
        self.controllers.delete.action_delete_expense()

    def action_filter_expenses(self) -> None:
        self.controllers.filter.action_filter_expenses()

    def apply_filter_to_table(self, filters: ExpenseRecord | None) -> None:
        self.controllers.filter.apply_filter_to_table(filters)

    def action_clear_filter(self) -> None:
        self.controllers.filter.action_clear_filter()

    def action_toggle_selected_row(self) -> None:
        self.controllers.rows.action_toggle_selected_row()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.controllers.rows.toggle_row_selection(
            self.row_key_to_expense_id(event.row_key)
        )

    def toggle_current_row_selection(self) -> None:
        self.controllers.rows.toggle_current_row_selection()

    def row_key_to_expense_id(self, row_key: object) -> int:
        return self.controllers.rows.row_key_to_expense_id(row_key)

    def get_visible_records(self) -> list[ExpenseRecord]:
        return self.controllers.get.get_visible_records()

    def update_summary(self, records: list[ExpenseRecord]) -> None:
        self.controllers.add.update_summary(records)

    def update_filter_button(self) -> None:
        self.controllers.filter.update_filter_button()

    def update_delete_button(self) -> None:
        self.controllers.delete.update_delete_button()

    def refresh_expenses_view(self) -> None:
        self.controllers.filter.refresh_expenses_view()

    def refresh_expense_table(self, records: list[ExpenseRecord]) -> None:
        self.controllers.filter.refresh_expense_table(records)

    def action_quit(self) -> None:
        self.exit()
