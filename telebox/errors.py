from dataclasses import dataclass

from xcept import Exception_


@dataclass
class TeleboxError(Exception_):
    pass
