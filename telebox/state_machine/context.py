from typing import Optional, TypeVar, Generic

from telebox import Bot
from telebox.deps import DepsBase


DT = TypeVar("DT", bound=DepsBase)


class StateContext(Generic[DT]):
    __slots__ = ("deps", "state", "next_state", "chat_id", "user_id", "data", "bot")

    def __init__(
        self,
        deps: DT,
        state: str,
        next_state: str,
        chat_id: int,
        *,
        user_id: Optional[int] = None,
        data: Optional[dict] = None,
        bot: Optional[Bot] = None
    ):
        self.deps: DT = deps
        self.state: str = state
        self.next_state: str = next_state
        self.chat_id: int = chat_id
        self.user_id: Optional[int] = user_id
        self.data: dict = data if data is not None else {}
        self.bot: Optional[Bot] = bot
