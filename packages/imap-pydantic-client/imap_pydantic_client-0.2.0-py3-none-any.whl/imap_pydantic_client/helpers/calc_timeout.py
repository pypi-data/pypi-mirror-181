from datetime import datetime, timedelta


def calc_timeout(timeout):
    """
    Calculate the time when a timeout should occur in seconds since epoch.

    :param timeout:(int or list): Either an integer representing the number of
    minutes to timeout in, or a list, formatted as [hour, minute] of
    the local time to timeout at.

    :return The timeout time in number of sections since epoch.
    """
    t = datetime.now()

    if type(timeout) is list:
        hr = (timeout[0] - t.hour) % 24
        mi = (timeout[1] - t.minute) % 60
        sec = 0 - t.second

        if (timeout[1] - t.minute) < 0:
            hr -= 1
            hr %= 24
    elif type(timeout) is int:
        hr = timeout // 60
        mi = timeout % 60
        sec = 0
    else:
        err = (
            "timeout must be either a list in the format [hours, minutes] "
            "or an integer representing minutes"
        )
        raise ValueError(err)

    t_delta = timedelta(seconds=sec, minutes=mi, hours=hr)
    return (t + t_delta).timestamp()
