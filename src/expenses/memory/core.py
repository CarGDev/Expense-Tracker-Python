from __future__ import annotations

from datetime import datetime

from expenses.memory.add_expenses import add_expense_fn
from expenses.memory.delete_expenses import delete_expense_fn
from expenses.memory.filter_expenses import filter_expenses_fn
from expenses.memory.get_expenses_by_datetime import get_expenses_by_datetime_fn
from expenses.memory.store import _expense_store
from expenses.memory.types import ExpenseRecord
from expenses.memory.view_expenses import view_expense_fn


class ExpenseMemory:
    def add_expense(self, expense: ExpenseRecord) -> ExpenseRecord:
        return add_expense_fn(self, expense, _expense_store)

    def delete_expense(self, expense_id: int) -> bool:
        return delete_expense_fn(self, expense_id, _expense_store)

    def view_all_expenses(self) -> list[ExpenseRecord]:
        return [dict(expense) for expense in _expense_store]

    def view_expense(self, expense_id: int) -> ExpenseRecord | None:
        return view_expense_fn(self, expense_id, _expense_store)

    def get_expenses_by_datetime(
        self,
        datetime_from: datetime,
        datetime_to: datetime,
    ) -> list[ExpenseRecord]:
        return get_expenses_by_datetime_fn(
            self, datetime_from, datetime_to, _expense_store
        )

    def filter_expenses(
        self,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        category: str | None = None,
        subcategory: str | None = None,
    ) -> list[ExpenseRecord]:
        return filter_expenses_fn(
            self, _expense_store, date_from, date_to, category, subcategory
        )

    def get_expense_count(self) -> int:
        return len(_expense_store)

    def get_total_amount(self, records: list[ExpenseRecord] | None = None) -> float:
        expenses = _expense_store if records is None else records
        return sum(float(expense.get("amount", 0)) for expense in expenses)

    def clear(self) -> None:
        _expense_store.clear()
