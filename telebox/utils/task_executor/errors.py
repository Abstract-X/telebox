from dataclasses import dataclass

from telebox.errors import TeleboxError


@dataclass
class TaskExecutorError(TeleboxError):
    """Class for task executor errors."""


@dataclass
class TaskNotFoundError(TaskExecutorError):
    id: str
