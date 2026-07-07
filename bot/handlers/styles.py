from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes


STYLE_LIST = [
    ("premium_luxury.jpg", "💎 Premium Luxury", "premium_luxury"),
    ("emerald_luxe.jpg", "🌿 Emerald Luxe", "emerald_luxe"),
    ("chocolate_royal.jpg", "🍫 Chocolate Royal", "chocolate_royal"),
    ("wine_prestige.jpg", "🍷 Wine Prestige", "wine_prestige"),
    ("pink_vogue.jpg", "🌸 Pink Vogue", "pink_vogue"),
    ("y2k.jpg", "✨ Y2K", "y2k"),
    ("natural_glow.jpg", "🌾 Natural Glow", "natural_glow"),
    ("imperial_red.jpg", "❤️ Imperial Red", "imperial_red"),
]


async def styles(update: Update, context: ContextTypes.DEFAULT_TYPE):

    for i, (filename, title, callback) in enumerate(STYLE_LIST):

        keyboard = [
            [
                InlineKeyboardButton(
                    text="✅ Выбрать стиль",
                    callback_data=callback,
                )
            ]
        ]

        # Только под последней картинкой добавляем кнопку "Назад"
        if i == len(STYLE_LIST) - 1:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="back",
                    )
                ]
            )

        reply_markup = InlineKeyboardMarkup(keyboard)

        with open(f"images/styles/{filename}", "rb") as photo:

            await update.message.reply_photo(
                photo=photo,
                caption=title,
                reply_markup=reply_markup,
            )