from typing import Optional


class StateHistory:
    def __init__(self, state_ids: Optional[list[int]] = None):
        self.state_ids = state_ids or []

    @property
    def state_id(self) -> Optional[int]:
        return self.state_ids[-1] if self.state_ids else None

    @property
    def previous_state_id(self) -> Optional[int]:
        return self.state_ids[-2] if len(self.state_ids) > 1 else None

    def set_state_id(self, state_id: int) -> None:
        try:
            index = self.state_ids.index(state_id)
        except ValueError:
            self.state_ids.append(state_id)
        else:
            del self.state_ids[index + 1:]
