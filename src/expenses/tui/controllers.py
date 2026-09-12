"""Controller bundle for the expense TUI."""
# pylint: disable=too-few-public-methods

from typing import Any

from expenses.tui.actions import Add, Delete, Filter, Get
from expenses.tui.navigation import Navigator
from expenses.tui.selection import Rows


class ExpenseControllers:
    """Groups app helpers to keep the app instance small."""

    def __init__(self, app: Any) -> None:
        self.navigator = Navigator(app)
        self.rows = Rows(app)
        self.add = Add(app)
        self.delete = Delete(app)
        self.filter = Filter(app)
        self.get = Get(app)
