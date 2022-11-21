from abc import ABC, abstractmethod


class AbstractCallbackDataBuilder(ABC):

    @abstractmethod
    def get_builded_data(self, key, value=None) -> str:
        pass

    @abstractmethod
    def get_parsed_data(self, data: str):
        pass
