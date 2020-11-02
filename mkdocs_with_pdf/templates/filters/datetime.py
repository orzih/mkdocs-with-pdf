from datetime import date, datetime


def strptime(value: str, format) -> date:
    return datetime.strptime(value, format)


def strftime(value, format) -> str:
    return value.strftime(format)
