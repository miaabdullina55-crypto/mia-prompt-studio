from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.config import TOKEN
from bot.database.db import create_tables

from bot.handlers.start import start
from bot.handlers.menu import menu
from bot.handlers.styles import styles
from bot.handlers.callbacks import button_click
from bot.handlers.input import handle_text
from bot.handlers.cabinet import cabinet
from bot.handlers.premium import premium


def main():

    # Создаем базу данных и таблицы
    create_tables()

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

    print("✅ MIA Prompt Studio запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()