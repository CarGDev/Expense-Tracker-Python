"""Delete expense action handlers."""
# pylint: disable=too-few-public-methods

from typing import Any

from textual.widgets import Button, DataTable


class Delete:
    """Handles deleting expenses."""

    def __init__(self, app: Any) -> None:
        self.app = app

    def action_delete_expense(self) -> None:
        table = self.app.query_one("#expenses-table", DataTable)

        if table.row_count == 0:
            self.app.notify("No expenses to delete", severity="warning")
            return

        if not self.app.state.selected_expense_ids:
            self.app.notify("Select rows before deleting", severity="warning")
            return

        deleted_count = 0
        for expense_id in list(self.app.state.selected_expense_ids):
            if self.app.state.memory.delete_expense(expense_id):
                deleted_count += 1

        self.app.state.selected_expense_ids.clear()
        if self.app.state.active_records is not None:
            self.app.state.active_records = [
                record
                for record in self.app.state.active_records
                if self.app.state.memory.view_expense(int(record.get("id", 0)))
                is not None
            ]
        self.app.refresh_expenses_view()
        self.app.notify(f"Deleted {deleted_count} expense(s)")

    def update_delete_button(self) -> None:
        delete_button = self.app.query_one("#delete", Button)
        if self.app.state.selected_expense_ids:
            delete_button.remove_class("hidden")
        else:
            delete_button.add_class("hidden")
