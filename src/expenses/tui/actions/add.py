"""Add expense action handlers."""
# pylint: disable=too-few-public-methods

from typing import Any

from textual.widgets import Static

from expenses.memory.types import ExpenseRecord
from expenses.tui.screens import AddExpenseScreen


class Add:
    """Handles adding expenses."""

    def __init__(self, app: Any) -> None:
        self.app = app

    def action_add_expense(self) -> None:
        self.app.push_screen(AddExpenseScreen(), self.add_expense_to_table)

    def add_expense_to_table(self, expense: ExpenseRecord | None) -> None:
        if expense is None:
            return

        try:
            self.app.state.memory.add_expense(expense)
        except ValueError as exc:
            self.app.notify(str(exc), severity="error")
            return

        self.app.state.active_records = None
        self.app.state.selected_expense_ids.clear()
        self.app.refresh_expenses_view()

    def update_summary(self, records: list[ExpenseRecord]) -> None:
        count = len(records)
        total = self.app.state.memory.get_total_amount(records)
        self.app.query_one("#summary-count", Static).update(f"Item: {count}")
        self.app.query_one("#summary-total", Static).update(f"Total: ${total:.2f}")
