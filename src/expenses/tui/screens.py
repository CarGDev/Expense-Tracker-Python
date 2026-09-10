from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Select, Static

from expenses.categories import CATEGORIES


class AddExpenseScreen(ModalScreen[tuple[str, str, str, str] | None]):
    """Modal form for collecting an expense before adding it to the table."""

    def compose(self) -> ComposeResult:
        first_category = next(iter(CATEGORIES))

        yield Vertical(
            Static("Add Expense", id="modal-title"),
            Static("Category"),
            Select(
                [(category.title(), category) for category in CATEGORIES],
                value=first_category,
                id="category-select",
            ),
            Static("Subcategory"),
            Select(
                [(subcategory, subcategory) for subcategory in CATEGORIES[first_category]],
                value=CATEGORIES[first_category][0],
                id="subcategory-select",
            ),
            Static("Date"),
            Input(placeholder="YYYY-MM-DD", id="date-input"),
            Static("Amount"),
            Input(placeholder="0.00", id="amount-input"),
            Horizontal(
                Button("Save", id="save-expense", variant="success"),
                Button("Cancel", id="cancel-expense"),
                id="modal-buttons",
            ),
            id="add-expense-modal",
        )

    @on(Select.Changed, "#category-select")
    def update_subcategories(self, event: Select.Changed) -> None:
        category = str(event.value)
        subcategory_select = self.query_one("#subcategory-select", Select)
        subcategories = CATEGORIES[category]

        subcategory_select.set_options(
            [(subcategory, subcategory) for subcategory in subcategories]
        )
        subcategory_select.value = subcategories[0]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel-expense":
            self.dismiss(None)
            return

        if event.button.id != "save-expense":
            return

        category = self.query_one("#category-select", Select).value
        subcategory = self.query_one("#subcategory-select", Select).value
        date = self.query_one("#date-input", Input).value.strip()
        amount = self.query_one("#amount-input", Input).value.strip()

        if not date or not amount:
            self.notify("Date and amount are required", severity="error")
            return

        self.dismiss((str(category), str(subcategory), date, amount))
