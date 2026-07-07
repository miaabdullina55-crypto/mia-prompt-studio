from pathlib import Path

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def show_gallery(query, style):

    folder = Path("images/banners")

    print("STYLE =", repr(style))
    print("FOUND =", [p.name for p in folder.glob(f"{style}_*.jpg")])

    banners = sorted(
        folder.glob(f"{style}_*.jpg")
    )

    if not banners:

        await query.message.reply_text(
            "❌ Для этого стиля пока нет шаблонов."
        )
        return

    for banner in banners:

        template = banner.stem

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Выбрать",
                        callback_data=f"template:{template}",
                    )
                ]
            ]
        )

        with open(banner, "rb") as photo:

            await query.message.reply_photo(
                photo=photo,
                reply_markup=keyboard,
            )

    back_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⬅️ Назад",
                    callback_data="back",
                )
            ]
        ]
    )

    await query.message.reply_text(
        "Конец списка шаблонов.",
        reply_markup=back_keyboard,
    )
