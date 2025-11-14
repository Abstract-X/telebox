from typing import Union, Optional

from telebox.bot.bot import Bot
from telebox.bot.enums.message_type import MessageType
from telebox.bot.types.callback_query import CallbackQuery
from telebox.bot.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.bot.types.input_media import InputMedia
from telebox.bot.types.input_media_animation import InputMediaAnimation
from telebox.bot.types.input_media_audio import InputMediaAudio
from telebox.bot.types.input_media_document import InputMediaDocument
from telebox.bot.types.input_media_photo import InputMediaPhoto
from telebox.bot.types.input_media_video import InputMediaVideo
from telebox.bot.types.link_preview_options import LinkPreviewOptions
from telebox.bot.types.message import Message
from telebox.bot.types.message_entity import MessageEntity
from telebox.bot.types.reply_keyboard_markup import ReplyKeyboardMarkup
from telebox.bot.types.reply_parameters import ReplyParameters
from telebox.dialog_manager.inline.menu import AbstractInlineMenu
from telebox.dialog_manager.reply.menu import AbstractReplyMenu
from telebox.dispatcher.context import Context, CONTEXT, OPTIONAL_CONTEXT, event_context
from telebox.utils.deps import Deps
from telebox.utils.unset import Unset, UNSET


class DialogManager:
    def __init__(self, bot: Bot, deps: Deps):
        self._bot = bot
        self._deps = deps

    def send_reply_menu(
        self,
        menu: AbstractReplyMenu,
        chat_id: Union[int, str, Context] = CONTEXT,
        business_connection_id: Union[str, Context, None] = OPTIONAL_CONTEXT,
        message_thread_id: Union[int, Context, None] = OPTIONAL_CONTEXT,
        direct_messages_topic_id: Union[int, None, Unset] = UNSET,
        link_preview_options: Union[LinkPreviewOptions, None, Unset] = UNSET,
        disable_notification: Union[bool, None, Unset] = UNSET,
        protect_content: Union[bool, None, Unset] = UNSET,
        message_effect_id: Union[str, None, Unset] = UNSET,
        reply_parameters: Union[ReplyParameters, None, Unset] = UNSET,
        timeout_secs: Union[float, int, None, Unset] = UNSET
    ) -> Message:
        return self._send_menu(
            text=menu.get_text(deps=self._deps),
            reply_markup=menu.get_markup(deps=self._deps),
            chat_id=chat_id,
            parse_mode=menu.get_parse_mode(),
            entities=menu.get_entities(),
            media=menu.get_media(deps=self._deps),
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            timeout_secs=timeout_secs
        )

    def send_inline_menu(
        self,
        menu: AbstractInlineMenu,
        chat_id: Union[int, str, Context] = CONTEXT,
        edit: bool = True,
        message_id: Union[int, Context, None] = OPTIONAL_CONTEXT,
        business_connection_id: Union[str, Context, None] = OPTIONAL_CONTEXT,
        message_thread_id: Union[int, Context, None] = OPTIONAL_CONTEXT,
        direct_messages_topic_id: Union[int, None, Unset] = UNSET,
        link_preview_options: Union[LinkPreviewOptions, None, Unset] = UNSET,
        disable_notification: Union[bool, None, Unset] = UNSET,
        protect_content: Union[bool, None, Unset] = UNSET,
        message_effect_id: Union[str, None, Unset] = UNSET,
        reply_parameters: Union[ReplyParameters, None, Unset] = UNSET,
        timeout_secs: Union[float, int, None, Unset] = UNSET
    ) -> Message:
        text = menu.get_text(deps=self._deps)
        parse_mode = menu.get_parse_mode()
        entities = menu.get_entities()
        media = menu.get_media(deps=self._deps)
        markup = menu.get_markup(deps=self._deps)
        event = event_context.get(None)

        if (
            message_id
            or (
                (event is not None)
                and isinstance(event, CallbackQuery)
                and edit
            )
        ):
            if media:
                data = self._bot.converter.get_data(media)
                data["caption"] = text
                data["parse_mode"] = parse_mode
                data["caption_entities"] = entities
                media = self._bot.converter.get_object(
                    data=data,
                    class_=type(media)
                )

                return self._bot.edit_message_media(
                    media=media,
                    business_connection_id=business_connection_id,
                    chat_id=chat_id,
                    message_id=message_id,
                    reply_markup=markup,
                    timeout_secs=timeout_secs
                )

            return self._bot.edit_message_text(
                text=text,
                business_connection_id=business_connection_id,
                chat_id=chat_id,
                message_id=message_id,
                parse_mode=parse_mode,
                entities=entities,
                link_preview_options=link_preview_options,
                reply_markup=markup,
                timeout_secs=timeout_secs
            )

        return self._send_menu(
            text=text,
            reply_markup=markup,
            chat_id=chat_id,
            parse_mode=parse_mode,
            entities=entities,
            media=media,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            timeout_secs=timeout_secs
        )

    def _send_menu(
        self,
        text: str,
        reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup],
        chat_id: Union[int, str, Context] = CONTEXT,
        parse_mode: Union[str, None, Unset] = UNSET,
        entities: Union[list[MessageEntity], None, Unset] = UNSET,
        media: Optional[InputMedia] = None,
        business_connection_id: Union[str, Context, None] = OPTIONAL_CONTEXT,
        message_thread_id: Union[int, Context, None] = OPTIONAL_CONTEXT,
        direct_messages_topic_id: Union[int, None, Unset] = UNSET,
        link_preview_options: Union[LinkPreviewOptions, None, Unset] = UNSET,
        disable_notification: Union[bool, None, Unset] = UNSET,
        protect_content: Union[bool, None, Unset] = UNSET,
        message_effect_id: Union[str, None, Unset] = UNSET,
        reply_parameters: Union[ReplyParameters, None, Unset] = UNSET,
        timeout_secs: Union[float, int, None, Unset] = UNSET
    ) -> Message:
        if media:
            if isinstance(media, InputMediaPhoto):
                return self._bot.send_photo(
                    photo=media.media,
                    chat_id=chat_id,
                    caption=text,
                    parse_mode=parse_mode,
                    caption_entities=entities,
                    show_caption_above_media=media.show_caption_above_media,
                    has_spoiler=media.has_spoiler,
                    reply_markup=reply_markup
                )
            elif isinstance(media, InputMediaVideo):
                return self._bot.send_video(
                    video=media.media,
                    chat_id=chat_id,
                    duration=media.duration,
                    width=media.width,
                    height=media.height,
                    thumbnail=media.thumbnail,
                    cover=media.cover,
                    start_timestamp=media.start_timestamp,
                    caption=text,
                    parse_mode=parse_mode,
                    caption_entities=entities,
                    show_caption_above_media=media.show_caption_above_media,
                    has_spoiler=media.has_spoiler,
                    supports_streaming=media.supports_streaming,
                    reply_markup=reply_markup
                )
            elif isinstance(media, InputMediaAnimation):
                return self._bot.send_animation(
                    animation=media.media,
                    chat_id=chat_id,
                    duration=media.duration,
                    width=media.width,
                    height=media.height,
                    thumbnail=media.thumbnail,
                    caption=text,
                    parse_mode=parse_mode,
                    caption_entities=entities,
                    show_caption_above_media=media.show_caption_above_media,
                    has_spoiler=media.has_spoiler,
                    reply_markup=reply_markup
                )
            elif isinstance(media, InputMediaDocument):
                return self._bot.send_document(
                    document=media.media,
                    chat_id=chat_id,
                    thumbnail=media.thumbnail,
                    caption=text,
                    parse_mode=parse_mode,
                    caption_entities=entities,
                    disable_content_type_detection=media.disable_content_type_detection,
                    reply_markup=reply_markup
                )
            elif isinstance(media, InputMediaAudio):
                return self._bot.send_audio(
                    audio=media.media,
                    chat_id=chat_id,
                    caption=text,
                    parse_mode=text,
                    caption_entities=entities,
                    duration=media.duration,
                    performer=media.performer,
                    title=media.title,
                    thumbnail=media.thumbnail,
                    reply_markup=reply_markup
                )
            else:
                raise ValueError(f"Unknown media type {media.type!r}!")
            
        return self._bot.send_message(
            text=text,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
            timeout_secs=timeout_secs
        )
