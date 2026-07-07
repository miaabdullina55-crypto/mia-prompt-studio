import os

print("=" * 60)
print("PROJECT FOLDER:", os.getcwd())
print("=" * 60)

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.config import TOKEN

from bot.database.db_postgres import get_connection

from bot.handlers.start import start
from bot.handlers.menu import menu
from bot.handlers.styles import styles
from bot.handlers.callbacks import button_click
from bot.handlers.input import handle_text
from bot.handlers.cabinet import cabinet
from bot.handlers.premium import premium


def main():

    # ======================================
    # ПРОВЕРКА POSTGRESQL
    # ======================================
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        print("✅ POSTGRES CONNECTED")
        conn.close()
    except Exception as e:
        print("❌ DB ERROR:", e)
    # ======================================

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("premium", premium))

    app.add_handler(
        MessageHandler(filters.Regex("^🪄 Создать промпт$"), menu)
    )

    app.add_handler(
        MessageHandler(filters.Regex("^👤 Личный кабинет$"), cabinet)
    )

    app.add_handler(
        MessageHandler(filters.Regex("^🎨 Выбрать фирменный стиль$"), styles)
    )

    app.add_handler(CallbackQueryHandler(button_click))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )

    print("🤖 Бот запущен")

    app.run_polling()


if __name__ == "__main__":
    main()