from enum import IntEnum


class ProcessingStatus(IntEnum):
    PROCESSING = 1
    ABORTED = 2
    HANDLER_NOT_FOUND = 3
    RATE_LIMIT_EXCEEDED = 4
    ERROR_OCCURRED = 5
    ADDED_TO_CHAT_QUEUE = 6
