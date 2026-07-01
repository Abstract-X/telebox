from typing import Union

from telebox.bot.bot import Bot
from telebox.bot.types import CallbackQuery
from telebox.bot.types.link_preview_options import LinkPreviewOptions
from telebox.bot.types.reply_parameters import ReplyParameters
from telebox.bot.types.reply_keyboard_markup import ReplyKeyboardMarkup
from telebox.bot.types.reply_keyboard_remove import ReplyKeyboardRemove
from telebox.bot.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.bot.types.message import Message
from telebox.bot.types.message_entity import MessageEntity
from telebox.bot.types.input_media import InputMedia
from telebox.bot.types.input_media_photo import InputMediaPhoto
from telebox.bot.types.input_media_video import InputMediaVideo
from telebox.bot.types.input_media_animation import InputMediaAnimation
from telebox.bot.types.input_media_audio import InputMediaAudio
from telebox.bot.types.input_media_document import InputMediaDocument
from telebox.ui.reply.menu import ReplyMenu
from telebox.ui.inline.menu import InlineMenu
from telebox.ui.inline.keyboard import InlineKeyboard
from telebox.context_values import FromContext, FROM_CONTEXT, OPTIONAL_FROM_CONTEXT, event_context
from telebox.unset import Unset, UNSET


class UI:
    def __init__(self, bot: Bot):
        self.bot = bot

    def send_reply_menu(
        self,
        menu: ReplyMenu,
        *,
        chat_id: Union[int, str, FromContext] = FROM_CONTEXT,
        business_connection_id: Union[str, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        message_thread_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        direct_messages_topic_id: Union[int, None, Unset] = UNSET,
        link_preview_options: Union[LinkPreviewOptions, None, Unset] = UNSET,
        disable_notification: Union[bool, None, Unset] = UNSET,
        protect_content: Union[bool, None, Unset] = UNSET,
        message_effect_id: Union[str, None, Unset] = UNSET,
        reply_parameters: Union[ReplyParameters, None, Unset] = UNSET,
        request_timeout: Union[float, int, None, Unset] = UNSET
    ) -> Message:
        return self._send_menu(
            text=menu.text,
            reply_markup=menu.keyboard.get_markup(),
            chat_id=chat_id,
            parse_mode=menu.parse_mode,
            entities=menu.entities,
            media=menu.media,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            request_timeout=request_timeout
        )

    def remove_reply_keyboard(
        self,
        text: str,
        selective: Union[bool, None, Unset] = UNSET,
        *,
        chat_id: Union[int, str, FromContext] = FROM_CONTEXT,
        business_connection_id: Union[str, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        message_thread_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        direct_messages_topic_id: Union[int, None, Unset] = UNSET,
        parse_mode: Union[str, None, Unset] = UNSET,
        entities: Union[list[MessageEntity], None, Unset] = UNSET,
        link_preview_options: Union[LinkPreviewOptions, None, Unset] = UNSET,
        disable_notification: Union[bool, None, Unset] = UNSET,
        protect_content: Union[bool, None, Unset] = UNSET,
        message_effect_id: Union[str, None, Unset] = UNSET,
        reply_parameters: Union[ReplyParameters, None, Unset] = UNSET,
        request_timeout: Union[float, int, None, Unset] = UNSET
    ) -> Message:
        return self.bot.send_message(
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
            reply_markup=ReplyKeyboardRemove(
                remove_keyboard=True,
                selective=selective
            ),
            request_timeout=request_timeout
        )

    def send_inline_menu(
        self,
        menu: InlineMenu,
        *,
        chat_id: Union[int, str, FromContext] = FROM_CONTEXT,
        business_connection_id: Union[str, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        message_thread_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        direct_messages_topic_id: Union[int, None, Unset] = UNSET,
        link_preview_options: Union[LinkPreviewOptions, None, Unset] = UNSET,
        disable_notification: Union[bool, None, Unset] = UNSET,
        protect_content: Union[bool, None, Unset] = UNSET,
        message_effect_id: Union[str, None, Unset] = UNSET,
        reply_parameters: Union[ReplyParameters, None, Unset] = UNSET,
        request_timeout: Union[float, int, None, Unset] = UNSET
    ) -> Message:
        return self._send_menu(
            text=menu.text,
            reply_markup=menu.keyboard.get_markup(),
            chat_id=chat_id,
            parse_mode=menu.parse_mode,
            entities=menu.entities,
            media=menu.media,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            request_timeout=request_timeout
        )

    def edit_inline_menu(
        self,
        menu: InlineMenu,
        *,
        chat_id: Union[int, str, FromContext] = FROM_CONTEXT,
        message_id: Union[int, FromContext, None] = FROM_CONTEXT,
        business_connection_id: Union[str, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        link_preview_options: Union[LinkPreviewOptions, None, Unset] = UNSET,
        request_timeout: Union[float, int, None, Unset] = UNSET
    ) -> Message:
        if menu.media:
            data = self.bot.converter.get_data(menu.media)
            data["caption"] = menu.text
            data["parse_mode"] = menu.parse_mode
            data["caption_entities"] = menu.entities
            media = self.bot.converter.get_object(
                data=data,
                class_=type(menu.media)
            )

            return self.bot.edit_message_media(
                media=media,
                business_connection_id=business_connection_id,
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=menu.keyboard.get_markup(),
                request_timeout=request_timeout
            )

        return self.bot.edit_message_text(
            text=menu.text,
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            parse_mode=menu.parse_mode,
            entities=menu.entities,
            link_preview_options=link_preview_options,
            reply_markup=menu.keyboard.get_markup(),
            request_timeout=request_timeout
        )

    def edit_inline_keyboard(
        self,
        keyboard: InlineKeyboard,
        *,
        chat_id: Union[int, str, FromContext] = FROM_CONTEXT,
        message_id: Union[int, FromContext, None] = FROM_CONTEXT,
        business_connection_id: Union[str, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        request_timeout: Union[float, int, None, Unset] = UNSET
    ) -> Message:
        return self.bot.edit_message_reply_markup(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=keyboard.get_markup(),
            request_timeout=request_timeout
        )

    def remove_inline_keyboard(
        self,
        *,
        chat_id: Union[int, str, FromContext, None] = FROM_CONTEXT,
        message_id: Union[int, FromContext, None] = FROM_CONTEXT,
        business_connection_id: Union[str, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        request_timeout: Union[float, int, None, Unset] = UNSET
    ) -> None:
        self.bot.edit_message_reply_markup(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            request_timeout=request_timeout
        )

    def show_inline_menu(
        self,
        menu: InlineMenu,
        *,
        chat_id: Union[int, str, FromContext] = FROM_CONTEXT,
        message_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        business_connection_id: Union[str, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        message_thread_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        direct_messages_topic_id: Union[int, None, Unset] = UNSET,
        link_preview_options: Union[LinkPreviewOptions, None, Unset] = UNSET,
        disable_notification: Union[bool, None, Unset] = UNSET,
        protect_content: Union[bool, None, Unset] = UNSET,
        message_effect_id: Union[str, None, Unset] = UNSET,
        reply_parameters: Union[ReplyParameters, None, Unset] = UNSET,
        request_timeout: Union[float, int, None, Unset] = UNSET
    ) -> Message:
        if isinstance(message_id, FromContext):
            event = event_context.get(None)

            if isinstance(event, CallbackQuery) and (event.message_id is not None):
                message_id = event.message_id
            else:
                message_id = None

        if message_id is not None:
            return self.edit_inline_menu(
                menu=menu,
                chat_id=chat_id,
                message_id=message_id,
                business_connection_id=business_connection_id,
                link_preview_options=link_preview_options,
                request_timeout=request_timeout
            )

        return self.send_inline_menu(
            menu=menu,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            request_timeout=request_timeout
        )

    def _send_menu(
        self,
        text: str,
        reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup],
        *,
        chat_id: Union[int, str, FromContext] = FROM_CONTEXT,
        parse_mode: Union[str, None, Unset] = UNSET,
        entities: Union[list[MessageEntity], None, Unset] = UNSET,
        media: Union[InputMedia, None, Unset] = UNSET,
        business_connection_id: Union[str, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        message_thread_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        direct_messages_topic_id: Union[int, None, Unset] = UNSET,
        link_preview_options: Union[LinkPreviewOptions, None, Unset] = UNSET,
        disable_notification: Union[bool, None, Unset] = UNSET,
        protect_content: Union[bool, None, Unset] = UNSET,
        message_effect_id: Union[str, None, Unset] = UNSET,
        reply_parameters: Union[ReplyParameters, None, Unset] = UNSET,
        request_timeout: Union[float, int, None, Unset] = UNSET
    ) -> Message:
        if media:
            if isinstance(media, InputMediaPhoto):
                return self.bot.send_photo(
                    photo=media.media,
                    chat_id=chat_id,
                    business_connection_id=business_connection_id,
                    message_thread_id=message_thread_id,
                    direct_messages_topic_id=direct_messages_topic_id,
                    disable_notification=disable_notification,
                    protect_content=protect_content,
                    message_effect_id=message_effect_id,
                    reply_parameters=reply_parameters,
                    caption=text,
                    parse_mode=parse_mode,
                    caption_entities=entities,
                    show_caption_above_media=media.show_caption_above_media,
                    has_spoiler=media.has_spoiler,
                    reply_markup=reply_markup,
                    request_timeout=request_timeout
                )
            elif isinstance(media, InputMediaVideo):
                return self.bot.send_video(
                    video=media.media,
                    chat_id=chat_id,
                    business_connection_id=business_connection_id,
                    message_thread_id=message_thread_id,
                    direct_messages_topic_id=direct_messages_topic_id,
                    disable_notification=disable_notification,
                    protect_content=protect_content,
                    message_effect_id=message_effect_id,
                    reply_parameters=reply_parameters,
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
                    reply_markup=reply_markup,
                    request_timeout=request_timeout
                )
            elif isinstance(media, InputMediaAnimation):
                return self.bot.send_animation(
                    animation=media.media,
                    chat_id=chat_id,
                    business_connection_id=business_connection_id,
                    message_thread_id=message_thread_id,
                    direct_messages_topic_id=direct_messages_topic_id,
                    disable_notification=disable_notification,
                    protect_content=protect_content,
                    message_effect_id=message_effect_id,
                    reply_parameters=reply_parameters,
                    duration=media.duration,
                    width=media.width,
                    height=media.height,
                    thumbnail=media.thumbnail,
                    caption=text,
                    parse_mode=parse_mode,
                    caption_entities=entities,
                    show_caption_above_media=media.show_caption_above_media,
                    has_spoiler=media.has_spoiler,
                    reply_markup=reply_markup,
                    request_timeout=request_timeout
                )
            elif isinstance(media, InputMediaDocument):
                return self.bot.send_document(
                    document=media.media,
                    chat_id=chat_id,
                    business_connection_id=business_connection_id,
                    message_thread_id=message_thread_id,
                    direct_messages_topic_id=direct_messages_topic_id,
                    disable_notification=disable_notification,
                    protect_content=protect_content,
                    message_effect_id=message_effect_id,
                    reply_parameters=reply_parameters,
                    thumbnail=media.thumbnail,
                    caption=text,
                    parse_mode=parse_mode,
                    caption_entities=entities,
                    disable_content_type_detection=media.disable_content_type_detection,
                    reply_markup=reply_markup,
                    request_timeout=request_timeout
                )
            elif isinstance(media, InputMediaAudio):
                return self.bot.send_audio(
                    audio=media.media,
                    chat_id=chat_id,
                    business_connection_id=business_connection_id,
                    message_thread_id=message_thread_id,
                    direct_messages_topic_id=direct_messages_topic_id,
                    disable_notification=disable_notification,
                    protect_content=protect_content,
                    message_effect_id=message_effect_id,
                    reply_parameters=reply_parameters,
                    caption=text,
                    parse_mode=text,
                    caption_entities=entities,
                    duration=media.duration,
                    performer=media.performer,
                    title=media.title,
                    thumbnail=media.thumbnail,
                    reply_markup=reply_markup,
                    request_timeout=request_timeout
                )
            else:
                raise ValueError(f"Unknown media type {media.type!r}!")

        return self.bot.send_message(
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
            request_timeout=request_timeout
        )
