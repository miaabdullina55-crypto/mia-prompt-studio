from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.config import TOKEN

# SQLite (пока оставляем)
from bot.database.db import create_tables

# ВРЕМЕННАЯ ПРОВЕРКА PostgreSQL
from bot.database.db_postgres import get_connection

from bot.handlers.start import start
from bot.handlers.menu import menu
from bot.handlers.styles import styles
from bot.handlers.callbacks import button_click
from bot.handlers.input import handle_text
from bot.handlers.cabinet import cabinet
from bot.handlers.premium import premium


def main():

    # Создаем SQLite (пока не удаляем)
    create_tables()

    # ======================================
    # Проверка подключения к PostgreSQL
    # ======================================
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    print("✅ POSTGRES CONNECTED")
    conn.close()
    # ======================================

    # Запускаем Telegram-бота
    app = Application.builder().token(TOKEN).build()

    # /start
    app.add_handler(
        CommandHandler("start", start)
    )

    # /premium
    app.add_handler(
        CommandHandler("premium", premium)
    )

    # Главное меню
    app.add_handler(
        MessageHandler(
            filters.Regex("^🪄 Создать промпт$"),
            menu
        )
    )

    # Личный кабинет
    app.add_handler(
        MessageHandler(
            filters.Regex("^👤 Личный кабинет$"),
            cabinet
        )
    )

    # Выбор стиля
    app.add_handler(
        MessageHandler(
            filters.Regex("^🎨 Выбрать фирменный стиль$"),
            styles
        )
    )

    # Callback-кнопки
    app.add_handler(
        CallbackQueryHandler(button_click)
    )

    # Ввод текста пользователя
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    print("