from abc import ABC, abstractmethod


class AbstractEventFilterFactory(ABC):

    @abstractmethod
    def get_filter(self, *args, **kwargs):
        pass
