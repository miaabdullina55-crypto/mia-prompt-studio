from pathlib import Path


LAST_FILE = None


def save_prompt(prompt_text):

    global LAST_FILE

    output = Path("output")
    output.mkdir(exist_ok=True)

    file = output / "PROMPT.txt"

    file.write_text(
        prompt_text,
        encoding="utf-8"
    )

    LAST_FILE = str(file)

    return str(file)


def get_last_file():
    return LAST_FILE