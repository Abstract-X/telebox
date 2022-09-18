from abc import ABC, abstractmethod


class AbstractErrorFilter(ABC):

    @abstractmethod
    def check_error(self, error, event) -> bool:
        pass
