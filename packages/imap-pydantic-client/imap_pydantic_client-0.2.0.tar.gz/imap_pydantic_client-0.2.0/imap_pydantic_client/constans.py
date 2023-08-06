from enum import Enum

EXCLUDED_FLAGS_FOLDERS = [
    b"\\HasNoChildren",
    b"\\HasChildren",
    b"\\HasChildren",
]
BATCH_SIZE_IDS_EMAIL = 100


class EmailListenerStatus(Enum):
    NOT_READY = "Not ready"
    OK = "Ok"
    ERROR = "Error"
    READY = "Ready"
