"""Shared state for the expense TUI."""

from dataclasses import dataclass, field

from expenses.memory.core import ExpenseMemory
from expenses.memory.types import ExpenseRecord


@dataclass
class ExpenseState:
    """Mutable state owned by the TUI app."""

    memory: ExpenseMemory = field(default_factory=ExpenseMemory)
    active_records: list[ExpenseRecord] | None = None
    selected_expense_ids: set[int] = field(default_factory=set)
