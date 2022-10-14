from typing import Optional


class StateMagazine:

    def __init__(self, states: list[str]):
        if not states:
            raise ValueError("State magazine can't be empty!")

        self._states = states[:]

    def __iter__(self):
        return iter(self._states)

    def __repr__(self):
        return f"{type(self).__name__}({self._states!r})"

    @property
    def current_state(self) -> str:
        return self._states[-1]

    @property
    def previous_state(self) -> Optional[str]:
        try:
            return self._states[-2]
        except IndexError:
            return None

    def set_state(self, state: str) -> None:
        try:
            index = self._states.index(state)
        except ValueError:
            self._states.append(state)
        else:
            del self._states[index + 1:]
