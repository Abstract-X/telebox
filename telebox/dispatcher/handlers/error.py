from abc import ABC, abstractmethod


class AbstractErrorHandler(ABC):

    @abstractmethod
    def process_error(self, deps, error, event):
        pass
