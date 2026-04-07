# Expense Tracker — Python + SQLite

A desktop application to log, view, and manage personal expenses. The app stores data in a local SQLite database and generates a monthly category-wise spending summary with basic insights.

Built as a personal learning project to apply database operations and Python fundamentals in a working application.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Database | SQLite3 |
| Interface | Tkinter + ttk |

## Features

- Add expenses with category, amount, date, and description
- View all recorded expenses sorted by latest date first
- Delete any selected expense by its unique ID
- Monthly spending summary broken down by category
- Flags if any category exceeds 40% of total monthly spend
- Data persists in a local file — survives app restarts

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS expenses (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category    TEXT    NOT NULL,
    amount      REAL    NOT NULL,
    date        TEXT    NOT NULL,
    description TEXT
);
```

## Backend Logic

The core of the project is four database functions built around standard CRUD operations.

**Add** — Reads user input, converts amount from string to float, and inserts into the database using parameterized queries to avoid SQL injection. Wrapped in try-except so the app doesn't crash on bad input.

**Read** — Fetches all records ordered by date descending and returns them as a list of tuples for the table to render.

**Delete** — Removes a record by its primary key `id`, not by value, so only the exact selected row is affected.

**Monthly Summary** — Filters the current month using `WHERE date LIKE 'YYYY-MM%'`, then groups and totals spending per category using Python's `defaultdict`. Calculates each category's percentage share and applies a threshold alert if any single category crosses 40% of total spend.

## Project Structure

```
expense-tracker-python/
├── expense_tracker.py
├── README.md
└── .gitignore
```

`expenses.db` is excluded via `.gitignore` and gets created automatically on first run.

## Getting Started

Python 3 is the only requirement. No external libraries needed.

```bash
git clone https://github.com/ayushgautam266atwork/expense-tracker-python.git
cd expense-tracker-python
python expense_tracker.py
```

## Author

**Ayush Gautam**
B.Tech Computer Science — AKGEC Ghaziabad
Aspiring Data Analyst

[LinkedIn](https://www.linkedin.com/in/ayush-gautam-071a4b28b) · [GitHub](https://github.com/ayushgautam266atwork)
