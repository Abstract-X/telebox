from abc import ABC, abstractmethod


class AbstractEventHandler(ABC):

    @abstractmethod
    def process_event(self, event) -> None:
        pass
