"""Read helpers for expense records."""
# pylint: disable=too-few-public-methods

from typing import Any

from expenses.memory.types import ExpenseRecord


class Get:
    """Returns visible records for the current table state."""

    def __init__(self, app: Any) -> None:
        self.app = app

    def get_visible_records(self) -> list[ExpenseRecord]:
        if self.app.state.active_records is None:
            return self.app.state.memory.view_all_expenses()
        return self.app.state.active_records
