from datetime import datetime

from bot.database.db_postgres import (
    add_user,
    get_user,
    update_free_left,
    update_paid_until,
)


def register_user(user):

    if get_user(user.id) is None:

        add_user(
            telegram_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )


def get_user_data(user_id):

    return get_user(user_id)


def get_free_prompts(user_id):

    user = get_user(user_id)

    if user is None:
        return 0

    return int(user[3])


def has_free_prompts(user_id):

    return get_free_prompts(user_id) > 0


def decrease_free_prompts(user_id):

    free = get_free_prompts(user_id)

    if free <= 0:
        return 0

    free -= 1

    update_free_left(
        user_id,
        free,
    )

    return free


def activate_subscription(user_id, paid_until):

    update_paid_until(
        user_id,
        paid_until,
    )