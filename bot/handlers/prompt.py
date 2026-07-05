from pathlib import Path


def load_prompt(template_name):

    file = Path(f"prompts/{template_name}.txt")

    return file.read_text(encoding="utf-8")


def get_fields_count(template_name):

    prompt = load_prompt(template_name)

    for line in prompt.splitlines():

        line = line.strip()

        if line.startswith("FIELDS="):
            return int(line.replace("FIELDS=", "").strip())

    return 5


def generate_prompt(template_name, values):

    prompt = load_prompt(template_name)

    for key, value in values.items():

        prompt = prompt.replace(
            f"{{{{{key}}}}}",
            value
        )

    return prompt