from abc import ABC, abstractmethod


class AbstractEventHandler(ABC):

    @abstractmethod
    def process_event(self, event):
        pass

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__
