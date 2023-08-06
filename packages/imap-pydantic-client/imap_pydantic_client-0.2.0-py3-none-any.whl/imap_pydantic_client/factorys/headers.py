from string import ascii_letters
from imap_pydantic_client.factorys.fakers import fake


def get_random_header_data(delivered_to: str = None, to: str = None, from_: str = None):
    return {
        "Delivered-To": delivered_to or fake.company_email(),
        "Return-Path": f"<{fake.sha1(raw_output=False)}@{fake.domain_name()}",
        "X-Gm-Message-State": fake.sha256(raw_output=False),
        "X-Google-Smtp-Source": fake.sha256(raw_output=False),
        "X-BeenThere": fake.company_email(),
        "MIME-Version": "1.0",
        "From": from_ or fake.email_set(),
        "Date": fake.past_datetime(tzinfo=fake.pytimezone()).strftime(
            "%a, %-d %b %Y %H:%M:%S %z",
        ),
        "Message-ID": f"<{fake.sha256(raw_output=False)}@{fake.domain_name()}>",
        "Subject": fake.bothify(
            text=f'[Test Subject]: {"?" * 80}',
            letters=ascii_letters,
        ),
        "To": to or fake.company_email(),
        "Cc": ", ".join([fake.email_set() for _ in range(3)]),
        "Content-Type": fake.content_type_popular(),
        "X-Original-Sender": fake.company_email(),
        "List-ID": fake.domain_name(levels=1),
        "X-Spam-Checked-In-Group": fake.company_email(),
        "X-Google-Group-Id": fake.bothify(text="############"),
        "Received": fake.bothify(text="############"),
    }
