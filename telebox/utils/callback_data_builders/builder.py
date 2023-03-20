from abc import ABC, abstractmethod


class AbstractCallbackDataBuilder(ABC):

    @abstractmethod
    def get_string(self, key, value=None) -> str:
        pass

    @abstractmethod
    def get_data(self, string: str):
        pass

    def get_key(self, string: str):
        key, _ = self.get_data(string)

        return key

    def get_value(self, string: str):
        _, value = self.get_data(string)

        return value
