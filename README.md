# 💰 Python Expense Tracker

A beginner-friendly, command-line Expense Tracker built with Python. It helps users manage their income and expenses, track monthly spending, set budgets, and export transactions to CSV.

## Features

- Add income and expenses
- View transaction history
- Calculate total income, expenses, and balance
- Search transactions by category
- Delete transactions
- Edit existing transactions
- Generate monthly financial summaries
- Export transactions to CSV for Excel
- Set monthly spending budgets
- View budget usage and remaining balance
- Save data using JSON files

## Technologies Used

- Python
- JSON (data storage)
- CSV (transaction export)
- VS Code

## Project Structure

```text
Expense tracker/
│
├── main.py
├── tracker.py
├── budget.py
├── transactions.csv
├── transactions.json
├── budget.json
└── README.md
```

## How to Run

1. Install Python on your computer.
2. Clone or download this repository.
3. Open the project folder in VS Code.
4. Open the terminal in the project directory.
5. Run:

```bash
python main.py
```

## Data Storage

Transactions and budgets are stored locally in JSON files:

- `transactions.json` – stores income and expense records.
- `budget.json` – stores monthly budgets.

Transactions can also be exported to `transactions.csv` for viewing in spreadsheet applications.

## Purpose

This project was created to practice Python programming, including functions, lists, dictionaries, loops, conditional statements, exception handling, file handling, JSON, and modular programming.

---

**Built as a Python learning project.

