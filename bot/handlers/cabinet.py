from telegram import Update
from telegram.ext import ContextTypes

from bot.config import (
    SUBSCRIPTION_PRICE,
    SUBSCRIPTION_PERIOD,
    CONTACT_USERNAME,
)

from bot.database.users import get_free_prompts
from bot.database.premium import (
    is_premium,
    get_premium_until,
)


async def cabinet(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    # Если Premium активен
    if is_premium(user_id):

        paid_until = get_premium_until(user_id)

        await update.message.reply_text(
            "👤 Личный кабинет\n\n"

            "💎 Тариф\n"
            "Premium\n\n"

            "📅 Действует до\n"
            f"{paid_until}\n\n"

            "━━━━━━━━━━━━━━\n\n"

            "🆔 Ваш ID\n"
            f"{user_id}"
        )

        return

    # Бесплатный тариф
    free_left = get_free_prompts(user_id)

    if free_left == 1:
        free_text = "1 бесплатный промпт"
    elif 2 <= free_left <= 4:
        free_text = f"{free_left} бесплатных промпта"
    else:
        free_text = f"{free_left} бесплатных промптов"

    await update.message.reply_text(
        "👤 Личный кабинет\n\n"

        "🎁 Тариф\n"
        "Бесплатный\n\n"

        "📝 Осталось\n"
        f"{free_text}\n\n"

        "━━━━━━━━━━━━━━\n\n"

        "💎 Продлить доступ\n\n"

        f"{SUBSCRIPTION_PRICE} / {SUBSCRIPTION_PERIOD}\n\n"

        "✉️ Для оформления доступа\n"
        f"{CONTACT_USERNAME}\n\n"

        "🆔 Ваш ID\n"
        f"{user_id}\n\n"

        "Отправьте этот номер для активации Premium."
    )