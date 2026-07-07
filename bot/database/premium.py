from datetime import datetime, timedelta

from bot.database.db_postgres import (
    get_user,
    update_paid_until,
)


def activate_premium(user_id: int, days: int = 30):

    paid_until = (
        datetime.now() +
        timedelta(days=days)
    ).strftime("%Y-%m-%d %H:%M:%S")

    update_paid_until(
        user_id,
        paid_until,
    )

    return paid_until


def is_premium(user_id: int):

    user = get_user(user_id)

    if user is None:
        return False

    paid_until = user[4]

    if not paid_until:
        return False

    try:
        expire = datetime.strptime(
            paid_until,
            "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        return False

    if expire < datetime.now():

        update_paid_until(
            user_id,
            None,
        )

        return False

    return True


def get_premium_until(user_id: int):

    user = get_user(user_id)

    if user is None:
        return None

    return user[4]