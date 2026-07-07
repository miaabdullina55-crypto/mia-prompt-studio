from telegram import Update
from telegram.ext import ContextTypes

from bot.config import ADMIN_ID
from bot.database.premium import activate_premium


async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Команду может использовать только администратор
    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "⛔ У вас нет доступа к этой команде."
        )

        return

    # Проверяем, указан ли ID пользователя
    if len(context.args) != 1:

        await update.message.reply_text(
            "Использование:\n\n"
            "/premium ID_ПОЛЬЗОВАТЕЛЯ\n\n"
            "Пример:\n"
            "/premium 123456789"
        )

        return

    try:
        user_id = int(context.args[0])

    except ValueError:

        await update.message.reply_text(
            "❌ ID должен состоять только из цифр."
        )

        return

    # Активируем Premium
    paid_until = activate_premium(user_id)

    # Сообщение администратору
    await update.message.reply_text(
        "✅ Premium успешно активирован!\n\n"
        f"ID: {user_id}\n\n"
        f"Действует до:\n{paid_until}"
    )

    # Сообщение пользователю
    try:

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "🎉 Поздравляем!\n\n"
                "Ваш Premium успешно активирован!\n\n"
                f"📅 Доступ открыт до:\n{paid_until}\n\n"
                "Спасибо, что пользуетесь\n"
                "MIA Prompt Studio 💜"
            )
        )

    except Exception:
        # Если пользователь ещё ни разу не запускал бота
        pass