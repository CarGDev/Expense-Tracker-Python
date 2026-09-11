from expenses.memory.types import ExpenseRecord


def view_expense_fn(
    self, expense_id: int, _expense_store: list[ExpenseRecord]
) -> ExpenseRecord | None:
    for expense in _expense_store:
        if int(expense.get("id", 0)) == expense_id:
            return dict(expense)
    return None
