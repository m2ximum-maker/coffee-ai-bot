import os
import sqlite3

from typing import Optional
from datetime import datetime

def db_path() -> str:
    path = os.getenv("DB_PATH")

    if path is None:
        raise ValueError("DB_PATH не найден в .env")

    return path


def get_connection():
    return sqlite3.connect(db_path())


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount INTEGER NOT NULL,
                drink TEXT NOT NULL,
                coffee_shop TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()

def add_expense(user_id: int, amount: int, drink: str, coffee_shop: Optional[str] = None) -> None:
    with sqlite3.connect(db_path()) as conn:
        conn.execute(
            """
            INSERT INTO expenses (user_id, amount, drink, coffee_shop, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                amount,
                drink,
                coffee_shop,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        conn.commit()


def delete_expense(user_id: int, expense_id: int) -> bool:
    with sqlite3.connect(db_path()) as conn:
        cursor = conn.execute(
            """
            DELETE FROM expenses
            WHERE id = ? AND user_id = ?
            """,
            (expense_id, user_id),
        )
        conn.commit()

        return cursor.rowcount > 0


def get_expenses(user_id: int) -> list[tuple[int, int, int, str, Optional[str], str]]:
    with sqlite3.connect(db_path()) as conn:
        return conn.execute(
            """
            SELECT id, user_id, amount, drink, coffee_shop, created_at
            FROM expenses
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchall()

def get_total_expenses(user_id: int) -> int:
    with sqlite3.connect(db_path()) as conn:
        result = conn.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        total = result[0]

        return total if total is not None else 0
