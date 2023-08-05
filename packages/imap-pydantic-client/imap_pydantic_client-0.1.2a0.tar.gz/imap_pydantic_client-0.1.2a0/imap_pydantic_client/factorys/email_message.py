from .content import get_random_content_data
from .fakers import fake
from .headers import get_random_header_data


def get_email_message_data(
    is_plain_text: bool = True,
    is_attachment: bool = True,
    is_html: bool = True,
    delivered_to: str = None,
    to: str = None,
    from_: str = None,
):
    return {
        "subject": "[TEST email]",
        "headers": get_random_header_data(delivered_to, to, from_),
        "date": fake.past_datetime(tzinfo=fake.pytimezone()),
        "from_email": from_ or fake.email_set(),
        "content": [
            get_random_content_data(is_plain_text, is_attachment, is_html)
            for _ in range(3)
        ],
    }
