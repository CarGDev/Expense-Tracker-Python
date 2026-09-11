from expenses.memory.types import ExpenseRecord


def delete_expense_fn(
    self, expense_id: int, _expense_store: list[ExpenseRecord]
) -> bool:
    for index, expense in enumerate(_expense_store):
        if int(expense.get("id", 0)) == expense_id:
            del _expense_store[index]
            return True
    return False
