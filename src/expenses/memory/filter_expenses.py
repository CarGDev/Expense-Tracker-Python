from datetime import datetime

from expenses.memory.types import ExpenseRecord


def filter_expenses_fn(
    self,
    _expense_store: list[ExpenseRecord],
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    category: str | None = None,
    subcategory: str | None = None,
) -> list[ExpenseRecord]:
    filtered: list[ExpenseRecord] = []

    for expense in _expense_store:
        if date_from is not None and expense["date"] < date_from:
            continue
        if date_to is not None and expense["date"] > date_to:
            continue
        if category and expense.get("category") != category:
            continue
        if subcategory and expense.get("subcategory") != subcategory:
            continue
        filtered.append(dict(expense))

    return filtered
