import re

from textual import events, on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Select, Static

from expenses.categories import CATEGORIES
from expenses.memory.types import ExpenseRecord
from expenses.memory.utils import parse_yyyy_mm_dd


class AddExpenseScreen(ModalScreen[ExpenseRecord | None]):
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
                [
                    (subcategory, subcategory)
                    for subcategory in CATEGORIES[first_category]
                ],
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

    @on(Input.Blurred, "#date-input")
    def date_input_blurred(self, event: Input) -> None:
        raw_value = event.input.value.replace("-", "").strip()

        if not raw_value:
            return

        digits = ""

        for char in raw_value:
            if char.isdigit():
                if len(digits) < 8:
                    digits += char
                else:
                    event.input.value = ""
                    self.notify("Date cannot be more than 8 digits", severity="error")
                    return
            else:
                event.input.value = ""
                self.notify("Only numbers are valid for date", severity="error")
                return

        if len(digits) != 8:
            event.input.value = ""
            self.notify("Date must be 8 digits: YYYYMMDD", severity="error")
            return

        formatted_date = f"{digits[:4]}-{digits[4:6]}-{digits[6:]}"

        if parse_yyyy_mm_dd(formatted_date) is None:
            event.input.value = ""
            self.notify("Date is not valid", severity="error")
            return

        event.input.value = formatted_date

    def on_focus(self, event: Input.Focused) -> None:
        if event.widget.id != "date-input":
            return

        date_input = self.query_one("#date-input", Input)
        date_input.value = date_input.value.replace("-", "")

    @on(Input.Blurred, "#amount-input")
    def amount_input_blurred(self, event: Input) -> None:
        raw_value = event.input.value.replace("$", "").strip()

        if not raw_value:
            event.input.value = ""
            return

        dollars, _, cents = raw_value.partition(".")
        if not dollars:
            dollars = "0"

        cents = cents[:2].ljust(2, "0")
        event.input.value = f"${dollars}.{cents}"

    @on(Input.Changed, "#amount-input")
    def update_input(self, event: Input) -> None:
        raw_value = event.value.replace("$", "")

        cleaned = ""
        has_decimal = False

        for char in raw_value:
            if char.isdigit():
                cleaned += char
            elif char == "." and not has_decimal:
                cleaned += char
                has_decimal = True

        if event.input.value != cleaned:
            event.input.value = cleaned

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel-expense":
            self.dismiss(None)
            return

        if event.button.id != "save-expense":
            return

        category = str(self.query_one("#category-select", Select).value)
        subcategory = str(self.query_one("#subcategory-select", Select).value)
        date = self.query_one("#date-input", Input).value.strip()
        amount = self.query_one("#amount-input", Input).value.strip().replace("$", "")

        if not date or not amount:
            self.notify("Date and amount are required", severity="error")
            return

        if parse_yyyy_mm_dd(date) is None:
            self.notify("Date must use YYYY-MM-DD", severity="error")
            return

        try:
            float(amount)
        except ValueError:
            self.notify("Amount must be a number", severity="error")
            return

        self.dismiss(
            {
                "category": category,
                "subcategory": subcategory,
                "date": date,
                "amount": amount,
            }
        )


class FilterExpenseScreen(ModalScreen[ExpenseRecord | None]):
    """Modal form for filtering expenses by date and category."""

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Filter Expenses", id="modal-title"),
            Static("From Date"),
            Input(placeholder="YYYY-MM-DD", id="from-date-input"),
            Static("To Date"),
            Input(placeholder="YYYY-MM-DD", id="to-date-input"),
            Static("Category"),
            Select(
                [("All", "")]
                + [(category.title(), category) for category in CATEGORIES],
                value="",
                id="filter-category-select",
            ),
            Static("Subcategory"),
            Select(
                [("All", "")],
                value="",
                id="filter-subcategory-select",
            ),
            Horizontal(
                Button("Apply", id="apply-filter", variant="success"),
                Button("Cancel", id="cancel-filter"),
                id="modal-buttons",
            ),
            id="filter-expense-modal",
        )

    @on(Select.Changed, "#filter-category-select")
    def update_filter_subcategories(self, event: Select.Changed) -> None:
        subcategory_select = self.query_one("#filter-subcategory-select", Select)

        if event.value == "":
            subcategory_select.set_options([("All", "")])
            subcategory_select.value = ""
            return

        category = str(event.value)
        subcategories = CATEGORIES[category]
        subcategory_select.set_options(
            [("All", "")]
            + [(subcategory, subcategory) for subcategory in subcategories]
        )
        subcategory_select.value = ""

    def on_focus(self, event: events.Focus) -> None:
        if event.widget.id not in {"from-date-input", "to-date-input"}:
            return

        date_input = self.query_one(f"#{event.widget.id}", Input)
        date_input.value = date_input.value.replace("-", "")

    @on(Input.Blurred, "#from-date-input")
    @on(Input.Blurred, "#to-date-input")
    def filter_date_input_blurred(self, event: Input.Blurred) -> None:
        raw_value = event.input.value.replace("-", "").strip()

        if not raw_value:
            return

        digits = ""

        for char in raw_value:
            if char.isdigit():
                if len(digits) < 8:
                    digits += char
                else:
                    event.input.value = ""
                    self.notify("Date cannot be more than 8 digits", severity="error")
                    return
            else:
                event.input.value = ""
                self.notify("Only numbers are valid for date", severity="error")
                return

        if len(digits) != 8:
            event.input.value = ""
            self.notify("Date must be 8 digits: YYYYMMDD", severity="error")
            return

        formatted_date = f"{digits[:4]}-{digits[4:6]}-{digits[6:]}"

        if parse_yyyy_mm_dd(formatted_date) is None:
            event.input.value = ""
            self.notify("Date is not valid", severity="error")
            return

        event.input.value = formatted_date

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel-filter":
            self.dismiss(None)
            return

        if event.button.id != "apply-filter":
            return

        date_from = self.query_one("#from-date-input", Input).value.strip()
        date_to = self.query_one("#to-date-input", Input).value.strip()
        category = str(self.query_one("#filter-category-select", Select).value or "")
        subcategory = str(
            self.query_one("#filter-subcategory-select", Select).value or ""
        )

        if date_from and parse_yyyy_mm_dd(date_from) is None:
            self.notify("From date must use YYYY-MM-DD", severity="error")
            return

        if date_to and parse_yyyy_mm_dd(date_to) is None:
            self.notify("To date must use YYYY-MM-DD", severity="error")
            return

        self.dismiss(
            {
                "date_from": date_from,
                "date_to": date_to,
                "category": category,
                "subcategory": subcategory,
            }
        )
