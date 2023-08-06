from datetime import datetime


class DateFormats:
    date_path = "%Y/%m/%d"
    date = "%Y-%m-%d"
    timestamp = "%Y%m%d_%H%M%s"


def archive_date_today():
    return datetime.today().strftime(DateFormats.date_path)


def current_date():
    return datetime.today().strftime(DateFormats.date)


def current_timestamp():
    return datetime.today().strftime(DateFormats.timestamp)
