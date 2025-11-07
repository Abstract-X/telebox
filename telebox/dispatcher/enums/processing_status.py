from enum import IntEnum


class ProcessingStatus(IntEnum):
    PROCESSING = 1
    ABORTED = 2
    HANDLER_NOT_FOUND = 3
    ERROR_OCCURRED = 4
    ADDED_TO_CHAT_QUEUE = 5
