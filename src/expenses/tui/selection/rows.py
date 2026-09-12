"""Row selection helpers."""

from typing import Any

from textual.widgets import DataTable


class Rows:
    """Handles expense row selection."""

    def __init__(self, app: Any) -> None:
        self.app = app

    def action_toggle_selected_row(self) -> None:
        self.toggle_current_row_selection()

    def toggle_current_row_selection(self) -> None:
        table = self.app.query_one("#expenses-table", DataTable)

        if table.row_count == 0:
            return

        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        self.toggle_row_selection(self.row_key_to_expense_id(row_key))

    def toggle_row_selection(self, expense_id: int) -> None:
        if expense_id in self.app.state.selected_expense_ids:
            self.app.state.selected_expense_ids.remove(expense_id)
        else:
            self.app.state.selected_expense_ids.add(expense_id)

        self.app.refresh_expenses_view()

    def row_key_to_expense_id(self, row_key: object) -> int:
        return int(getattr(row_key, "value", row_key))
