import os
import psycopg2


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