from datetime import datetime


def get_time():
    """
    Get the current time in seconds since epoch.
    :return: The current time in seconds since epoch.
    """
    return datetime.now().timestamp()
