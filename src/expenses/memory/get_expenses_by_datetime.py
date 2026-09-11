from datetime import datetime

from expenses.memory.types import ExpenseRecord


def get_expenses_by_datetime_fn(
    self,
    datetime_from: datetime,
    datetime_to: datetime,
    _expense_store: list[ExpenseRecord],
) -> list[ExpenseRecord]:
    return [
        dict(expense)
        for expense in _expense_store
        if datetime_from <= expense["date"] <= datetime_to
    ]
