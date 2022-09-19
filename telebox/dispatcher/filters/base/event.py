from abc import ABC, abstractmethod


class AbstractEventFilter(ABC):

    @abstractmethod
    def check_event(self, event) -> bool:
        pass
