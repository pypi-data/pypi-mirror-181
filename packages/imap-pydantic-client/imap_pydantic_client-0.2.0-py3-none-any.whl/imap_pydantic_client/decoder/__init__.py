__all__ = ["Headers", "Decoder"]

import email
import logging
from email import message, policy
from email import utils
from email.generator import BytesGenerator
from email.parser import HeaderParser
from io import BytesIO
from mailbox import MMDFMessage, mboxMessage
from typing import Optional, Any, Type

from pydantic import BaseModel

from .structs import Headers

logger = logging.getLogger(__name__)


class Decoder:
    __data: dict
    __message: message.Message
    __email_message: Optional[message.EmailMessage]
    __header_model: Type[Headers]
    __codec: bytes

    def __new__(cls, message_data, *, header_model=Headers):
        cls.__data = message_data
        cls.__header_model = header_model
        cls.__codec = list(cls.__data.keys())[-1]
        cls.__message = email.message_from_bytes(
            cls.__data[cls.__codec],
            policy=policy.default,
        )
        cls.__email_message = cls.__message2email(cls.__message)
        return cls

    @classmethod
    def parse(cls):
        """
        Parse the email message
        :return:
        """
        return {
            "subject": cls.get_subject(),
            "headers": cls.get_headers(),
            "from_email": cls.get_from(),
            "date": cls.get_date(),
            "content": cls.get_content(),
        }

    @classmethod
    def get_headers(cls) -> BaseModel:
        """
        Returns the headers of the message
        :return: BaseModel like object
        """
        codec = list(cls.__data.keys())[-1]
        data = dict(HeaderParser().parsestr(cls.__data[codec].decode("utf-8")).items())

        return cls.__header_model.parse_obj(data)

    @classmethod
    def get_from(cls):
        """
        Helper function for getting who an email message is from.

        :return: string containing from email address.
        """

        from_raw = cls.__message.get_all("From", [])
        from_list = utils.getaddresses(from_raw)
        if len(from_list[0]) == 1:
            return from_list[0][0]
        elif len(from_list[0]) == 2:
            return from_list[0][1]
        else:
            return "UnknownEmail"

    @classmethod
    def get_subject(cls):
        """
        Helper function for getting the subject of the message.

        :return: string containing the subject.
        """
        subject = cls.__message.get("Subject")
        return "No Subject" if subject is None else subject.strip()

    @classmethod
    def get_content(cls):
        """
        Helper function for getting the content of the message.

        :return: string containing the content.
        """
        if cls.__message.is_multipart():
            return cls.__parse_multi_part_message()
        else:
            return cls.__parse_single_part_message()

    @classmethod
    def get_date(cls):
        """
        Helper function for getting the date of the message.

        :return: string containing the date.
        """
        return cls.get_headers().date

    @classmethod
    def __parse_multi_part_message(cls) -> list[dict[str, dict[str, str | Any] | Any]]:
        """
        Helper function for parsing multipart email messages.

        :param email_message (email.message): The email message to parse.
            val_dict (dict): A dictionary containing the message data from each
                part of the message. Will be returned after it is updated.

        :return: The dictionary containing the message data for each part of the message.

        """
        answer = []
        for part in cls.__message.walk():
            part_dict = {}
            file_name = part.get_filename()
            if bool(file_name):
                part_dict["attachment"] = {
                    "file_name": file_name,
                    "content": part.get_payload(decode=True),
                }
            elif part.get_content_type() == "text/html":
                part_dict["html"] = part.get_payload()
            elif part.get_content_type() == "text/plain":
                part_dict["plain_text"] = part.get_payload()
            if part_dict:
                answer.append(part_dict)
        return answer

    @classmethod
    def __parse_single_part_message(cls):
        """
        Helper function for parsing single part email messages.

        :param email_message: (email.message) The email message to parse.
        :return: The dictionary containing the message data for each part of the message.
        """

        return [{"plain_text": cls.__message.get_payload()}]

    @staticmethod
    def __message2email(msg: message.Message) -> message.EmailMessage:
        """
        Helper function for converting a message to an email message.

        :param msg: (email.message): The email message to convert.
        :return: (email.message): The email message.
        """
        fp = BytesIO()
        g = BytesGenerator(fp, mangle_from_=False, maxheaderlen=0)
        g.flatten(msg, unixfrom=msg.get_unixfrom() is not None)
        fp.seek(0)
        emsg = email.message_from_binary_file(fp, policy=policy.default)
        assert isinstance(emsg, message.EmailMessage)
        if isinstance(msg, (MMDFMessage, mboxMessage)):
            emsg.set_unixfrom(f"From {msg.get_from()}")
        return emsg
