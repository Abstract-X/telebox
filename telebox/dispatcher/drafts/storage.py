from abc import ABC, abstractmethod
from typing import Optional, Union

from telebox.serialization import get_serialized_data, get_deserialized_data


Value = Union[str, int, float, bool, list["Value"], dict[str, "Value"], None]


class AbstractDraftStorage(ABC):
    @abstractmethod
    def _save(
        self,
        data: bytes,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        pass

    @abstractmethod
    def _load(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[bytes]:
        pass

    @abstractmethod
    def delete(self, *, chat_id: int, user_id: Optional[int] = None) -> None:
        pass

    def save(
        self,
        data: dict[str, Value],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        if data:
            self._save(
                data=get_serialized_data(data),
                chat_id=chat_id,
                user_id=user_id
            )
        else:
            self.delete(chat_id=chat_id, user_id=user_id)

    def load(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> dict[str, Value]:
        data = self._load(chat_id=chat_id, user_id=user_id)

        if not data:
            return {}

        return get_deserialized_data(data)
