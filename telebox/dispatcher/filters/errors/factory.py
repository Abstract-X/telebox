from abc import ABC, abstractmethod


class AbstractErrorFilterFactory(ABC):

    @abstractmethod
    def get(self, *args, **kwargs):
        pass
