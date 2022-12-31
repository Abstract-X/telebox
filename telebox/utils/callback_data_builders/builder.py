from abc import ABC, abstractmethod


class AbstractCallbackDataBuilder(ABC):

    @abstractmethod
    def get_builded_data(self, key, value=None) -> str:
        pass

    @abstractmethod
    def get_parsed_data(self, data: str):
        pass

    def get_key(self, data: str):
        key, _ = self.get_parsed_data(data)

        return key

    def get_value(self, data: str):
        _, value = self.get_parsed_data(data)

        return value
