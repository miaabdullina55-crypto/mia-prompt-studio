from pathlib import Path


def load_instruction(template_name):

    file = Path(f"instructions_text/{template_name}.txt")

    if file.exists():
        return file.read_text(encoding="utf-8")

    return (
        "1. Перейдите в ChatGPT.\n\n"
        "2. Первым загрузите ваше заранее подготовленное фото.\n\n"
        "3. Вторым и третьим загрузите фотографии продуктов, относящиеся к вашей нише.\n\n"
        "4. Нажмите «📥 Скачать PROMPT (.txt)», затем загрузите его в этот же чат ChatGPT."
    )