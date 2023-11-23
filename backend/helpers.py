
def is_true_value(value):
    if value in ("true", "True", "1"):
        return True
    return False

def is_none_or_empty(value):
    if value is None or value == "":
        return True
    return False
