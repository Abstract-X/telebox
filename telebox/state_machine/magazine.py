from typing import Optional


class StateMagazine:
    def __init__(self, states: list[str]):
        if not states:
            raise ValueError("State magazine cannot be empty!")

        self.states = states

    def __iter__(self):
        return iter(self.states)

    def __repr__(self):
        return f"{type(self).__name__}({self.states!r})"

    @property
    def state(self) -> str:
        return self.states[-1]

    @property
    def previous_state(self) -> Optional[str]:
        try:
            return self.states[-2]
        except IndexError:
            return None

    def set_state(self, state: str) -> None:
        try:
            index = self.states.index(state)
        except ValueError:
            self.states.append(state)
        else:
            del self.states[index + 1:]
