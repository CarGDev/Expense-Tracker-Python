"""Filter expense action handlers and table refreshes."""

from typing import Any

from textual.widgets import Button, DataTable

from expenses.memory.types import ExpenseRecord
from expenses.memory.utils import parse_yyyy_mm_dd
from expenses.tui.screens import FilterExpenseScreen


class Filter:
    """Handles filtering expenses and refreshing the table."""

    def __init__(self, app: Any) -> None:
        self.app = app

    def action_filter_expenses(self) -> None:
        if self.app.state.active_records is not None:
            self.app.action_clear_filter()
            return

        self.app.push_screen(FilterExpenseScreen(), self.apply_filter_to_table)

    def apply_filter_to_table(self, filters: ExpenseRecord | None) -> None:
        if filters is None:
            return

        if not filters:
            self.app.state.active_records = None
            self.app.state.selected_expense_ids.clear()
            self.app.refresh_expenses_view()
            return

        date_from = parse_yyyy_mm_dd(str(filters.get("date_from", "")))
        date_to = parse_yyyy_mm_dd(str(filters.get("date_to", "")))
        category = str(filters.get("category", "")) or None
        subcategory = str(filters.get("subcategory", "")) or None

        self.app.state.active_records = self.app.state.memory.filter_expenses(
            date_from=date_from,
            date_to=date_to,
            category=category,
            subcategory=subcategory,
        )
        self.app.state.selected_expense_ids.clear()
        self.app.refresh_expenses_view()

    def action_clear_filter(self) -> None:
        self.app.state.active_records = None
        self.app.state.selected_expense_ids.clear()
        self.app.refresh_expenses_view()
        self.app.notify("Filters cleared")

    def update_filter_button(self) -> None:
        filter_button = self.app.query_one("#filter", Button)
        if self.app.state.active_records is None:
            filter_button.label = "󰈲"
        else:
            filter_button.label = "󰃢"

    def refresh_expenses_view(self) -> None:
        records = self.app.get_visible_records()
        visible_expense_ids = {int(expense.get("id", 0)) for expense in records}
        self.app.state.selected_expense_ids.intersection_update(visible_expense_ids)

        self.app.refresh_expense_table(records)
        self.app.update_summary(records)
        self.app.update_filter_button()
        self.app.update_delete_button()

    def refresh_expense_table(self, records: list[ExpenseRecord]) -> None:
        table = self.app.query_one("#expenses-table", DataTable)
        table.clear()

        for expense in records:
            expense_date = expense["date"]
            expense_id = int(expense["id"])
            table.add_row(
                "󰄲" if expense_id in self.app.state.selected_expense_ids else "",
                str(expense_id),
                str(expense["category"]),
                str(expense["subcategory"]),
                expense_date.strftime("%Y-%m-%d"),
                f"${float(expense['amount']):.2f}",
                key=str(expense_id),
            )
