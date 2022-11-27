from typing import Optional, Union, Literal
from datetime import datetime

from telebox.bot.bot import Bot
from telebox.bot.types.types.message import Message
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.bot.types.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.bot.types.types.reply_keyboard_markup import ReplyKeyboardMarkup
from telebox.bot.types.types.reply_keyboard_remove import ReplyKeyboardRemove
from telebox.bot.types.types.force_reply import ForceReply
from telebox.bot.types.types.input_file import InputFile
from telebox.bot.types.types.message_id import MessageId
from telebox.bot.types.types.input_media import InputMedia
from telebox.bot.types.types.input_media_audio import InputMediaAudio
from telebox.bot.types.types.input_media_document import InputMediaDocument
from telebox.bot.types.types.input_media_photo import InputMediaPhoto
from telebox.bot.types.types.input_media_video import InputMediaVideo
from telebox.bot.types.types.user_profile_photos import UserProfilePhotos
from telebox.bot.types.types.chat_permissions import ChatPermissions
from telebox.bot.types.types.file import File
from telebox.bot.types.types.chat_invite_link import ChatInviteLink
from telebox.bot.types.types.chat import Chat
from telebox.bot.types.types.forum_topic import ForumTopic
from telebox.bot.types.types.menu_button import MenuButton
from telebox.bot.types.types.poll import Poll
from telebox.bot.types.types.mask_position import MaskPosition
from telebox.bot.types.types.inline_query_result import InlineQueryResult
from telebox.bot.types.types.labeled_price import LabeledPrice
from telebox.bot.types.types.shipping_option import ShippingOption
from telebox.bot.types.types.passport_element_error import PassportElementError
from telebox.bot.types.types.game_high_score import GameHighScore
from telebox.bot.types.types.chat_member import ChatMember
from telebox.bot.types.types.chat_member_owner import ChatMemberOwner
from telebox.bot.types.types.chat_member_administrator import ChatMemberAdministrator
from telebox.utils.not_set import NotSet, NOT_SET
from telebox.context.utils import (
    get_event_chat_id,
    get_event_user_id,
    get_event_message_topic_id,
    get_event_sender_chat_id,
    get_event_message_id,
    get_event_callback_query_id,
    get_event_inline_query_id,
    get_event_shipping_query_id,
    get_event_pre_checkout_query_id
)


class ContextBot:

    def __init__(self, bot: Bot):
        self._bot = bot

    def send_message(
        self,
        text: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        entities: Optional[list[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_message(
            chat_id=get_event_chat_id(),
            text=text,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def forward_message_from_chat(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None
    ) -> Message:
        return self._bot.forward_message(
            chat_id=chat_id,
            from_chat_id=get_event_chat_id(),
            message_id=get_event_message_id(),
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            disable_notification=disable_notification,
            protect_content=protect_content
        )

    def forward_message_to_chat(
        self,
        from_chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None
    ):
        return self._bot.forward_message(
            chat_id=get_event_chat_id(),
            from_chat_id=from_chat_id,
            message_id=message_id,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            disable_notification=disable_notification,
            protect_content=protect_content
        )

    def copy_message_from_chat(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> MessageId:
        return self._bot.copy_message(
            chat_id=chat_id,
            from_chat_id=get_event_chat_id(),
            message_id=get_event_message_id(),
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def copy_message_to_chat(
        self,
        from_chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> MessageId:
        return self._bot.copy_message(
            chat_id=get_event_chat_id(),
            from_chat_id=from_chat_id,
            message_id=message_id,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def send_photo(
        self,
        photo: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_photo(
            chat_id=get_event_chat_id(),
            photo=photo,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def send_audio(
        self,
        audio: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumb: Union[InputFile, str, None] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_audio(
            chat_id=get_event_chat_id(),
            audio=audio,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumb=thumb,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def send_document(
        self,
        document: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        thumb: Union[InputFile, str, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_document(
            chat_id=get_event_chat_id(),
            document=document,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def send_video(
        self,
        video: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumb: Union[InputFile, str, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_video(
            chat_id=get_event_chat_id(),
            video=video,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def send_animation(
        self,
        animation: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumb: Union[InputFile, str, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_animation(
            chat_id=get_event_chat_id(),
            animation=animation,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def send_voice(
        self,
        voice: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_voice(
            chat_id=get_event_chat_id(),
            voice=voice,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def send_video_note(
        self,
        video_note: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        duration: Optional[int] = None,
        length: Optional[int] = None,
        thumb: Union[InputFile, str, None] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_video_note(
            chat_id=get_event_chat_id(),
            video_note=video_note,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            duration=duration,
            length=length,
            thumb=thumb,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def send_media_group(
        self,
        media: list[Union[InputMediaAudio,
                          InputMediaDocument,
                          InputMediaPhoto,
                          InputMediaVideo]],
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None
    ) -> list[Message]:
        return self._bot.send_media_group(
            chat_id=get_event_chat_id(),
            media=media,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply
        )

    def send_location(
        self,
        latitude: float,
        longitude: float,
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_location(
            chat_id=get_event_chat_id(),
            latitude=latitude,
            longitude=longitude,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def edit_message_live_location(
        self,
        latitude: float,
        longitude: float,
        message_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None,
        horizontal_accuracy: Optional[float] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._bot.edit_message_live_location(
            latitude=latitude,
            longitude=longitude,
            timeout_secs=timeout_secs,
            chat_id=get_event_chat_id(),
            message_id=get_event_message_id() if message_id is None else message_id,
            horizontal_accuracy=horizontal_accuracy,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            reply_markup=reply_markup
        )

    def stop_message_live_location(
        self,
        message_id: Optional[int],
        *,
        timeout_secs: Union[int, float, None] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._bot.stop_message_live_location(
            timeout_secs=timeout_secs,
            chat_id=get_event_chat_id(),
            message_id=get_event_message_id() if message_id is None else message_id,
            reply_markup=reply_markup
        )

    def send_venue(
        self,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_venue(
            chat_id=get_event_chat_id(),
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def send_contact(
        self,
        phone_number: str,
        first_name: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_contact(
            chat_id=get_event_chat_id(),
            phone_number=phone_number,
            first_name=first_name,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def send_poll(
        self,
        question: str,
        options: list[str],
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        is_anonymous: Optional[bool] = None,
        type_: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        correct_option_id: Optional[int] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Union[str, None, NotSet] = NOT_SET,
        explanation_entities: Optional[list[MessageEntity]] = None,
        open_period: Optional[int] = None,
        close_date: Optional[datetime] = None,
        is_closed: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_poll(
            chat_id=get_event_chat_id(),
            question=question,
            options=options,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            is_anonymous=is_anonymous,
            type_=type_,
            allows_multiple_answers=allows_multiple_answers,
            correct_option_id=correct_option_id,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def send_dice(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_dice(
            chat_id=get_event_chat_id(),
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def send_chat_action(
        self,
        action: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.send_chat_action(
            chat_id=get_event_chat_id(),
            action=action,
            timeout_secs=timeout_secs
        )

    def get_user_profile_photos(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> UserProfilePhotos:
        return self._bot.get_user_profile_photos(
            user_id=get_event_user_id(),
            timeout_secs=timeout_secs,
            offset=offset,
            limit=limit
        )

    def ban_chat_member(
        self,
        user_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None,
        until_date: Optional[datetime] = None,
        revoke_messages: Optional[bool] = None
    ) -> Literal[True]:
        return self._bot.ban_chat_member(
            chat_id=get_event_chat_id(),
            user_id=get_event_user_id() if user_id is None else user_id,
            timeout_secs=timeout_secs,
            until_date=until_date,
            revoke_messages=revoke_messages
        )

    def unban_chat_member(
        self,
        user_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None,
        only_if_banned: Optional[bool] = None
    ) -> Literal[True]:
        return self._bot.unban_chat_member(
            chat_id=get_event_chat_id(),
            user_id=get_event_user_id() if user_id is None else user_id,
            timeout_secs=timeout_secs,
            only_if_banned=only_if_banned
        )

    def restrict_chat_member(
        self,
        permissions: ChatPermissions,
        user_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None,
        until_date: Optional[datetime] = None
    ) -> Literal[True]:
        return self._bot.restrict_chat_member(
            chat_id=get_event_chat_id(),
            user_id=get_event_user_id() if user_id is None else user_id,
            permissions=permissions,
            timeout_secs=timeout_secs,
            until_date=until_date
        )

    def promote_chat_member(
        self,
        user_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None,
        is_anonymous: Optional[bool] = None,
        can_manage_chat: Optional[bool] = None,
        can_post_messages: Optional[bool] = None,
        can_edit_messages: Optional[bool] = None,
        can_delete_messages: Optional[bool] = None,
        can_manage_video_chats: Optional[bool] = None,
        can_restrict_members: Optional[bool] = None,
        can_promote_members: Optional[bool] = None,
        can_change_info: Optional[bool] = None,
        can_invite_users: Optional[bool] = None,
        can_pin_messages: Optional[bool] = None,
        can_manage_topics: Optional[bool] = None
    ) -> Literal[True]:
        return self._bot.promote_chat_member(
            chat_id=get_event_chat_id(),
            user_id=get_event_user_id() if user_id is None else user_id,
            timeout_secs=timeout_secs,
            is_anonymous=is_anonymous,
            can_manage_chat=can_manage_chat,
            can_post_messages=can_post_messages,
            can_edit_messages=can_edit_messages,
            can_delete_messages=can_delete_messages,
            can_manage_video_chats=can_manage_video_chats,
            can_restrict_members=can_restrict_members,
            can_promote_members=can_promote_members,
            can_change_info=can_change_info,
            can_invite_users=can_invite_users,
            can_pin_messages=can_pin_messages,
            can_manage_topics=can_manage_topics
        )

    def set_chat_administrator_custom_title(
        self,
        custom_title: str,
        user_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.set_chat_administrator_custom_title(
            chat_id=get_event_chat_id(),
            user_id=get_event_user_id() if user_id is None else user_id,
            custom_title=custom_title,
            timeout_secs=timeout_secs
        )

    def ban_chat_sender_chat(
        self,
        sender_chat_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.ban_chat_sender_chat(
            chat_id=get_event_chat_id(),
            sender_chat_id=get_event_sender_chat_id() if sender_chat_id is None else sender_chat_id,
            timeout_secs=timeout_secs
        )

    def unban_chat_sender_chat(
        self,
        sender_chat_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.unban_chat_sender_chat(
            chat_id=get_event_chat_id(),
            sender_chat_id=get_event_sender_chat_id() if sender_chat_id is None else sender_chat_id,
            timeout_secs=timeout_secs
        )

    def set_chat_permissions(
        self,
        permissions: ChatPermissions,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.set_chat_permissions(
            chat_id=get_event_chat_id(),
            permissions=permissions,
            timeout_secs=timeout_secs
        )

    def export_chat_invite_link(
        self,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> str:
        return self._bot.export_chat_invite_link(
            chat_id=get_event_chat_id(),
            timeout_secs=timeout_secs
        )

    def create_chat_invite_link(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        name: Optional[str] = None,
        expire_date: Optional[datetime] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None
    ) -> ChatInviteLink:
        return self._bot.create_chat_invite_link(
            chat_id=get_event_chat_id(),
            timeout_secs=timeout_secs,
            name=name,
            expire_date=expire_date,
            member_limit=member_limit,
            creates_join_request=creates_join_request
        )

    def edit_chat_invite_link(
        self,
        invite_link: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        name: Optional[str] = None,
        expire_date: Optional[datetime] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None
    ) -> ChatInviteLink:
        return self._bot.edit_chat_invite_link(
            chat_id=get_event_chat_id(),
            invite_link=invite_link,
            timeout_secs=timeout_secs,
            name=name,
            expire_date=expire_date,
            member_limit=member_limit,
            creates_join_request=creates_join_request
        )

    def revoke_chat_invite_link(
        self,
        invite_link: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> ChatInviteLink:
        return self._bot.revoke_chat_invite_link(
            chat_id=get_event_chat_id(),
            invite_link=invite_link,
            timeout_secs=timeout_secs
        )

    def approve_chat_join_request(
        self,
        user_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.approve_chat_join_request(
            chat_id=get_event_chat_id(),
            user_id=get_event_user_id() if user_id is None else user_id,
            timeout_secs=timeout_secs
        )

    def decline_chat_join_request(
        self,
        user_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.decline_chat_join_request(
            chat_id=get_event_chat_id(),
            user_id=get_event_user_id() if user_id is None else user_id,
            timeout_secs=timeout_secs
        )

    def set_chat_photo(
        self,
        photo: InputFile,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.set_chat_photo(
            chat_id=get_event_chat_id(),
            photo=photo,
            timeout_secs=timeout_secs
        )

    def delete_chat_photo(
        self,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.delete_chat_photo(
            chat_id=get_event_chat_id(),
            timeout_secs=timeout_secs
        )

    def set_chat_title(
        self,
        title: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.set_chat_title(
            chat_id=get_event_chat_id(),
            title=title,
            timeout_secs=timeout_secs
        )

    def set_chat_description(
        self,
        description: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.set_chat_description(
            chat_id=get_event_chat_id(),
            description=description,
            timeout_secs=timeout_secs
        )

    def pin_chat_message(
        self,
        message_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None,
        disable_notification: Optional[bool] = None
    ) -> Literal[True]:
        return self._bot.pin_chat_message(
            chat_id=get_event_chat_id(),
            message_id=get_event_message_id() if message_id is None else message_id,
            timeout_secs=timeout_secs,
            disable_notification=disable_notification
        )

    def unpin_chat_message(
        self,
        message_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.unpin_chat_message(
            chat_id=get_event_chat_id(),
            message_id=get_event_message_id() if message_id is None else message_id,
            timeout_secs=timeout_secs
        )

    def unpin_all_chat_messages(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
    ) -> Literal[True]:
        return self._bot.unpin_all_chat_messages(
            chat_id=get_event_chat_id(),
            timeout_secs=timeout_secs
        )

    def leave_chat(
        self,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.leave_chat(
            chat_id=get_event_chat_id(),
            timeout_secs=timeout_secs
        )

    def get_chat(
        self,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Chat:
        return self._bot.get_chat(
            chat_id=get_event_chat_id(),
            timeout_secs=timeout_secs
        )

    def get_chat_administrators(
        self,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> list[Union[ChatMemberOwner,
                    ChatMemberAdministrator]]:
        return self._bot.get_chat_administrators(
            chat_id=get_event_chat_id(),
            timeout_secs=timeout_secs
        )

    def get_chat_member_count(
        self,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> int:
        return self._bot.get_chat_member_count(
            chat_id=get_event_chat_id(),
            timeout_secs=timeout_secs
        )

    def get_chat_member(
        self,
        user_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> ChatMember:
        return self._bot.get_chat_member(
            chat_id=get_event_chat_id(),
            user_id=get_event_user_id() if user_id is None else user_id,
            timeout_secs=timeout_secs
        )

    def set_chat_sticker_set(
        self,
        sticker_set_name: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.set_chat_sticker_set(
            chat_id=get_event_chat_id(),
            sticker_set_name=sticker_set_name,
            timeout_secs=timeout_secs
        )

    def delete_chat_sticker_set(
        self,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.delete_chat_sticker_set(
            chat_id=get_event_chat_id(),
            timeout_secs=timeout_secs
        )

    def create_forum_topic(
        self,
        name: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        icon_color: Optional[int] = None,
        icon_custom_emoji_id: Optional[str] = None
    ) -> ForumTopic:
        return self._bot.create_forum_topic(
            chat_id=get_event_chat_id(),
            name=name,
            timeout_secs=timeout_secs,
            icon_color=icon_color,
            icon_custom_emoji_id=icon_custom_emoji_id
        )

    def edit_forum_topic(
        self,
        name: str,
        icon_custom_emoji_id: str,
        message_thread_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        if message_thread_id is None:
            message_thread_id = get_event_message_topic_id()

        return self._bot.edit_forum_topic(
            chat_id=get_event_chat_id(),
            message_thread_id=message_thread_id,
            name=name,
            icon_custom_emoji_id=icon_custom_emoji_id,
            timeout_secs=timeout_secs
        )

    def close_forum_topic(
        self,
        message_thread_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        if message_thread_id is None:
            message_thread_id = get_event_message_topic_id()

        return self._bot.close_forum_topic(
            chat_id=get_event_chat_id(),
            message_thread_id=message_thread_id,
            timeout_secs=timeout_secs
        )

    def reopen_forum_topic(
        self,
        message_thread_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        if message_thread_id is None:
            message_thread_id = get_event_message_topic_id()

        return self._bot.reopen_forum_topic(
            chat_id=get_event_chat_id(),
            message_thread_id=message_thread_id,
            timeout_secs=timeout_secs
        )

    def delete_forum_topic(
        self,
        message_thread_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        if message_thread_id is None:
            message_thread_id = get_event_message_topic_id()

        return self._bot.delete_forum_topic(
            chat_id=get_event_chat_id(),
            message_thread_id=message_thread_id,
            timeout_secs=timeout_secs
        )

    def unpin_all_forum_topic_messages(
        self,
        message_thread_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        if message_thread_id is None:
            message_thread_id = get_event_message_topic_id()

        return self._bot.unpin_all_forum_topic_messages(
            chat_id=get_event_chat_id(),
            message_thread_id=message_thread_id,
            timeout_secs=timeout_secs
        )

    def answer_callback_query(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        text: Optional[str] = None,
        show_alert: Optional[bool] = None,
        url: Optional[str] = None,
        cache_time: Optional[int] = None
    ) -> Literal[True]:
        return self._bot.answer_callback_query(
            callback_query_id=get_event_callback_query_id(),
            timeout_secs=timeout_secs,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time
        )

    def set_chat_menu_button(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        menu_button: Optional[MenuButton] = None
    ) -> Literal[True]:
        return self._bot.set_chat_menu_button(
            timeout_secs=timeout_secs,
            chat_id=get_event_chat_id(),
            menu_button=menu_button
        )

    def get_chat_menu_button(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
    ) -> Literal[True]:
        return self._bot.get_chat_menu_button(
            timeout_secs=timeout_secs,
            chat_id=get_event_chat_id()
        )

    def edit_message_text(
        self,
        text: str,
        message_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        entities: Optional[list[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._bot.edit_message_text(
            text=text,
            timeout_secs=timeout_secs,
            chat_id=get_event_chat_id(),
            message_id=get_event_message_id() if message_id is None else message_id,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup
        )

    def edit_message_caption(
        self,
        message_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._bot.edit_message_caption(
            timeout_secs=timeout_secs,
            chat_id=get_event_chat_id(),
            message_id=get_event_message_id() if message_id is None else message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            reply_markup=reply_markup
        )

    def edit_message_media(
        self,
        media: InputMedia,
        message_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._bot.edit_message_media(
            media=media,
            timeout_secs=timeout_secs,
            chat_id=get_event_chat_id(),
            message_id=get_event_message_id() if message_id is None else message_id,
            reply_markup=reply_markup
        )

    def edit_message_reply_markup(
        self,
        message_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._bot.edit_message_reply_markup(
            timeout_secs=timeout_secs,
            chat_id=get_event_chat_id(),
            message_id=get_event_message_id() if message_id is None else message_id,
            reply_markup=reply_markup
        )

    def stop_poll(
        self,
        message_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Poll:
        return self._bot.stop_poll(
            chat_id=get_event_chat_id(),
            message_id=get_event_message_id() if message_id is None else message_id,
            timeout_secs=timeout_secs,
            reply_markup=reply_markup
        )

    def delete_message(
        self,
        message_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.delete_message(
            chat_id=get_event_chat_id(),
            message_id=get_event_message_id() if message_id is None else message_id,
            timeout_secs=timeout_secs
        )

    def send_sticker(
        self,
        sticker: Union[InputFile, str],
        *,
        with_reply: bool = False,
        timeout_secs: Union[int, float, None] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._bot.send_sticker(
            chat_id=get_event_chat_id(),
            sticker=sticker,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def upload_sticker_file(
        self,
        png_sticker: InputFile,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> File:
        return self._bot.upload_sticker_file(
            user_id=get_event_user_id(),
            png_sticker=png_sticker,
            timeout_secs=timeout_secs
        )

    def create_new_sticker_set(
        self,
        name: str,
        title: str,
        emojis: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        png_sticker: Union[InputFile, str, None] = None,
        tgs_sticker: Optional[InputFile] = None,
        webm_sticker: Optional[InputFile] = None,
        contains_masks: Optional[bool] = None,
        mask_position: Optional[MaskPosition] = None
    ) -> Literal[True]:
        return self._bot.create_new_sticker_set(
            user_id=get_event_user_id(),
            name=name,
            title=title,
            emojis=emojis,
            timeout_secs=timeout_secs,
            png_sticker=png_sticker,
            tgs_sticker=tgs_sticker,
            webm_sticker=webm_sticker,
            contains_masks=contains_masks,
            mask_position=mask_position
        )

    def add_sticker_to_set(
        self,
        name: str,
        emojis: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        png_sticker: Union[InputFile, str, None] = None,
        tgs_sticker: Optional[InputFile] = None,
        webm_sticker: Optional[InputFile] = None,
        mask_position: Optional[MaskPosition] = None
    ) -> Literal[True]:
        return self._bot.add_sticker_to_set(
            user_id=get_event_user_id(),
            name=name,
            emojis=emojis,
            timeout_secs=timeout_secs,
            png_sticker=png_sticker,
            tgs_sticker=tgs_sticker,
            webm_sticker=webm_sticker,
            mask_position=mask_position
        )

    def set_sticker_set_thumb(
        self,
        name: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        thumb: Union[InputFile, str, None] = None
    ) -> Literal[True]:
        return self._bot.set_sticker_set_thumb(
            name=name,
            user_id=get_event_user_id(),
            timeout_secs=timeout_secs,
            thumb=thumb
        )

    def answer_inline_query(
        self,
        results: list[InlineQueryResult],
        *,
        timeout_secs: Union[int, float, None] = None,
        cache_time: Optional[int] = None,
        is_personal: Optional[bool] = None,
        next_offset: Optional[str] = None,
        switch_pm_text: Optional[str] = None,
        switch_pm_parameter: Optional[str] = None
    ) -> Literal[True]:
        return self._bot.answer_inline_query(
            inline_query_id=get_event_inline_query_id(),
            results=results,
            timeout_secs=timeout_secs,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter
        )

    def send_invoice(
        self,
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: list[LabeledPrice],
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[list[int]] = None,
        start_parameter: Optional[str] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._bot.send_invoice(
            chat_id=get_event_chat_id(),
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
            start_parameter=start_parameter,
            provider_data=provider_data,
            photo_url=photo_url,
            photo_size=photo_size,
            photo_width=photo_width,
            photo_height=photo_height,
            need_name=need_name,
            need_phone_number=need_phone_number,
            need_email=need_email,
            need_shipping_address=need_shipping_address,
            send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider,
            is_flexible=is_flexible,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def answer_shipping_query(
        self,
        ok: bool,
        *,
        timeout_secs: Union[int, float, None] = None,
        shipping_options: Optional[list[ShippingOption]] = None,
        error_message: Optional[str] = None
    ) -> Literal[True]:
        return self._bot.answer_shipping_query(
            shipping_query_id=get_event_shipping_query_id(),
            ok=ok,
            timeout_secs=timeout_secs,
            shipping_options=shipping_options,
            error_message=error_message
        )

    def answer_pre_checkout_query(
        self,
        ok: bool,
        *,
        timeout_secs: Union[int, float, None] = None,
        error_message: Optional[str] = None
    ) -> Literal[True]:
        return self._bot.answer_pre_checkout_query(
            pre_checkout_query_id=get_event_pre_checkout_query_id(),
            ok=ok,
            timeout_secs=timeout_secs,
            error_message=error_message
        )

    def set_passport_data_errors(
        self,
        errors: list[PassportElementError],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._bot.set_passport_data_errors(
            user_id=get_event_user_id(),
            errors=errors,
            timeout_secs=timeout_secs
        )

    def send_game(
        self,
        game_short_name: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        with_reply: bool = False,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._bot.send_game(
            chat_id=get_event_chat_id(),
            game_short_name=game_short_name,
            timeout_secs=timeout_secs,
            message_thread_id=get_event_message_topic_id(strictly=False),
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=get_event_message_id() if with_reply else None,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

    def set_game_score(
        self,
        score: int,
        user_id: Optional[int] = None,
        message_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None,
        force: Optional[bool] = None,
        disable_edit_message: Optional[bool] = None
    ) -> Message:
        return self._bot.set_game_score(
            user_id=get_event_user_id() if user_id is None else user_id,
            score=score,
            timeout_secs=timeout_secs,
            force=force,
            disable_edit_message=disable_edit_message,
            chat_id=get_event_chat_id(),
            message_id=get_event_message_id() if message_id is None else message_id
        )

    def get_game_high_scores(
        self,
        user_id: Optional[int] = None,
        message_id: Optional[int] = None,
        *,
        timeout_secs: Union[int, float, None] = None,
    ) -> list[GameHighScore]:
        return self._bot.get_game_high_scores(
            user_id=get_event_user_id() if user_id is None else user_id,
            timeout_secs=timeout_secs,
            chat_id=get_event_chat_id(),
            message_id=get_event_message_id() if message_id is None else message_id
        )
