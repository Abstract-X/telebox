from abc import ABC, abstractmethod


class AbstractErrorFilterFactory(ABC):

    @abstractmethod
    def get_filter(self, *args, **kwargs):
        pass
