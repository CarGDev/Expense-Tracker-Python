"""Button navigation for the expense TUI."""
# pylint: disable=too-few-public-methods

from collections.abc import Callable
from typing import Protocol

from textual.widgets import Button


class NavigationApp(Protocol):
    """App actions used by the navigation handler."""

    def action_add_expense(self) -> None:
        """Open the add expense flow."""

    def action_filter_expenses(self) -> None:
        """Open or clear the filter flow."""

    def action_delete_expense(self) -> None:
        """Delete selected expenses."""


class Navigator:
    """Routes button events to app actions."""

    def __init__(self, app: NavigationApp) -> None:
        self.app = app

    def on_button_pressed(self, event: Button.Pressed) -> None:
        actions: dict[str, Callable[[], None]] = {
            "add": self.app.action_add_expense,
            "filter": self.app.action_filter_expenses,
            "delete": self.app.action_delete_expense,
        }
        action = actions.get(event.button.id or "")

        if action is not None:
            action()
