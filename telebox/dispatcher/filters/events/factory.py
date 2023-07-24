from abc import ABC, abstractmethod


class AbstractEventFilterFactory(ABC):

    @abstractmethod
    def get(self, *args, **kwargs):
        pass
