from abc import ABC, abstractmethod


class AbstractCallbackDataBuilder(ABC):

    @abstractmethod
    def build(self, filter_key, value=None) -> str:
        pass

    @abstractmethod
    def parse(self, data: str):
        pass
