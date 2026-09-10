# Expense Tracker — Python Implementation

By **Carlos Gutierrez** — Semester 4, Week 3.

> This repository implements the **Python track** of the assignment. The course assigns the same application in two languages to compare how each handles data structures, memory management, concurrency, and error handling.

## 1. Assignment Context

**Python 1 — Project Overview:** each group designs and implements an application with specific requirements in two assigned languages, emphasizing language-specific features.

**Option 1 assigned here: Expense Tracker** — record, view, and categorize expenses; filter by date/category; calculate totals.

The brief gives language examples:

* **Python:** `dict` storage, dynamic typing, `datetime`.
* **C++:** `struct`/`class` for expenses, STL containers, explicit memory management.

This repo is the **Python implementation** — C++ counterpart: [CarGDev/Expense-Tracker-Cpp](https://github.com/CarGDev/Expense-Tracker-Cpp).

## 2. Core Requirements

* **Data storage** — expense with `date`, `amount`, `category`, `description` → `dict`-based records with `datetime` handling in `src/expenses/`
* **Filter & search** — by date range and category/subcategory (via `textual` TUI filtering)
* **Summary** — total by category and overall

## 3. Python Highlights

* Dynamic `dict` storage vs C++ strongly-typed `struct ExpenseRecord`
* Dynamic typing and duck typing for flexible expense handling
* `datetime` standard library for date parsing and range filtering
* Simple, Pythonic error handling for user input validation
* Terminal UI with `textual` (`src/expenses/menu.py:1`, `src/expenses/__main__.py:1`)

## 4. Project Structure

```
src/
  expenses/
    __init__.py            # package entry, version
    __main__.py            # python -m expenses entry point
    cli.py                 # CLI placeholder / future extension
    menu.py                # textual App, layout & bindings
pyproject.toml             # setuptools config, textual optional dep [menu], entry point `expenses`
LICENSE                    # MIT
```

## 5. Prerequisites

* Python `>=3.10`, `pip`
* Optional TUI dependency: `textual` (installed via `[menu]` extra)

## 6. Install & Run

Install with optional menu (TUI) dependency:

```bash
pip install -e ".[menu]"
```

Run the application:

```bash
python -m expenses
```

Or, after installation via entry point:

```bash
expenses
```

## 7. Usage (TUI)

* `textual` app defined in `src/expenses/menu.py:5` (`Expenses` App)
* Header/Footer chrome with title `Expense Tracker`
* `q` — quit application (`BINDINGS` in `src/expenses/menu.py:8`)
* Welcome screen placeholder — extend `compose()` to add add/filter/summary views to match the C++ TUI feature parity

> The C++ version provides a full `ncurses` layout with `add_expense` / `get_expenses` / `remove_expenses` flows; the Python `textual` implementation mirrors the same workflows idiomatically — add this parity as the app evolves.

## 8. License

MIT © 2026 Carlos Gutierrez — see [LICENSE](./LICENSE).
