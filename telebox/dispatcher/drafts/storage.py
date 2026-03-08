from abc import ABC, abstractmethod
from typing import Optional, Union

from telebox.context_values import (
    FromContext,
    FROM_CONTEXT,
    OPTIONAL_FROM_CONTEXT,
    get_chat_id_and_user_id
)
from telebox.dispatcher.drafts.draft import Draft, Value


class AbstractDraftStorage(ABC):
    @abstractmethod
    def _save_draft(
        self,
        draft: dict[str, Value],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        pass

    @abstractmethod
    def _load_draft(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[dict[str, Value]]:
        pass

    @abstractmethod
    def _clear_draft(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        pass

    def save_draft(
        self,
        draft: Draft,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT
    ):
        chat_id, user_id = get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        self._save_draft(
            draft=draft.get_data(),
            chat_id=chat_id,
            user_id=user_id
        )

    def load_draft(
        self,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT
    ) -> Draft:
        chat_id, user_id = get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        data = self._load_draft(chat_id=chat_id, user_id=user_id)

        return Draft(data)

    def clear_draft(
        self,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT
    ) -> None:
        chat_id, user_id = get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        self._clear_draft(chat_id=chat_id, user_id=user_id)

    def draft(
        self,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT
    ) -> "DraftContext":
        return DraftContext(
            storage=self,
            chat_id=chat_id,
            user_id=user_id
        )


class DraftContext:
    def __init__(
        self,
        storage: AbstractDraftStorage,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT
    ):
        self._storage = storage
        self._chat_id = chat_id
        self._user_id = user_id
        self._draft: Optional[Draft] = None

    def __enter__(self):
        self._draft = self._storage.load_draft(chat_id=self._chat_id, user_id=self._user_id)

        return self._draft

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._draft.is_changed:
            self._storage.save_draft(
                draft=self._draft,
                chat_id=self._chat_id,
                user_id=self._user_id
            )
