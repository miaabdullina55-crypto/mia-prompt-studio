from bot.handlers.prompt import get_fields_count


def create_form_text(template_name):

    count = get_fields_count(template_name)

    text = (
        "Введите данные в поле «Сообщение».\n\n"
        "Напечатайте текст так, как показано ниже.\n\n"
        "Номер текста соответствует номеру в кружке на изображении.\n\n"
    )

    for i in range(1, count + 1):

        text += f"ТЕКСТ{i}:{{{{        }}}}\n\n"

    return text