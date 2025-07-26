from abc import ABC, abstractmethod


class AbstractFilterFactory(ABC):

    @abstractmethod
    def get(self, *args, **kwargs):
        pass
