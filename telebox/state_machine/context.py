from typing import Optional, TypeVar, Generic

from telebox.deps import DepsBase


DT = TypeVar("DT", bound=DepsBase)


class StateContext(Generic[DT]):
    __slots__ = ("deps", "chat_id", "user_id", "data")

    def __init__(
        self,
        deps: DT,
        chat_id: int,
        user_id: Optional[int] = None,
        data: Optional[dict] = None
    ):
        self.deps: DT = deps
        self.chat_id: int = chat_id
        self.user_id: Optional[int] = user_id
        self.data: dict = data if data is not None else {}
