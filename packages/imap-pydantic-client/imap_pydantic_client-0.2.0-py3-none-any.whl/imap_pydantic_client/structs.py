import binascii
import json
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, root_validator

from .decoder import Headers


class Attachment(BaseModel):
    file_name: str
    content: bytes


class EmailMessageContent(BaseModel):
    plain_text: Optional[str]
    html: Optional[str]
    attachment: Optional[Attachment]


class EmailMessage(BaseModel):
    hash: str
    subject: str
    headers: Headers
    date: datetime
    from_email: str
    content: List[EmailMessageContent]

    @root_validator(pre=True)
    def validate_headers(cls, values: dict):  # noqa: pylint: disable=E0213
        values["hash"] = binascii.crc32(json.dumps(values).encode('utf8'))
        return values


class EmailListenerSettings(BaseModel):
    email: EmailStr
    password: str
    smtp_server: Optional[str]
    smtp_server_port: Optional[int]
    auto_login: bool = True
