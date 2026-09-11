from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, DataTable, Footer, Header, Static

from expenses.constants.app import BINDINGS, CSS_PATH, SUB_TITLE, TITLE
from expenses.memory.core import ExpenseMemory
from expenses.memory.types import ExpenseRecord
from expenses.memory.utils import parse_yyyy_mm_dd
from expenses.tui.screens import AddExpenseScreen, FilterExpenseScreen


class Expenses(App[None]):
    BINDINGS = BINDINGS
    CSS_PATH = CSS_PATH
    SUB_TITLE = SUB_TITLE
    TITLE = TITLE

    def __init__(self) -> None:
        super().__init__()
        self.memory = ExpenseMemory()
        self.active_records: list[ExpenseRecord] | None = None
        self.selected_expense_ids: set[int] = set()

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
                    Button("󰐕 Add", id="add", variant="success"),
                    Button("󰈲 Filter", id="filter", variant="primary"),
                    Button("󰆴 Delete", id="delete", variant="error", classes="hidden"),
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
        if event.button.id == "add":
            self.action_add_expense()
        elif event.button.id == "filter":
            self.action_filter_expenses()
        elif event.button.id == "delete":
            self.action_delete_expense()

    def action_add_expense(self) -> None:
        self.push_screen(AddExpenseScreen(), self.add_expense_to_table)

    def add_expense_to_table(self, expense: ExpenseRecord | None) -> None:
        if expense is None:
            return

        try:
            self.memory.add_expense(expense)
        except ValueError as exc:
            self.notify(str(exc), severity="error")
            return

        self.active_records = None
        self.selected_expense_ids.clear()
        self.refresh_expenses_view()

    def action_delete_expense(self) -> None:
        table = self.query_one("#expenses-table", DataTable)

        if table.row_count == 0:
            self.notify("No expenses to delete", severity="warning")
            return

        if not self.selected_expense_ids:
            self.notify("Select rows before deleting", severity="warning")
            return

        deleted_count = 0
        for expense_id in list(self.selected_expense_ids):
            if self.memory.delete_expense(expense_id):
                deleted_count += 1

        self.selected_expense_ids.clear()
        if self.active_records is not None:
            self.active_records = [
                record
                for record in self.active_records
                if self.memory.view_expense(int(record.get("id", 0))) is not None
            ]
        self.refresh_expenses_view()
        self.notify(f"Deleted {deleted_count} expense(s)")

    def action_filter_expenses(self) -> None:
        if self.active_records is not None:
            self.action_clear_filter()
            return

        self.push_screen(FilterExpenseScreen(), self.apply_filter_to_table)

    def apply_filter_to_table(self, filters: ExpenseRecord | None) -> None:
        if filters is None:
            return

        if not filters:
            self.active_records = None
            self.selected_expense_ids.clear()
            self.refresh_expenses_view()
            return

        date_from = parse_yyyy_mm_dd(str(filters.get("date_from", "")))
        date_to = parse_yyyy_mm_dd(str(filters.get("date_to", "")))
        category = str(filters.get("category", "")) or None
        subcategory = str(filters.get("subcategory", "")) or None

        self.active_records = self.memory.filter_expenses(
            date_from=date_from,
            date_to=date_to,
            category=category,
            subcategory=subcategory,
        )
        self.selected_expense_ids.clear()
        self.refresh_expenses_view()

    def action_clear_filter(self) -> None:
        self.active_records = None
        self.selected_expense_ids.clear()
        self.refresh_expenses_view()
        self.notify("Filters cleared")

    def action_toggle_selected_row(self) -> None:
        self.toggle_current_row_selection()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.toggle_row_selection(self.row_key_to_expense_id(event.row_key))

    def toggle_current_row_selection(self) -> None:
        table = self.query_one("#expenses-table", DataTable)

        if table.row_count == 0:
            return

        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        self.toggle_row_selection(self.row_key_to_expense_id(row_key))

    def row_key_to_expense_id(self, row_key: object) -> int:
        return int(getattr(row_key, "value", row_key))

    def toggle_row_selection(self, expense_id: int) -> None:
        if expense_id in self.selected_expense_ids:
            self.selected_expense_ids.remove(expense_id)
        else:
            self.selected_expense_ids.add(expense_id)

        self.refresh_expenses_view()

    def get_visible_records(self) -> list[ExpenseRecord]:
        if self.active_records is None:
            return self.memory.view_all_expenses()
        return self.active_records

    def update_summary(self, records: list[ExpenseRecord]) -> None:
        count = len(records)
        total = self.memory.get_total_amount(records)
        self.query_one("#summary-count", Static).update(f"Item: {count}")
        self.query_one("#summary-total", Static).update(f"Total: ${total:.2f}")

    def update_filter_button(self) -> None:
        filter_button = self.query_one("#filter", Button)
        if self.active_records is None:
            filter_button.label = "󰈲 Filter"
        else:
            filter_button.label = "󰃢 Clear"

    def update_delete_button(self) -> None:
        delete_button = self.query_one("#delete", Button)
        if self.selected_expense_ids:
            delete_button.remove_class("hidden")
        else:
            delete_button.add_class("hidden")

    def refresh_expenses_view(self) -> None:
        records = self.get_visible_records()
        visible_expense_ids = {int(expense.get("id", 0)) for expense in records}
        self.selected_expense_ids.intersection_update(visible_expense_ids)

        self.refresh_expense_table(records)
        self.update_summary(records)
        self.update_filter_button()
        self.update_delete_button()

    def refresh_expense_table(self, records: list[ExpenseRecord]) -> None:
        table = self.query_one("#expenses-table", DataTable)
        table.clear()

        for expense in records:
            expense_date = expense["date"]
            expense_id = int(expense["id"])
            table.add_row(
                "󰄲" if expense_id in self.selected_expense_ids else "",
                str(expense_id),
                str(expense["category"]),
                str(expense["subcategory"]),
                expense_date.strftime("%Y-%m-%d"),
                f"${float(expense['amount']):.2f}",
                key=str(expense_id),
            )

    def action_quit(self) -> None:
        self.exit()
