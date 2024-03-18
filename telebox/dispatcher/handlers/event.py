from abc import ABC, abstractmethod
from typing import Optional

from telebox.dispatcher.types.aborting import Aborting


class AbstractEventHandler(ABC):

    @abstractmethod
    def process_event(self, event) -> Optional[Aborting]:
        pass
