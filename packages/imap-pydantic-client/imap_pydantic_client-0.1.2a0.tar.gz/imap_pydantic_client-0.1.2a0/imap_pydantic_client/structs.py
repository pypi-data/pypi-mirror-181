from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from .decoder import Headers


class Attachment(BaseModel):
    file_name: str
    content: bytes


class EmailMessageContent(BaseModel):
    plain_text: Optional[str]
    html: Optional[str]
    attachment: Optional[Attachment]


class EmailMessage(BaseModel):
    subject: str
    headers: Headers
    date: datetime
    from_email: EmailStr
    content: List[EmailMessageContent]


class EmailListenerSettings(BaseModel):
    email: EmailStr
    password: str
    smtp_server: Optional[str]
    smtp_server_port: Optional[int]
    auto_login: bool = True
