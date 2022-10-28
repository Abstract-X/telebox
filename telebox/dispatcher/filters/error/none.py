from telebox.dispatcher.filters.error_filter import AbstractErrorFilter
from telebox.dispatcher.dispatcher import Event


class ErrorNoneFilter(AbstractErrorFilter):

    def get_value(self, error: Exception, event: Event) -> bool:
        return True

    def check_value(self, value: bool) -> bool:
        return value
