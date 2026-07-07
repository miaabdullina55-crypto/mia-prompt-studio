from collections import defaultdict


# Хранилище данных пользователей
# user_data[user_id] =
# {
#     "style": "...",
#     "category": "...",
#     "template": "...",
#     "texts": {
#         "TEXT1": "...",
#         "TEXT2": "...",
#     }
# }

user_data = defaultdict(
    lambda: {
        "style": None,
        "category": None,
        "template": None,
        "texts": {}
    }
)


def get_user(user_id: int):
    """Получить данные пользователя."""
    return user_data[user_id]


def clear_texts(user_id: int):
    """Очистить введенные тексты."""
    user_data[user_id]["texts"] = {}


def clear_all(user_id: int):
    """Полностью очистить данные пользователя."""
    user_data[user_id] = {
        "style": None,
        "category": None,
        "template": None,
        "texts": {}
    }