from datetime import datetime
from typing import Any

from expenses.memory.types import ExpenseRecord


def parse_yyyy_mm_dd(value: str) -> datetime | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


def _next_expense_id(_expense_store: list[ExpenseRecord]) -> int:
    if not _expense_store:
        return 1
    return max(int(expense.get("id", 0)) for expense in _expense_store) + 1


def _normalize_datetime(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return parse_yyyy_mm_dd(value)
    return None
