from telegram import Update
from telegram.ext import ContextTypes

from bot.config import (
    SUBSCRIPTION_PRICE,
    SUBSCRIPTION_PERIOD,
    CONTACT_USERNAME,
)

from bot.database.premium import (
    is_premium,
    get_premium_until,
)


async def cabinet(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    # Premium активен
    if is_premium(user_id):

        paid_until = get_premium_until(user_id)

        await update.message.reply_text(
            "👤 Личный кабинет\n\n"

            "💎 Статус\n"
            "Premium активен\n\n"

            "📅 Действует до\n"
            f"{paid_until}\n\n"

            "━━━━━━━━━━━━━━\n\n"

            "🆔 Ваш ID\n"
            f"{user_id}"
        )

        return

    # Premium отсутствует
    await update.message.reply_text(
        "👤 Личный кабинет\n\n"

        "🔒 Подписка не активна\n\n"

        "Для просмотра и получения\n"
        "готовых PROMPT необходима\n"
        "подписка MIA Prompt Studio Premium.\n\n"

        "━━━━━━━━━━━━━━\n\n"

        "💎 MIA Prompt Studio Premium\n\n"

        "✔ Неограниченный доступ\n"
        "ко всем PROMPT\n\n"

        "✔ Все новые шаблоны\n\n"

        "✔ Регулярные обновления\n\n"

        f"💳 {SUBSCRIPTION_PRICE} / {SUBSCRIPTION_PERIOD}\n\n"

        "📩 Для подключения\n"
        f"{CONTACT_USERNAME}\n\n"

        "━━━━━━━━━━━━━━\n\n"

        "🆔 Ваш ID\n"
        f"{user_id}"
    )