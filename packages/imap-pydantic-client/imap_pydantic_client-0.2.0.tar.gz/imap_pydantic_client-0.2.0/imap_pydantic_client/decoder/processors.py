from datetime import datetime
from email.utils import parsedate_to_datetime


def date_processor(date: str) -> datetime:
    return parsedate_to_datetime(date)


PROCESSORS = {"date": date_processor}
