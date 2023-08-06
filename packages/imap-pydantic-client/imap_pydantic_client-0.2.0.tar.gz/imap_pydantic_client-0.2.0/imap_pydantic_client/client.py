import logging
from typing import Callable, List, Optional, Union

from imapclient import SEEN, IMAPClient
from imapclient.response_types import SearchIds

from .constans import BATCH_SIZE_IDS_EMAIL, EXCLUDED_FLAGS_FOLDERS, EmailListenerStatus
from .decoder import Decoder
from .helpers import calc_timeout, get_time
from .structs import EmailListenerSettings, EmailMessage

logger = logging.getLogger(__name__)


class EmailListener:
    folders: List = []
    status: EmailListenerStatus = EmailListenerStatus.NOT_READY
    __batch_size_ids_email: int = BATCH_SIZE_IDS_EMAIL
    __server: Optional[IMAPClient] = None
    __settings: EmailListenerSettings = None
    __func_is_double: Optional[Callable[[dict], bool]] = None

    def __init__(self, settings: EmailListenerSettings):
        self.__settings = settings
        if self.__settings.auto_login:
            self.__login()
            self.__prepare_mail_box_folder()
            self.status = EmailListenerStatus.READY

    def scrape(
        self,
        folder: str = "inbox",
        move=None,
        unread=False,
        delete=False,
    ) -> List[EmailMessage]:
        """
        Scrape unread emails from the current folder.
        A list of the file paths to each scraped email.
        :param folder:
        :param move:
        :param unread:
        :param delete:
        """
        self.__select_folder(folder, readonly=False)
        messages = self.__server.search("UNSEEN")
        return self.__processing(ids=messages, move=move, unread=unread, delete=delete)

    def get_all_msq(
        self,
        folder: str = "Inbox",
        move=None,
        unread=False,
        delete=False,
        func_check: Callable[[dict], bool] = None,
    ):
        logger.info("Getting all messages")
        self.__func_is_double = func_check
        self.__select_folder(folder, readonly=False)
        messages = self.__server.search()
        return self.__processing(ids=messages, move=move, unread=unread, delete=delete)

    def listen(
        self,
        timeout: Union[int, List[int]],
        process_func: Callable,
        **kwargs,
    ) -> None:
        """
        Listen in an email folder for incoming emails, and process them.

        :param timeout: (int or list): Either an integer representing the number of minutes to timeout in, or a list,
        formatted as [hour, minute] of the local time to timeout at.
        :param process_func: (function): A function called to further process the emails. The function must take only
        the list of file paths returned by the scrape function as an argument. Defaults to the example function
        write_txt_file in the email_processing module.
        :param kwargs: (dict): Additional arguments for processing the email.
        Optional arguments include:
            move (str): The folder to move emails to. If not set, the
                emails will not be moved.
            unread (bool): Whether the emails should be marked as unread.
                If not set, emails are kept as read.
            delete (bool): Whether the emails should be deleted. If not
                set, emails are not deleted.

        :return: None
        """
        outer_timeout = calc_timeout(timeout)
        while get_time() < outer_timeout:
            self.__idle(process_func=process_func, **kwargs)
        return

    def __processing(
        self,
        ids: SearchIds,
        *,
        move=None,
        unread=False,
        delete=False,
    ) -> List[EmailMessage]:
        answer: List[EmailMessage] = []
        for i in range(0, len(ids), self.__batch_size_ids_email):
            emails = self.__fetch(ids[i : i + self.__batch_size_ids_email])
            for uid, message_data in emails.items():
                data = self.__decode_email_message(message_data)
                answer.append(EmailMessage.parse_obj(data))
                self.__execute_options(uid, move=move, unread=unread, delete=delete)
        return answer

    def __fetch(self, ids: SearchIds, codec: str = "RFC822", modifiers=None):
        """
        Fetch emails from the server.

        :param ids: Ids mail to fetch
        :param codec: codec string
        :param modifiers:
        :return:
        """
        logger.info("Fetching emails from server")
        return self.__server.fetch(ids, codec, modifiers)

    @staticmethod
    def __decode_email_message(message_data: dict) -> dict:
        """
        Decode the email message data.

        :param message_data: Dict message_data
        :return:
        """
        return Decoder(message_data).parse()

    @staticmethod
    def __extract_label_folder(item) -> tuple:
        """
        Extract the label folder from a mailbox.
        :param item:
        :return:
        """
        populate_name = item[-1]
        parent_name = item[1].decode()
        label = next(
            (ell.decode() for ell in item[0] if ell not in EXCLUDED_FLAGS_FOLDERS),
            populate_name,
        )
        return label, populate_name, parent_name

    def __execute_options(self, uid: int, move: bool, unread: bool, delete: bool):
        """
        Loop through optional arguments and execute any required processing.

        :param uid: (int): The email ID to process.
        :param move: (str): The folder to move the emails to. If None, the emails are not moved. Defaults to None.
        :param unread: (bool): Whether the emails should be marked as unread. Defaults to False.
        :param delete: (bool): Whether the emails should be deleted. Defaults to False.
        :return: None
        """

        if unread:
            self.__server.remove_flags(uid, [SEEN])

        if move is not None:
            try:
                self.__server.move(uid, move)
            except Exception:  # noqa
                self.__server.create_folder(move)
                self.__server.move(uid, move)
        elif delete:
            self.__server.set_gmail_labels(uid, "\\Trash")
        return

    def __idle(self, process_func, **kwargs):
        """
        Helper function, idles in an email folder processing incoming emails.

        :param process_func: (function): A function called to further process the
                emails. The function must take only the list of file paths
                returned by the scrape function as an argument. Defaults to the
                example function write_txt_file in the email_processing module.

        :param kwargs: (dict): Additional arguments for processing the email.

        Optional arguments include:

            move (str): The folder to move emails to. If not set, the emails will not be moved.

            unread (bool): Whether the emails should be marked as unread. If not set, emails are kept as read.

            delete (bool): Whether the emails should be deleted. If not set, emails are not deleted.

        :return: None
        """

        move = kwargs.get("move")
        unread = bool(kwargs.get("unread"))
        delete = bool(kwargs.get("delete"))

        self.__server.idle()
        logger.info("Connection is now in IDLE mode.")
        inner_timeout = get_time() + 60 * 5
        while get_time() < inner_timeout:
            responses = self.__server.idle_check(timeout=30)
            logger.info(f"Server sent: {responses or 'nothing'}")
            if responses:
                self.__server.idle_done()
                msgs = self.scrape(move=move, unread=unread, delete=delete)
                process_func(self, msgs)
                self.__server.idle()
        self.__server.idle_done()
        return

    def __check_folder_exists(self, folder) -> None:
        """
        Check if a folder exists.

        :param folder: (str): The folder to check.
        :return: (None): or raise exception
        """
        for el in map(lambda x: x["label"], self.folders):  # noqa
            if el.upper() == folder.upper():
                return
        raise ValueError(f"Invalid folder: {folder}")

    def __select_folder(self, folder: str, readonly: bool = False):
        """
        Select a folder.

        :param folder: (str): The folder to select.
        :param readonly: (bool): Whether the folder should be read only.
        :return: (None):
        """
        self.__check_folder_exists(folder)
        self.__server.select_folder(folder, readonly=readonly)

    def __prepare_mail_box_folder(self):
        """
        Prepare the mail box folder.

        :return: (None)
        """
        for el in self.__server.list_folders():
            self.folders.append(
                dict(
                    zip(
                        ["label", "populate_name", "parent_name"],
                        self.__extract_label_folder(el),
                    ),
                ),
            )

    def __login(self):
        """
        Login to mailbox.

        :return: (None)
        """
        self.__server = IMAPClient(
            host=self.__settings.smtp_server,
            port=self.__settings.smtp_server_port,
        )
        self.__server.login(self.__settings.email, self.__settings.password)

    def __logout(self):
        """
        Logout from mailbox.

        :return: (None)
        """
        self.__server.logout()
        self.__server = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit.

        :param exc_type: (type): The exception type.
        :param exc_val: (value): The exception value.
        :param exc_tb: (traceback): The exception traceback.
        """
        self.__logout()
