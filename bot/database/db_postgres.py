import os
import psycopg2

from bot.config import FREE_PROMPTS


def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


def create_tables():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (

            telegram_id BIGINT PRIMARY KEY,

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
    created_at,
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users
        (
            telegram_id,
            username,
            first_name,
            free_left,
            paid_until,
            created_at
        )
        VALUES (%s, %s, %s, %s, NULL, %s)
        ON CONFLICT (telegram_id) DO NOTHING
        """,
        (
            telegram_id,
            username,
            first_name,
            FREE_PROMPTS,
            created_at,
        ),
    )

    conn.commit()
    conn.close()


def get_user(telegram_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE telegram_id = %s
        """,
        (telegram_id,),
    )

    user = cur.fetchone()

    conn.close()

    return user


def update_free_left(
    telegram_id,
    free_left,
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET free_left = %s
        WHERE telegram_id = %s
        """,
        (
            free_left,
            telegram_id,
        ),
    )

    conn.commit()
    conn.close()


def update_paid_until(
    telegram_id,
    paid_until,
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET paid_until = %s
        WHERE telegram_id = %s
        """,
        (
            paid_until,
            telegram_id,
        ),
    )

    conn.commit()
    conn.close()