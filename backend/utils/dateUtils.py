from datetime import datetime

DATE_FORMAT_YYYY_MM_DD = "%Y-%m-%d"


def get_current_year():
    return datetime.now().year


def get_current_date():
    return datetime.now().strftime(DATE_FORMAT_YYYY_MM_DD)
