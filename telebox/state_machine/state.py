from typing import Optional


class State:

    def __init__(self, name: Optional[str] = None):
        self._name = name or type(self).__name__

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name!r})"

    def __str__(self):
        return self.name

    @property
    def name(self) -> str:
        return self._name

    def process_enter(self, chat_id, user_id, event, data) -> None:
        pass

    def process_exit(self, chat_id, user_id, event, data) -> None:
        pass
