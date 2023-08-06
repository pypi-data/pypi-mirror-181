import os

from .fakers import fake


def get_random_attachment(file_size_in_bytes: int = 10):
    return {"file_name": "test.txt", "content": os.urandom(file_size_in_bytes)}


def get_random_content_data(
    is_plain_text: bool = False,
    is_attachment: bool = False,
    is_html: bool = True,
):
    text = fake.paragraph(nb_sentences=5)
    return {
        "plain_text": text if is_plain_text else None,
        "html": f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Test email</title></head><body>'
        f"<div>{text}</div></body></html>"
        if is_html
        else None,
        "attachment": get_random_attachment() if is_attachment else None,
    }
