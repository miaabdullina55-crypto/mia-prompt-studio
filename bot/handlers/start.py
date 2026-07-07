from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.config import FREE_PROMPTS
from bot.database.users import register_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Автоматическая регистрация пользователя
    register_user(update.effective_user)

    keyboard = [
        ["🪄 Создать промпт"],
        ["👥 Вступить в чат"],
        ["❓ Как пользоваться"],
        ["👤 Личный кабинет"],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "Добро пожаловать в MIA Prompt Studio 💜\n\n"

        "Создавайте стильные дизайны для своего бизнеса "
        "с помощью профессиональных промптов для ChatGPT.\n\n"

        "Все промпты можно использовать "
        "в БЕСПЛАТНОЙ версии ChatGPT.\n\n"

        "✨ Нейрофото\n"
        "✨ Баннеры\n"
        "✨ Коллажи\n"
        "✨ Прайсы\n"
        "✨ Оформление ВКонтакте\n"
        "✨ Instagram\n\n"

        f"🎁 Вам доступны {FREE_PROMPTS} бесплатных промпта.\n\n"

        "👇 Начнём?",

        reply_markup=reply_markup
    )