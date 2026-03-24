from typing import Optional

from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.drafts.storage import AbstractDraftStorage
from telebox.dispatcher.context import EventContext
from telebox.dispatcher.middleware import Middleware
from telebox.dispatcher.drafts.lazy_draft import LazyDraft


EVENT_TYPES = {
    EventType.MESSAGE,
    EventType.MEDIA_GROUP,
    EventType.CALLBACK_QUERY
}


class DraftMiddleware(Middleware):
    def __init__(self, storage: AbstractDraftStorage) -> None:
        self._storage = storage

    def on_start(self, ctx) -> dict:
        ctx: EventContext

        if (ctx.event_type not in EVENT_TYPES) or (ctx.chat_id is None):
            return {}

        draft = LazyDraft(storage=self._storage, chat_id=ctx.chat_id, user_id=ctx.user_id)
        ctx.draft = draft

        return {
            "draft": draft
        }

    def on_finish(self, ctx, data: dict) -> None:
        ctx: EventContext

        draft: Optional[LazyDraft] = data.get("draft")

        if draft is None:
            return

        if draft.is_changed:
            self._storage.save(
                data=draft.get_data(),
                chat_id=ctx.chat_id,
                user_id=ctx.user_id
            )
