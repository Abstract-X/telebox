from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.type_hints import Event


class EmptyFilter(AbstractFilter):
    def get_value(self, event: Event) -> bool:
        return True

    def check_value(self, value: bool) -> bool:
        return value
