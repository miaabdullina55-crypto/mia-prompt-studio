import re

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from bot.handlers.prompt import (
    generate_prompt,
    get_fields_count,
)
from bot.handlers.result import save_prompt
from bot.handlers.instruction import load_instruction

from bot.database.users import (
    has_free_prompts,
    decrease_free_prompts,
)

from bot.database.premium import is_premium

from bot.config import (
    CONTACT_USERNAME,
    SUBSCRIPTION_PRICE,
    SUBSCRIPTION_PERIOD,
)


def parse_user_text(text: str):

    pattern = r"ТЕКСТ(\d+)\s*:\s*\{\{(.*?)\}\}"

    matches = re.findall(pattern, text, re.DOTALL)

    data = {}

    for num, value in matches:
        data[f"TEXT{num}"] = value.strip()

    return data


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    user_text = update.message.text

    premium = is_premium(user_id)

    # Проверяем остаток бесплатных промптов только для бесплатного тарифа
    if not premium and not has_free_prompts(user_id):

        await update.message.reply_text(
            "🎁 Бесплатные промпты закончились.\n\n"
            "Для продления доступа напишите:\n\n"
            f"👉 {CONTACT_USERNAME}\n\n"
            f"Стоимость доступа:\n"
            f"{SUBSCRIPTION_PRICE} / {SUBSCRIPTION_PERIOD}"
        )

        return

    parsed = parse_user_text(user_text)

    template = context.user_data.get(
        "template",
        "premium_luxury_0001"
    )

    fields_count = get_fields_count(template)

    errors = []

    for i in range(1, fields_count + 1):

        field = f"TEXT{i}"

        pattern = rf"ТЕКСТ{i}\s*:\s*\{{\{{.*?\}}\}}"

        if not re.search(pattern, user_text, re.DOTALL):

            errors.append(field)

        elif field not in parsed or not parsed[field]:

            errors.append(field)

    if errors:

        text = (
            "❌ Обнаружены ошибки.\n\n"
            "Каждый текст должен быть записан внутри двойных фигурных скобок.\n\n"
            "Пример:\n\n"
            "ТЕКСТ1:{{Ваш текст}}\n\n"
            "Исправьте:\n"
        )

        for field in errors:
            text += f"\n• {field}"

        await update.message.reply_text(text)

        return

    prompt = generate_prompt(
        template,
        parsed
    )

    save_prompt(prompt)

    # Для Premium ничего не списываем
    if premium:
        free_left = -1
    else:
        free_left = decrease_free_prompts(user_id)

    instruction = load_instruction(template)

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📥 Скачать PROMPT (.txt)",
                    callback_data="download_prompt",
                )
            ],
            [
                InlineKeyboardButton(
                    "🚀 Перейти в ChatGPT",
                    url="https://chatgpt.com",
                )
            ],
        ]
    )

    if premium:

        text = (
            f"{instruction}\n\n"
            "💎 Premium активен.\n"
            "Безлимитное создание PROMPT."
        )

    elif free_left > 0:

        text = (
            f"{instruction}\n\n"
            f"🎁 Осталось бесплатных промптов: {free_left} из 3"
        )

    else:

        text = (
            f"{instruction}\n\n"
            "🎁 Это был ваш последний бесплатный промпт.\n\n"
            "Следующий PROMPT будет доступен после активации доступа."
        )

    await update.message.reply_text(
        text,
        reply_markup=keyboard,
    )