from __future__ import annotations

from datetime import datetime
from typing import Any


ExpenseRecord = dict[str, Any]

_expense_store: list[ExpenseRecord] = []


def parse_yyyy_mm_dd(value: str) -> datetime | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


def _next_expense_id() -> int:
    if not _expense_store:
        return 1
    return max(int(expense.get("id", 0)) for expense in _expense_store) + 1


def _normalize_datetime(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return parse_yyyy_mm_dd(value)
    return None


class ExpenseMemory:
    def add_expense(self, expense: ExpenseRecord) -> ExpenseRecord:
        record = dict(expense)

        if not record.get("id"):
            record["id"] = _next_expense_id()

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

    def delete_expense(self, expense_id: int) -> bool:
        for index, expense in enumerate(_expense_store):
            if int(expense.get("id", 0)) == expense_id:
                del _expense_store[index]
                return True
        return False

    def view_all_expenses(self) -> list[ExpenseRecord]:
        return [dict(expense) for expense in _expense_store]

    def view_expense(self, expense_id: int) -> ExpenseRecord | None:
        for expense in _expense_store:
            if int(expense.get("id", 0)) == expense_id:
                return dict(expense)
        return None

    def get_expenses_by_datetime(
        self,
        datetime_from: datetime,
        datetime_to: datetime,
    ) -> list[ExpenseRecord]:
        return [
            dict(expense)
            for expense in _expense_store
            if datetime_from <= expense["date"] <= datetime_to
        ]

    def filter_expenses(
        self,
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

    def get_expense_count(self) -> int:
        return len(_expense_store)

    def get_total_amount(self, records: list[ExpenseRecord] | None = None) -> float:
        expenses = _expense_store if records is None else records
        return sum(float(expense.get("amount", 0)) for expense in expenses)

    def clear(self) -> None:
        _expense_store.clear()
