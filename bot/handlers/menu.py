from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["🎨 Выбрать фирменный стиль"],
        ["👤 Нейрофото"],
        ["⬅️ Назад"],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "Что будем делать?",
        reply_markup=reply_markup
    )