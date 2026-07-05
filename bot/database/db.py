import sqlite3
from pathlib import Path

from bot.config import FREE_PROMPTS


DB_FILE = Path("mia.db")


def connect():
    return sqlite3.connect(DB_FILE)


def create_tables():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            telegram_id INTEGER PRIMARY KEY,

            username TEXT,

            first_name TEXT,

            free_left INTEGER NOT NULL DEFAULT 3,

            paid_until TEXT,

            created_at TEXT

        )
    """)

    conn.commit()
    conn.close()


def add_user(
    telegram_id,
    username,
    first_name,
    created_at
):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO users
        (
            telegram_id,
            username,
            first_name,
            free_left,
            paid_until,
            created_at
        )
        VALUES (?, ?, ?, ?, NULL, ?)
        """,
        (
            telegram_id,
            username,
            first_name,
            FREE_PROMPTS,
            created_at,
        )
    )

    conn.commit()
    conn.close()


def get_user(telegram_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def user_exists(telegram_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    exists = cursor.fetchone() is not None

    conn.close()

    return exists


def update_free_left(
    telegram_id,
    free_left
):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET free_left = ?
        WHERE telegram_id = ?
        """,
        (
            free_left,
            telegram_id,
        )
    )

    conn.commit()
    conn.close()


def update_paid_until(
    telegram_id,
    paid_until
):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET paid_until = ?
        WHERE telegram_id = ?
        """,
        (
            paid_until,
            telegram_id,
        )
    )

    conn.commit()
    conn.close()