from expenses.memory.types import ExpenseRecord
from expenses.memory.utils import _next_expense_id, _normalize_datetime


def add_expense_fn(
    self, expense: ExpenseRecord, _expense_store: list[ExpenseRecord]
) -> ExpenseRecord:
    record = dict(expense)

    if not record.get("id"):
        record["id"] = _next_expense_id(_expense_store)

    parsed_datetime = _normalize_datetime(record.get("date"))
    if parsed_datetime is None:
        raise ValueError("Expense date must use YYYY-MM-DD")
    record["date"] = parsed_datetime

    try:
        record["amount"] = float(record.get("amount", 0))
    except (TypeError, ValueError) as exc:
        raise ValueError("Expense amount must be a number") from exc

    _expense_store.append(record)
    return record
