from typing import Union

from telebox.bot.bot import Bot
from telebox.bot.types.message import Message
from telebox.bot.types.callback_query import CallbackQuery
from telebox.dialog_manager.reply.menu import AbstractReplyMenu
from telebox.dialog_manager.inline.menu import AbstractInlineMenu
from telebox.dispatcher.context import Context, CONTEXT, event_context
from telebox.utils.deps import Deps


class DialogManager:
    def __init__(self, bot: Bot, deps: Deps):
        self._bot = bot
        self._deps = deps

    def send_reply_menu(
        self,
        menu: AbstractReplyMenu,
        chat_id: Union[int, str, Context] = CONTEXT
    ) -> Message:
        text = menu.get_text(deps=self._deps)
        parse_mode = menu.get_parse_mode()
        markup = menu.get_markup(deps=self._deps)

        return self._bot.send_message(
            text=text,
            chat_id=chat_id,
            parse_mode=parse_mode,
            reply_markup=markup
        )

    def send_inline_menu(
        self,
        menu: AbstractInlineMenu,
        chat_id: Union[int, str, Context] = CONTEXT,
        edit: bool = True
    ) -> Message:
        text = menu.get_text(deps=self._deps)
        parse_mode = menu.get_parse_mode()
        markup = menu.get_markup(deps=self._deps)
        event = event_context.get(None)

        if event is not None and isinstance(event, CallbackQuery) and edit:
            return self._bot.edit_message_text(
                text=text,
                parse_mode=parse_mode,
                reply_markup=markup
            )
        else:
            return self._bot.send_message(
                text=text,
                chat_id=chat_id,
                parse_mode=parse_mode,
                reply_markup=markup
            )
