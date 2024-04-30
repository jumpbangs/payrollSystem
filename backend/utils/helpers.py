def is_true_value(value):
    if value in ("true", "True", "1"):
        return True
    return False


def is_none_or_empty(value):
    if value is None or value == "":
        return True
    return False


def is_user_manager_or_admin(user_role):
    return user_role == "M" or user_role == "A"


def is_user_admin(user_role):
    return user_role == "A"


def is_user_manager(user_role):
    return user_role == "M"


def is_user_staff(user_role):
    return user_role == "E"
