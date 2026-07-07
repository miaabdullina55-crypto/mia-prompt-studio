from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from bot.handlers.gallery import show_gallery
from bot.handlers.form import create_form_text
from bot.handlers.result import get_last_file


STYLE_CALLBACKS = {
    "premium_luxury",
    "emerald_luxe",
    "chocolate_royal",
    "wine_prestige",
    "pink_vogue",
    "y2k",
    "natural_glow",
    "imperial_red",
}


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    print(f"CALLBACK = {query.data}")

    # ==========================================
    # Скачать PROMPT
    # ==========================================
    if query.data == "download_prompt":

        file = get_last_file()

        if file is None:

            await query.message.reply_text(
                "❌ Сначала создайте PROMPT."
            )

            return

        with open(file, "rb") as document:

            await query.message.reply_document(
                document=document,
                filename="PROMPT.txt"
            )

        return

    # ==========================================
    # Выбор фирменного стиля
    # ==========================================
    if query.data in STYLE_CALLBACKS:

        context.user_data["style"] = query.data

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🖼 Баннер", callback_data="banner")],
                [InlineKeyboardButton("📄 Прайс", callback_data="price")],
                [InlineKeyboardButton("🧩 Коллаж", callback_data="collage")],
                [InlineKeyboardButton("💙 ВКонтакте", callback_data="vk")],
                [InlineKeyboardButton("📷 Instagram", callback_data="instagram")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="back")],
            ]
        )

        await query.message.reply_text(
            "Что будем делать?",
            reply_markup=keyboard,
        )

        return

    # ==========================================
    # Баннер
    # ==========================================
    if query.data == "banner":

        context.user_data["category"] = "banner"

        await show_gallery(
            query,
            context.user_data["style"]
        )

        return

    # ==========================================
    # Выбран шаблон
    # ==========================================
    if query.data.startswith("template:"):

        template = query.data.replace("template:", "")

        context.user_data["template"] = template

        with open(f"images/instructions/{template}.jpg", "rb") as photo:

            await query.message.reply_photo(
                photo=photo,
                caption=create_form_text(template)
            )

        return

    # ==========================================
    # Назад
    # ==========================================
    if query.data == "back":

        await query.message.reply_text(
            "Возврат в меню."
        )

        return

    print("НЕИЗВЕСТНЫЙ CALLBACK =", query.data)