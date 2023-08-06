import hashlib
import json
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Optional
import binascii

from pydantic import BaseModel, Field, root_validator, validator

from .constants import MAIN_HEADERS_LIST


class Headers(BaseModel):
    hash: str
    id: Optional[str] = Field(alias="Message-ID")
    date: datetime = Field(alias="Date")
    subject: Optional[str] = Field(alias="Subject")
    from_: str = Field(alias="From")
    to: str = Field(alias="To")
    delivered_to: str = Field(alias="Delivered-To")
    cc: Optional[str] = Field(alias="Cc")
    bcc: Optional[str] = Field(alias="Bcc")
    received: str = Field(alias="Received")
    other: dict

    @root_validator(pre=True)
    def validate_headers(cls, values: dict):  # noqa: pylint: disable=E0213
        list_key_for_erase = []
        other = {}
        for name in values:
            if name not in MAIN_HEADERS_LIST:
                other[name] = values.get(name)
                list_key_for_erase.append(name)
        for key in list_key_for_erase:
            del values[key]
        values["other"] = other
        values["hash"] = binascii.crc32(json.dumps(values).encode('utf8'))  # noqa
        return values

    @validator("date", pre=True)
    def convert_date(cls, value: str) -> datetime:  # noqa: pylint: disable=E0213
        return parsedate_to_datetime(value)
