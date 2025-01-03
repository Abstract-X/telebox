from typing import Union, Optional, Any, Literal, IO, BinaryIO
import time
from datetime import datetime
from dataclasses import is_dataclass
import secrets
from http import HTTPStatus

from requests import Session, Response, RequestException
from requests_toolbelt import MultipartEncoder

from telebox.bot.utils.converters import DataclassConverter, get_timestamp
from telebox.bot.errors import get_request_error, BotError, RetryAfterError, InternalServerError
from telebox.bot.consts import chat_member_statuses
from telebox.bot.enums.input_file_type import InputFileType
from telebox.bot.types.types.response_parameters import ResponseParameters
from telebox.bot.types.types.update import Update
from telebox.bot.types.types.webhook_info import WebhookInfo
from telebox.bot.types.types.user import User
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
from telebox.bot.types.types.bot_command import BotCommand
from telebox.bot.types.types.bot_command_scope import BotCommandScope
from telebox.bot.types.types.bot_description import BotDescription
from telebox.bot.types.types.bot_name import BotName
from telebox.bot.types.types.bot_short_description import BotShortDescription
from telebox.bot.types.types.menu_button import MenuButton
from telebox.bot.types.types.chat_administrator_rights import ChatAdministratorRights
from telebox.bot.types.types.forum_topic import ForumTopic
from telebox.bot.types.types.poll import Poll
from telebox.bot.types.types.sticker import Sticker
from telebox.bot.types.types.sticker_set import StickerSet
from telebox.bot.types.types.mask_position import MaskPosition
from telebox.bot.types.types.input_sticker import InputSticker
from telebox.bot.types.types.inline_query_result import InlineQueryResult
from telebox.bot.types.types.sent_web_app_message import SentWebAppMessage
from telebox.bot.types.types.labeled_price import LabeledPrice
from telebox.bot.types.types.shipping_option import ShippingOption
from telebox.bot.types.types.passport_element_error import PassportElementError
from telebox.bot.types.types.game_high_score import GameHighScore
from telebox.bot.types.types.chat_member import ChatMember
from telebox.bot.types.types.chat_member_owner import ChatMemberOwner
from telebox.bot.types.types.chat_member_administrator import ChatMemberAdministrator
from telebox.bot.types.types.chat_member_member import ChatMemberMember
from telebox.bot.types.types.chat_member_restricted import ChatMemberRestricted
from telebox.bot.types.types.chat_member_left import ChatMemberLeft
from telebox.bot.types.types.chat_member_banned import ChatMemberBanned
from telebox.bot.types.types.inline_query_results_button import InlineQueryResultsButton
from telebox.bot.types.types.reaction_type import ReactionType
from telebox.bot.types.types.reply_parameters import ReplyParameters
from telebox.bot.types.types.link_preview_options import LinkPreviewOptions
from telebox.bot.types.types.user_chat_boosts import UserChatBoosts
from telebox.bot.types.types.business_connection import BusinessConnection
from telebox.bot.types.types.input_poll_option import InputPollOption
from telebox.bot.types.types.chat_full_info import ChatFullInfo
from telebox.bot.types.types.star_transactions import StarTransactions
from telebox.bot.types.types.input_paid_media import InputPaidMedia
from telebox.bot.types.types.inline_query_result_article import InlineQueryResultArticle
from telebox.bot.types.types.inline_query_result_photo import InlineQueryResultPhoto
from telebox.bot.types.types.inline_query_result_gif import InlineQueryResultGif
from telebox.bot.types.types.inline_query_result_mpeg4_gif import InlineQueryResultMpeg4Gif
from telebox.bot.types.types.inline_query_result_video import InlineQueryResultVideo
from telebox.bot.types.types.inline_query_result_audio import InlineQueryResultAudio
from telebox.bot.types.types.inline_query_result_voice import InlineQueryResultVoice
from telebox.bot.types.types.inline_query_result_document import InlineQueryResultDocument
from telebox.bot.types.types.inline_query_result_location import InlineQueryResultLocation
from telebox.bot.types.types.inline_query_result_venue import InlineQueryResultVenue
from telebox.bot.types.types.inline_query_result_contact import InlineQueryResultContact
from telebox.bot.types.types.inline_query_result_cached_photo import InlineQueryResultCachedPhoto
from telebox.bot.types.types.inline_query_result_cached_gif import InlineQueryResultCachedGif
from telebox.bot.types.types.inline_query_result_cached_mpeg4_gif import (
    InlineQueryResultCachedMpeg4Gif
)
from telebox.bot.types.types.inline_query_result_cached_sticker import (
    InlineQueryResultCachedSticker
)
from telebox.bot.types.types.inline_query_result_cached_document import (
    InlineQueryResultCachedDocument
)
from telebox.bot.types.types.inline_query_result_cached_video import InlineQueryResultCachedVideo
from telebox.bot.types.types.inline_query_result_cached_voice import InlineQueryResultCachedVoice
from telebox.bot.types.types.inline_query_result_cached_audio import InlineQueryResultCachedAudio
from telebox.bot.types.types.input_text_message_content import InputTextMessageContent
from telebox.bot.context import Context
from telebox.utils.not_set import NotSet, NOT_SET
from telebox.utils.serialization import get_serialized_data


API_URL = "https://api.telegram.org"
_CHAT_MEMBER_TYPES = {
    chat_member_statuses.CREATOR: ChatMemberOwner,
    chat_member_statuses.ADMINISTRATOR: ChatMemberAdministrator,
    chat_member_statuses.MEMBER: ChatMemberMember,
    chat_member_statuses.RESTRICTED: ChatMemberRestricted,
    chat_member_statuses.LEFT: ChatMemberLeft,
    chat_member_statuses.KICKED: ChatMemberBanned
}


class Bot:

    def __init__(
        self,
        session: Session,
        token: str,
        *,
        api_url: str = API_URL,
        parse_mode: Union[str, NotSet] = NOT_SET,
        timeout_secs: Union[int, float, None] = 300,
        retries: int = 0,
        retry_delay_secs: Union[int, float] = 0,
        wait_on_rate_limit: bool = False,
        use_cache: bool = True
    ):
        if retries < 0:
            raise ValueError("Number of retries cannot be less than zero!")

        self.session = session
        self.token = token
        self.api_url = api_url.lower().rstrip("/")
        self._parse_mode = parse_mode
        self._timeout_secs = timeout_secs
        self._retries = retries
        self._retry_delay_secs = retry_delay_secs
        self._wait_on_rate_limit = wait_on_rate_limit
        self._use_cache = use_cache
        self.context = Context(self)
        self._converter = DataclassConverter()
        self._user: Optional[User] = None
        self._cached_file_ids: dict[tuple[str, str], str] = {}

    @property
    def user(self) -> User:
        if self._user is None:
            raise BotError(
                "Bot user was not loaded! To use this property, you need to call "
                "bot.get_me method at least once!"
            )

        return self._user

    def get_updates(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        timeout: Optional[int] = None,
        allowed_updates: Optional[list[str]] = None
    ) -> list[Update]:
        return [
            self._converter.get_object(data=i, class_=Update)
            for i in self._send_request(
                method="getUpdates",
                parameters={
                    "offset": offset,
                    "limit": limit,
                    "timeout": timeout,
                    "allowed_updates": allowed_updates
                },
                timeout_secs=timeout_secs
            )
        ]

    def set_webhook(
        self,
        url: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        certificate: Optional[InputFile] = None,
        ip_address: Optional[str] = None,
        max_connections: Optional[int] = None,
        allowed_updates: Optional[list[str]] = None,
        drop_pending_updates: Optional[bool] = None,
        secret_token: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setWebhook",
            parameters={
                "url": url,
                "certificate": certificate,
                "ip_address": ip_address,
                "max_connections": max_connections,
                "allowed_updates": allowed_updates,
                "drop_pending_updates": drop_pending_updates,
                "secret_token": secret_token
            },
            timeout_secs=timeout_secs
        )

    def delete_webhook(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        drop_pending_updates: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteWebhook",
            parameters={
                "drop_pending_updates": drop_pending_updates
            },
            timeout_secs=timeout_secs
        )

    def get_webhook_info(
        self,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> WebhookInfo:
        return self._converter.get_object(
            data=self._send_request(method="getWebhookInfo", timeout_secs=timeout_secs),
            class_=WebhookInfo
        )

    def get_me(self, *, timeout_secs: Union[int, float, None] = None) -> User:
        self._user = self._converter.get_object(
            data=self._send_request(method="getMe", timeout_secs=timeout_secs),
            class_=User
        )

        return self._user

    def log_out(self, *, timeout_secs: Union[int, float, None] = None) -> Literal[True]:
        return self._send_request(method="logOut", timeout_secs=timeout_secs)

    def close(self, *, timeout_secs: Union[int, float, None] = None) -> Literal[True]:
        return self._send_request(method="close", timeout_secs=timeout_secs)

    def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        entities: Optional[list[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._converter.get_object(
            data=self._send_request(
                method="sendMessage",
                parameters={
                    "chat_id": chat_id,
                    "text": text,
                    "message_thread_id": message_thread_id,
                    "business_connection_id": business_connection_id,
                    "parse_mode": self._get_parse_mode(parse_mode, with_entities=bool(entities)),
                    "entities": entities,
                    "link_preview_options": link_preview_options,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def forward_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None
    ) -> Message:
        return self._converter.get_object(
            data=self._send_request(
                method="forwardMessage",
                parameters={
                    "chat_id": chat_id,
                    "from_chat_id": from_chat_id,
                    "message_id": message_id,
                    "message_thread_id": message_thread_id,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def forward_messages(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: list[int],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None
    ) -> list[MessageId]:
        return [
            self._converter.get_object(data=i, class_=MessageId)
            for i in self._send_request(
                method="forwardMessages",
                parameters={
                    "chat_id": chat_id,
                    "from_chat_id": from_chat_id,
                    "message_ids": message_ids,
                    "message_thread_id": message_thread_id,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content
                },
                timeout_secs=timeout_secs
            )
        ]

    def copy_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> MessageId:
        return self._converter.get_object(
            data=self._send_request(
                method="copyMessage",
                parameters={
                    "chat_id": chat_id,
                    "from_chat_id": from_chat_id,
                    "message_id": message_id,
                    "message_thread_id": message_thread_id,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "show_caption_above_media": show_caption_above_media,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=MessageId
        )

    def copy_messages(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: list[int],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        remove_caption: Optional[bool] = None
    ) -> list[MessageId]:
        return [
            self._converter.get_object(data=i, class_=MessageId)
            for i in self._send_request(
                method="copyMessages",
                parameters={
                    "chat_id": chat_id,
                    "from_chat_id": from_chat_id,
                    "message_ids": message_ids,
                    "message_thread_id": message_thread_id,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "remove_caption": remove_caption
                },
                timeout_secs=timeout_secs
            )
        ]

    def send_photo(
        self,
        chat_id: Union[int, str],
        photo: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        message = self._converter.get_object(
            data=self._send_request(
                method="sendPhoto",
                parameters={
                    "chat_id": chat_id,
                    "photo": self._get_file(photo),
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "show_caption_above_media": show_caption_above_media,
                    "has_spoiler": has_spoiler,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

        if self._use_cache:
            self._set_cached_file_id(
                file=photo,
                file_id=message.best_photo.file_id
            )

        return message

    def send_audio(
        self,
        chat_id: Union[int, str],
        audio: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumbnail: Union[InputFile, str, None] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        message = self._converter.get_object(
            data=self._send_request(
                method="sendAudio",
                parameters={
                    "chat_id": chat_id,
                    "audio": self._get_file(audio),
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "duration": duration,
                    "performer": performer,
                    "title": title,
                    "thumbnail": thumbnail,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

        if self._use_cache:
            self._set_cached_file_id(
                file=audio,
                file_id=message.audio.file_id
            )

        return message

    def send_document(
        self,
        chat_id: Union[int, str],
        document: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        thumbnail: Union[InputFile, str, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        message = self._converter.get_object(
            data=self._send_request(
                method="sendDocument",
                parameters={
                    "chat_id": chat_id,
                    "document": self._get_file(document),
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "thumbnail": thumbnail,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "disable_content_type_detection": disable_content_type_detection,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

        if self._use_cache:
            self._set_cached_file_id(
                file=document,
                file_id=message.document.file_id
            )

        return message

    def send_video(
        self,
        chat_id: Union[int, str],
        video: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Union[InputFile, str, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        message = self._converter.get_object(
            data=self._send_request(
                method="sendVideo",
                parameters={
                    "chat_id": chat_id,
                    "video": self._get_file(video),
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "duration": duration,
                    "width": width,
                    "height": height,
                    "thumbnail": thumbnail,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "show_caption_above_media": show_caption_above_media,
                    "has_spoiler": has_spoiler,
                    "supports_streaming": supports_streaming,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

        if self._use_cache:
            self._set_cached_file_id(
                file=video,
                file_id=message.video.file_id
            )

        return message

    def send_animation(
        self,
        chat_id: Union[int, str],
        animation: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Union[InputFile, str, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        message = self._converter.get_object(
            data=self._send_request(
                method="sendAnimation",
                parameters={
                    "chat_id": chat_id,
                    "animation": self._get_file(animation),
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "duration": duration,
                    "width": width,
                    "height": height,
                    "thumbnail": thumbnail,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "show_caption_above_media": show_caption_above_media,
                    "has_spoiler": has_spoiler,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

        if self._use_cache:
            self._set_cached_file_id(
                file=animation,
                file_id=message.animation.file_id
            )

        return message

    def send_voice(
        self,
        chat_id: Union[int, str],
        voice: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        message = self._converter.get_object(
            data=self._send_request(
                method="sendVoice",
                parameters={
                    "chat_id": chat_id,
                    "voice": self._get_file(voice),
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "duration": duration,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

        if self._use_cache:
            self._set_cached_file_id(
                file=voice,
                file_id=message.voice.file_id
            )

        return message

    def send_video_note(
        self,
        chat_id: Union[int, str],
        video_note: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        duration: Optional[int] = None,
        length: Optional[int] = None,
        thumbnail: Union[InputFile, str, None] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        message = self._converter.get_object(
            data=self._send_request(
                method="sendVideoNote",
                parameters={
                    "chat_id": chat_id,
                    "video_note": self._get_file(video_note),
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "duration": duration,
                    "length": length,
                    "thumbnail": thumbnail,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

        if self._use_cache:
            self._set_cached_file_id(
                file=video_note,
                file_id=message.video_note.file_id
            )

        return message

    def send_media_group(
        self,
        chat_id: Union[int, str],
        media: list[Union[InputMediaAudio,
                          InputMediaDocument,
                          InputMediaPhoto,
                          InputMediaVideo]],
        *,
        timeout_secs: Union[int, float, None] = None,
        caption: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Union[list[MessageEntity], None, NotSet] = NOT_SET,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None
    ) -> list[Message]:
        if caption is not NOT_SET:
            media[0].caption = caption

        if caption_entities is not NOT_SET:
            media[0].caption_entities = caption_entities

        if parse_mode is not NOT_SET:
            media[0].parse_mode = parse_mode

        media_ = []

        for i in media:
            class_ = type(i)
            data = self._converter.get_data(i)
            data["media"] = self._get_file(data["media"])
            data["parse_mode"] = self._get_parse_mode(
                parse_mode=data.get("parse_mode", NOT_SET),
                with_entities=bool(
                    data.get("caption_entities")
                )
            )
            media_.append(
                self._converter.get_object(
                    data=data,
                    class_=class_
                )
            )

        messages = [
            self._converter.get_object(data=i, class_=Message)
            for i in self._send_request(
                method="sendMediaGroup",
                parameters={
                    "chat_id": chat_id,
                    "media": media_,
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters
                },
                timeout_secs=timeout_secs
            )
        ]

        if self._use_cache:
            for single_media, message in zip(media, messages):
                if isinstance(single_media, InputMediaPhoto):
                    self._set_cached_file_id(
                        file=single_media.media,
                        file_id=message.best_photo.file_id
                    )
                elif isinstance(single_media, InputMediaVideo):
                    self._set_cached_file_id(
                        file=single_media.media,
                        file_id=message.video.file_id
                    )
                elif isinstance(single_media, InputMediaAudio):
                    self._set_cached_file_id(
                        file=single_media.media,
                        file_id=message.audio.file_id
                    )
                elif isinstance(single_media, InputMediaDocument):
                    self._set_cached_file_id(
                        file=single_media.media,
                        file_id=message.document.file_id
                    )

        return messages

    def send_location(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._converter.get_object(
            data=self._send_request(
                method="sendLocation",
                parameters={
                    "chat_id": chat_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "horizontal_accuracy": horizontal_accuracy,
                    "live_period": live_period,
                    "heading": heading,
                    "proximity_alert_radius": proximity_alert_radius,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def edit_message_live_location(
        self,
        latitude: float,
        longitude: float,
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        live_period: Optional[int] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        horizontal_accuracy: Optional[float] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="editMessageLiveLocation",
            parameters={
                "latitude": latitude,
                "longitude": longitude,
                "live_period": live_period,
                "business_connection_id": business_connection_id,
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "horizontal_accuracy": horizontal_accuracy,
                "heading": heading,
                "proximity_alert_radius": proximity_alert_radius,
                "reply_markup": reply_markup
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._converter.get_object(
            data=data,
            class_=Message
        )

    def stop_message_live_location(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="stopMessageLiveLocation",
            parameters={
                "business_connection_id": business_connection_id,
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "reply_markup": reply_markup
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._converter.get_object(
            data=data,
            class_=Message
        )

    def send_venue(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._converter.get_object(
            data=self._send_request(
                method="sendVenue",
                parameters={
                    "chat_id": chat_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "title": title,
                    "address": address,
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "foursquare_id": foursquare_id,
                    "foursquare_type": foursquare_type,
                    "google_place_id": google_place_id,
                    "google_place_type": google_place_type,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_contact(
        self,
        chat_id: Union[int, str],
        phone_number: str,
        first_name: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._converter.get_object(
            data=self._send_request(
                method="sendContact",
                parameters={
                    "chat_id": chat_id,
                    "phone_number": phone_number,
                    "first_name": first_name,
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "last_name": last_name,
                    "vcard": vcard,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_poll(
        self,
        chat_id: Union[int, str],
        question: str,
        options: list[InputPollOption],
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        question_parse_mode: Optional[str] = None,
        question_entities: Optional[list[MessageEntity]] = None,
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
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        options_ = []

        for i in options:
            data = self._converter.get_data(i)
            data["text_parse_mode"] = self._get_parse_mode(
                parse_mode=data.get("text_parse_mode", NOT_SET),
                with_entities=bool(
                    data.get("text_entities")
                )
            )
            options_.append(
                self._converter.get_object(
                    data=data,
                    class_=InputPollOption
                )
            )

        return self._converter.get_object(
            data=self._send_request(
                method="sendPoll",
                parameters={
                    "chat_id": chat_id,
                    "question": question,
                    "options": options_,
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "question_parse_mode": self._get_parse_mode(
                        question_parse_mode,
                        with_entities=bool(question_entities)
                    ),
                    "question_entities": question_entities,
                    "is_anonymous": is_anonymous,
                    "type": type_,
                    "allows_multiple_answers": allows_multiple_answers,
                    "correct_option_id": correct_option_id,
                    "explanation": explanation,
                    "explanation_parse_mode": self._get_parse_mode(
                        explanation_parse_mode,
                        with_entities=bool(explanation_entities)
                    ),
                    "explanation_entities": explanation_entities,
                    "open_period": open_period,
                    "close_date": close_date,
                    "is_closed": is_closed,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_dice(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._converter.get_object(
            data=self._send_request(
                method="sendDice",
                parameters={
                    "chat_id": chat_id,
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "emoji": emoji,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_chat_action(
        self,
        chat_id: Union[int, str],
        action: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None
    ) -> Literal[True]:
        return self._send_request(
            method="sendChatAction",
            parameters={
                "chat_id": chat_id,
                "action": action,
                "business_connection_id": business_connection_id,
                "message_thread_id": message_thread_id
            },
            timeout_secs=timeout_secs
        )

    def set_message_reaction(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        reaction: Optional[list[ReactionType]] = None,
        is_big: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setMessageReaction",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id,
                "reaction": reaction,
                "is_big": is_big
            },
            timeout_secs=timeout_secs
        )

    def get_user_profile_photos(
        self,
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> UserProfilePhotos:
        return self._converter.get_object(
            data=self._send_request(
                method="getUserProfilePhotos",
                parameters={
                    "user_id": user_id,
                    "offset": offset,
                    "limit": limit
                },
                timeout_secs=timeout_secs
            ),
            class_=UserProfilePhotos
        )

    def get_file(
        self,
        file_id: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> File:
        return self._converter.get_object(
            data=self._send_request(
                method="getFile",
                parameters={
                    "file_id": file_id
                },
                timeout_secs=timeout_secs
            ),
            class_=File
        )

    def ban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        until_date: Optional[datetime] = None,
        revoke_messages: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="banChatMember",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id,
                "until_date": until_date,
                "revoke_messages": revoke_messages
            },
            timeout_secs=timeout_secs
        )

    def unban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        only_if_banned: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unbanChatMember",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id,
                "only_if_banned": only_if_banned
            },
            timeout_secs=timeout_secs
        )

    def restrict_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        permissions: ChatPermissions,
        *,
        timeout_secs: Union[int, float, None] = None,
        use_independent_chat_permissions: Optional[bool] = None,
        until_date: Optional[datetime] = None
    ) -> Literal[True]:
        return self._send_request(
            method="restrictChatMember",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id,
                "permissions": permissions,
                "use_independent_chat_permissions": use_independent_chat_permissions,
                "until_date": until_date
            },
            timeout_secs=timeout_secs
        )

    def promote_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
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
        can_post_stories: Optional[bool] = None,
        can_edit_stories: Optional[bool] = None,
        can_delete_stories: Optional[bool] = None,
        can_manage_topics: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="promoteChatMember",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id,
                "is_anonymous": is_anonymous,
                "can_manage_chat": can_manage_chat,
                "can_post_messages": can_post_messages,
                "can_edit_messages": can_edit_messages,
                "can_delete_messages": can_delete_messages,
                "can_manage_video_chats": can_manage_video_chats,
                "can_restrict_members": can_restrict_members,
                "can_promote_members": can_promote_members,
                "can_change_info": can_change_info,
                "can_invite_users": can_invite_users,
                "can_pin_messages": can_pin_messages,
                "can_post_stories": can_post_stories,
                "can_edit_stories": can_edit_stories,
                "can_delete_stories": can_delete_stories,
                "can_manage_topics": can_manage_topics
            },
            timeout_secs=timeout_secs
        )

    def set_chat_administrator_custom_title(
        self,
        chat_id: Union[int, str],
        user_id: int,
        custom_title: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatAdministratorCustomTitle",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id,
                "custom_title": custom_title
            },
            timeout_secs=timeout_secs
        )

    def ban_chat_sender_chat(
        self,
        chat_id: Union[int, str],
        sender_chat_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="banChatSenderChat",
            parameters={
                "chat_id": chat_id,
                "sender_chat_id": sender_chat_id
            },
            timeout_secs=timeout_secs
        )

    def unban_chat_sender_chat(
        self,
        chat_id: Union[int, str],
        sender_chat_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unbanChatSenderChat",
            parameters={
                "chat_id": chat_id,
                "sender_chat_id": sender_chat_id
            },
            timeout_secs=timeout_secs
        )

    def set_chat_permissions(
        self,
        chat_id: Union[int, str],
        permissions: ChatPermissions,
        *,
        timeout_secs: Union[int, float, None] = None,
        use_independent_chat_permissions: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatPermissions",
            parameters={
                "chat_id": chat_id,
                "permissions": permissions,
                "use_independent_chat_permissions": use_independent_chat_permissions
            },
            timeout_secs=timeout_secs
        )

    def export_chat_invite_link(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> str:
        return self._send_request(
            method="exportChatInviteLink",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def create_chat_invite_link(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        name: Optional[str] = None,
        expire_date: Optional[datetime] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None
    ) -> ChatInviteLink:
        return self._converter.get_object(
            data=self._send_request(
                method="createChatInviteLink",
                parameters={
                    "chat_id": chat_id,
                    "name": name,
                    "expire_date": expire_date,
                    "member_limit": member_limit,
                    "creates_join_request": creates_join_request
                },
                timeout_secs=timeout_secs
            ),
            class_=ChatInviteLink
        )

    def edit_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        name: Optional[str] = None,
        expire_date: Optional[datetime] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None
    ) -> ChatInviteLink:
        return self._converter.get_object(
            data=self._send_request(
                method="editChatInviteLink",
                parameters={
                    "chat_id": chat_id,
                    "invite_link": invite_link,
                    "name": name,
                    "expire_date": expire_date,
                    "member_limit": member_limit,
                    "creates_join_request": creates_join_request
                },
                timeout_secs=timeout_secs
            ),
            class_=ChatInviteLink
        )

    def revoke_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> ChatInviteLink:
        return self._converter.get_object(
            data=self._send_request(
                method="revokeChatInviteLink",
                parameters={
                    "chat_id": chat_id,
                    "invite_link": invite_link
                },
                timeout_secs=timeout_secs
            ),
            class_=ChatInviteLink
        )

    def approve_chat_join_request(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="approveChatJoinRequest",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id
            },
            timeout_secs=timeout_secs
        )

    def decline_chat_join_request(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="declineChatJoinRequest",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id
            },
            timeout_secs=timeout_secs
        )

    def set_chat_photo(
        self,
        chat_id: Union[int, str],
        photo: InputFile,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatPhoto",
            parameters={
                "chat_id": chat_id,
                "photo": photo
            },
            timeout_secs=timeout_secs
        )

    def delete_chat_photo(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteChatPhoto",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )
    
    def set_chat_title(
        self,
        chat_id: Union[int, str],
        title: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatTitle",
            parameters={
                "chat_id": chat_id,
                "title": title
            },
            timeout_secs=timeout_secs
        )

    def set_chat_description(
        self,
        chat_id: Union[int, str],
        description: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatDescription",
            parameters={
                "chat_id": chat_id,
                "description": description
            },
            timeout_secs=timeout_secs
        )

    def pin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        disable_notification: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="pinChatMessage",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id,
                "disable_notification": disable_notification
            },
            timeout_secs=timeout_secs
        )

    def unpin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unpinChatMessage",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id
            },
            timeout_secs=timeout_secs
        )

    def unpin_all_chat_messages(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None,
    ) -> Literal[True]:
        return self._send_request(
            method="unpinAllChatMessages",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def leave_chat(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="leaveChat",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def get_chat(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> ChatFullInfo:
        return self._converter.get_object(
            data=self._send_request(
                method="getChat",
                parameters={
                    "chat_id": chat_id
                },
                timeout_secs=timeout_secs
            ),
            class_=ChatFullInfo
        )

    def get_chat_administrators(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> list[Union[ChatMemberOwner,
                    ChatMemberAdministrator]]:
        return [
            self._converter.get_object(data=i, class_=_CHAT_MEMBER_TYPES[i["status"]])
            for i in self._send_request(
                method="getChatAdministrators",
                parameters={
                    "chat_id": chat_id
                },
                timeout_secs=timeout_secs
            )
        ]

    def get_chat_member_count(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> int:
        return self._send_request(
            method="getChatMemberCount",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def get_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> ChatMember:
        data = self._send_request(
            method="getChatMember",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id
            },
            timeout_secs=timeout_secs
        )

        return self._converter.get_object(
            data=data,
            class_=_CHAT_MEMBER_TYPES[data["status"]]
        )

    def set_chat_sticker_set(
        self,
        chat_id: Union[int, str],
        sticker_set_name: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatStickerSet",
            parameters={
                "chat_id": chat_id,
                "sticker_set_name": sticker_set_name
            },
            timeout_secs=timeout_secs
        )

    def delete_chat_sticker_set(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteChatStickerSet",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def get_forum_topic_icon_stickers(
        self,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> list[Sticker]:
        return [
            self._converter.get_object(data=i, class_=Sticker)
            for i in self._send_request(
                method="getForumTopicIconStickers",
                timeout_secs=timeout_secs
            )
        ]

    def create_forum_topic(
        self,
        chat_id: Union[int, str],
        name: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        icon_color: Optional[int] = None,
        icon_custom_emoji_id: Optional[str] = None
    ) -> ForumTopic:
        return self._converter.get_object(
            data=self._send_request(
                method="createForumTopic",
                parameters={
                    "chat_id": chat_id,
                    "name": name,
                    "icon_color": icon_color,
                    "icon_custom_emoji_id": icon_custom_emoji_id
                },
                timeout_secs=timeout_secs
            ),
            class_=ForumTopic
        )

    def edit_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        name: Optional[str] = None,
        icon_custom_emoji_id: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="editForumTopic",
            parameters={
                "chat_id": chat_id,
                "message_thread_id": message_thread_id,
                "name": name,
                "icon_custom_emoji_id": icon_custom_emoji_id
            },
            timeout_secs=timeout_secs
        )

    def close_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="closeForumTopic",
            parameters={
                "chat_id": chat_id,
                "message_thread_id": message_thread_id
            },
            timeout_secs=timeout_secs
        )

    def reopen_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="reopenForumTopic",
            parameters={
                "chat_id": chat_id,
                "message_thread_id": message_thread_id
            },
            timeout_secs=timeout_secs
        )
    
    def delete_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteForumTopic",
            parameters={
                "chat_id": chat_id,
                "message_thread_id": message_thread_id
            },
            timeout_secs=timeout_secs
        )

    def unpin_all_forum_topic_messages(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unpinAllForumTopicMessages",
            parameters={
                "chat_id": chat_id,
                "message_thread_id": message_thread_id
            },
            timeout_secs=timeout_secs
        )

    def edit_general_forum_topic(
        self,
        chat_id: Union[int, str],
        name: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="editGeneralForumTopic",
            parameters={
                "chat_id": chat_id,
                "name": name
            },
            timeout_secs=timeout_secs
        )

    def close_general_forum_topic(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="closeGeneralForumTopic",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def reopen_general_forum_topic(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="reopenGeneralForumTopic",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def hide_general_forum_topic(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="hideGeneralForumTopic",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def unhide_general_forum_topic(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unhideGeneralForumTopic",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def unpin_all_general_forum_topic_messages(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unpinAllGeneralForumTopicMessages",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def answer_callback_query(
        self,
        callback_query_id: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        text: Optional[str] = None,
        show_alert: Optional[bool] = None,
        url: Optional[str] = None,
        cache_time: Optional[int] = None
    ) -> Literal[True]:
        return self._send_request(
            method="answerCallbackQuery",
            parameters={
                "callback_query_id": callback_query_id,
                "text": text,
                "show_alert": show_alert,
                "url": url,
                "cache_time": cache_time
            },
            timeout_secs=timeout_secs
        )

    def get_user_chat_boosts(
        self,
        chat_id: int,
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> UserChatBoosts:
        return self._converter.get_object(
            data=self._send_request(
                method="getUserChatBoosts",
                parameters={
                    "chat_id": chat_id,
                    "user_id": user_id
                },
                timeout_secs=timeout_secs
            ),
            class_=UserChatBoosts
        )

    def set_my_commands(
        self,
        commands: list[BotCommand],
        *,
        timeout_secs: Union[int, float, None] = None,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setMyCommands",
            parameters={
                "commands": commands,
                "scope": scope,
                "language_code": language_code
            },
            timeout_secs=timeout_secs
        )

    def delete_my_commands(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteMyCommands",
            parameters={
                "scope": scope,
                "language_code": language_code
            },
            timeout_secs=timeout_secs
        )

    def get_my_commands(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None
    ) -> list[BotCommand]:
        return [
            self._converter.get_object(data=i, class_=BotCommand)
            for i in self._send_request(
                method="getMyCommands",
                parameters={
                    "scope": scope,
                    "language_code": language_code
                },
                timeout_secs=timeout_secs
            )
        ]

    def set_my_name(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        name: Optional[str] = None,
        language_code: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setMyName",
            parameters={
                "name": name,
                "language_code": language_code
            },
            timeout_secs=timeout_secs
        )

    def get_my_name(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        language_code: Optional[str] = None
    ) -> BotName:
        return self._converter.get_object(
            data=self._send_request(
                method="getMyName",
                parameters={
                    "language_code": language_code
                },
                timeout_secs=timeout_secs
            ),
            class_=BotName
        )

    def set_my_description(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        description: Optional[str] = None,
        language_code: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setMyDescription",
            parameters={
                "description": description,
                "language_code": language_code
            },
            timeout_secs=timeout_secs
        )

    def get_my_description(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        language_code: Optional[str] = None
    ) -> BotDescription:
        return self._converter.get_object(
            data=self._send_request(
                method="getMyDescription",
                parameters={
                    "language_code": language_code
                },
                timeout_secs=timeout_secs
            ),
            class_=BotDescription
        )

    def set_my_short_description(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        short_description: Optional[str] = None,
        language_code: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setMyShortDescription",
            parameters={
                "short_description": short_description,
                "language_code": language_code
            },
            timeout_secs=timeout_secs
        )

    def get_my_short_description(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        language_code: Optional[str] = None
    ) -> BotShortDescription:
        return self._converter.get_object(
            data=self._send_request(
                method="getMyShortDescription",
                parameters={
                    "language_code": language_code
                },
                timeout_secs=timeout_secs
            ),
            class_=BotShortDescription
        )

    def set_chat_menu_button(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        chat_id: Optional[int] = None,
        menu_button: Optional[MenuButton] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatMenuButton",
            parameters={
                "chat_id": chat_id,
                "menu_button": menu_button
            },
            timeout_secs=timeout_secs
        )

    def get_chat_menu_button(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        chat_id: Optional[int] = None
    ) -> MenuButton:
        return self._converter.get_object(
            data=self._send_request(
                method="getChatMenuButton",
                parameters={
                    "chat_id": chat_id
                },
                timeout_secs=timeout_secs
            ),
            class_=MenuButton
        )

    def set_my_default_administrator_rights(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        rights: Optional[ChatAdministratorRights] = None,
        for_channels: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setMyDefaultAdministratorRights",
            parameters={
                "rights": rights,
                "for_channels": for_channels
            },
            timeout_secs=timeout_secs
        )

    def get_my_default_administrator_rights(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        for_channels: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="getMyDefaultAdministratorRights",
            parameters={
                "for_channels": for_channels
            },
            timeout_secs=timeout_secs
        )

    def get_star_transactions(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> StarTransactions:
        return self._converter.get_object(
            data=self._send_request(
                method="getStarTransactions",
                parameters={
                    "offset": offset,
                    "limit": limit
                },
                timeout_secs=timeout_secs
            ),
            class_=StarTransactions
        )

    def edit_message_text(
        self,
        text: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        entities: Optional[list[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="editMessageText",
            parameters={
                "text": text,
                "business_connection_id": business_connection_id,
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "parse_mode": self._get_parse_mode(parse_mode, with_entities=bool(entities)),
                "entities": entities,
                "link_preview_options": link_preview_options,
                "reply_markup": reply_markup
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._converter.get_object(
            data=data,
            class_=Message
        )

    def edit_message_caption(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="editMessageCaption",
            parameters={
                "business_connection_id": business_connection_id,
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "caption": caption,
                "parse_mode": self._get_parse_mode(
                    parse_mode,
                    with_entities=bool(caption_entities)
                ),
                "caption_entities": caption_entities,
                "show_caption_above_media": show_caption_above_media,
                "reply_markup": reply_markup
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._converter.get_object(
            data=data,
            class_=Message
        )

    def edit_message_media(
        self,
        media: InputMedia,
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        media_class = type(media)
        media_data = self._converter.get_data(media)
        media_data["parse_mode"] = self._get_parse_mode(
            parse_mode=media_data.get("parse_mode", NOT_SET),
            with_entities=bool(
                media_data.get("caption_entities")
            )
        )
        media = self._converter.get_object(
            data=media_data,
            class_=media_class
        )
        data = self._send_request(
            method="editMessageMedia",
            parameters={
                "media": media,
                "business_connection_id": business_connection_id,
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "reply_markup": reply_markup
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._converter.get_object(
            data=data,
            class_=Message
        )

    def edit_message_reply_markup(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="editMessageReplyMarkup",
            parameters={
                "business_connection_id": business_connection_id,
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "reply_markup": reply_markup
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._converter.get_object(
            data=data,
            class_=Message
        )

    def stop_poll(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Poll:
        return self._converter.get_object(
            data=self._send_request(
                method="stopPoll",
                parameters={
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "business_connection_id": business_connection_id,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Poll
        )

    def send_paid_media(
        self,
        chat_id: Union[int, str],
        star_count: int,
        media: list[InputPaidMedia],
        *,
        timeout_secs: Union[int, float, None] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[list[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._converter.get_object(
            data=self._send_request(
                method="sendPaidMedia",
                parameters={
                    "chat_id": chat_id,
                    "star_count": star_count,
                    "media": media,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode=parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "show_caption_above_media": show_caption_above_media,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def delete_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteMessage",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id
            },
            timeout_secs=timeout_secs
        )

    def delete_messages(
        self,
        chat_id: Union[int, str],
        message_ids: list[int],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteMessages",
            parameters={
                "chat_id": chat_id,
                "message_ids": message_ids
            },
            timeout_secs=timeout_secs
        )

    def send_sticker(
        self,
        chat_id: Union[int, str],
        sticker: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        emoji: Optional[str] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        message = self._converter.get_object(
            data=self._send_request(
                method="sendSticker",
                parameters={
                    "chat_id": chat_id,
                    "sticker": self._get_file(sticker),
                    "emoji": emoji,
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

        if self._use_cache:
            self._set_cached_file_id(
                file=sticker,
                file_id=message.sticker.file_id
            )

        return message

    def get_sticker_set(
        self,
        name: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> StickerSet:
        return self._converter.get_object(
            data=self._send_request(
                method="getStickerSet",
                parameters={
                    "name": name
                },
                timeout_secs=timeout_secs
            ),
            class_=StickerSet
        )

    def get_custom_emoji_stickers(
        self,
        custom_emoji_ids: list[str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> list[Sticker]:
        return [
            self._converter.get_object(data=i, class_=Sticker)
            for i in self._send_request(
                method="getCustomEmojiStickers",
                parameters={
                    "custom_emoji_ids": custom_emoji_ids
                },
                timeout_secs=timeout_secs
            )
        ]

    def upload_sticker_file(
        self,
        user_id: int,
        sticker: InputFile,
        sticker_format: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> File:
        return self._converter.get_object(
            data=self._send_request(
                method="uploadStickerFile",
                parameters={
                    "user_id": user_id,
                    "sticker": sticker,
                    "sticker_format": sticker_format
                },
                timeout_secs=timeout_secs
            ),
            class_=File
        )

    def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        stickers: list[InputSticker],
        *,
        timeout_secs: Union[int, float, None] = None,
        sticker_type: Optional[str] = None,
        needs_repainting: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="createNewStickerSet",
            parameters={
                "user_id": user_id,
                "name": name,
                "title": title,
                "stickers": stickers,
                "sticker_type": sticker_type,
                "needs_repainting": needs_repainting
            },
            timeout_secs=timeout_secs
        )

    def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        sticker: InputSticker,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="addStickerToSet",
            parameters={
                "user_id": user_id,
                "name": name,
                "sticker": sticker
            },
            timeout_secs=timeout_secs
        )

    def set_sticker_position_in_set(
        self,
        sticker: str,
        position: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerPositionInSet",
            parameters={
                "sticker": sticker,
                "position": position
            },
            timeout_secs=timeout_secs
        )

    def delete_sticker_from_set(
        self,
        sticker: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteStickerFromSet",
            parameters={
                "sticker": sticker
            },
            timeout_secs=timeout_secs
        )

    def set_sticker_emoji_list(
        self,
        sticker: str,
        emoji_list: list[str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerEmojiList",
            parameters={
                "sticker": sticker,
                "emoji_list": emoji_list
            },
            timeout_secs=timeout_secs
        )

    def set_sticker_keywords(
        self,
        sticker: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        keywords: Optional[list[str]] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerKeywords",
            parameters={
                "sticker": sticker,
                "keywords": keywords
            },
            timeout_secs=timeout_secs
        )

    def set_sticker_mask_position(
        self,
        sticker: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        mask_position: Optional[MaskPosition] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerMaskPosition",
            parameters={
                "sticker": sticker,
                "mask_position": mask_position
            },
            timeout_secs=timeout_secs
        )

    def set_sticker_set_title(
        self,
        name: str,
        title: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerSetTitle",
            parameters={
                "name": name,
                "title": title
            },
            timeout_secs=timeout_secs
        )

    def set_custom_emoji_sticker_set_thumbnail(
        self,
        name: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        custom_emoji_id: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setCustomEmojiStickerSetThumbnail",
            parameters={
                "name": name,
                "custom_emoji_id": custom_emoji_id
            },
            timeout_secs=timeout_secs
        )

    def delete_sticker_set(
        self,
        name: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteStickerSet",
            parameters={
                "name": name
            },
            timeout_secs=timeout_secs
        )

    def set_sticker_set_thumbnail(
        self,
        name: str,
        user_id: int,
        format_: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        thumbnail: Union[InputFile, str, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerSetthumbnail",
            parameters={
                "name": name,
                "user_id": user_id,
                "format": format_,
                "thumbnail": thumbnail
            },
            timeout_secs=timeout_secs
        )

    def replace_sticker_in_set(
        self,
        user_id: int,
        name: str,
        old_sticker: str,
        sticker: InputSticker,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> True:
        return self._send_request(
            method="replaceStickerInSet",
            parameters={
                "user_id": user_id,
                "name": name,
                "old_sticker": old_sticker,
                "sticker": sticker
            },
            timeout_secs=timeout_secs
        )

    def answer_inline_query(
        self,
        inline_query_id: str,
        results: list[InlineQueryResult],
        *,
        timeout_secs: Union[int, float, None] = None,
        cache_time: Optional[int] = None,
        is_personal: Optional[bool] = None,
        next_offset: Optional[str] = None,
        button: Optional[InlineQueryResultsButton] = None
    ) -> Literal[True]:
        return self._send_request(
            method="answerInlineQuery",
            parameters={
                "inline_query_id": inline_query_id,
                "results": [
                    self._get_prepared_inline_query_result(i)
                    for i in results
                ],
                "cache_time": cache_time,
                "is_personal": is_personal,
                "next_offset": next_offset,
                "button": button
            },
            timeout_secs=timeout_secs
        )

    def answer_web_app_query(
        self,
        web_app_query_id: str,
        result: InlineQueryResult,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> SentWebAppMessage:
        return self._converter.get_object(
            data=self._send_request(
                method="answerWebAppQuery",
                parameters={
                    "web_app_query_id": web_app_query_id,
                    "result": self._get_prepared_inline_query_result(result)
                },
                timeout_secs=timeout_secs
            ),
            class_=SentWebAppMessage
        )

    def send_invoice(
        self,
        chat_id: Union[int, str],
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: list[LabeledPrice],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        provider_token: Optional[str] = None,
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
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._converter.get_object(
            data=self._send_request(
                method="sendInvoice",
                parameters={
                    "chat_id": chat_id,
                    "title": title,
                    "description": description,
                    "payload": payload,
                    "currency": currency,
                    "prices": prices,
                    "message_thread_id": message_thread_id,
                    "provider_token": provider_token,
                    "max_tip_amount": max_tip_amount,
                    "suggested_tip_amounts": suggested_tip_amounts,
                    "start_parameter": start_parameter,
                    "provider_data": provider_data,
                    "photo_url": photo_url,
                    "photo_size": photo_size,
                    "photo_width": photo_width,
                    "photo_height": photo_height,
                    "need_name": need_name,
                    "need_phone_number": need_phone_number,
                    "need_email": need_email,
                    "need_shipping_address": need_shipping_address,
                    "send_phone_number_to_provider": send_phone_number_to_provider,
                    "send_email_to_provider": send_email_to_provider,
                    "is_flexible": is_flexible,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def create_invoice_link(
        self,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: list[LabeledPrice],
        *,
        timeout_secs: Union[int, float, None] = None,
        provider_token: Optional[str] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[list[int]] = None,
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
        is_flexible: Optional[bool] = None
    ) -> str:
        return self._send_request(
            method="createInvoiceLink",
            parameters={
                "title": title,
                "description": description,
                "payload": payload,
                "currency": currency,
                "prices": prices,
                "provider_token": provider_token,
                "max_tip_amount": max_tip_amount,
                "suggested_tip_amounts": suggested_tip_amounts,
                "provider_data": provider_data,
                "photo_url": photo_url,
                "photo_size": photo_size,
                "photo_width": photo_width,
                "photo_height": photo_height,
                "need_name": need_name,
                "need_phone_number": need_phone_number,
                "need_email": need_email,
                "need_shipping_address": need_shipping_address,
                "send_phone_number_to_provider": send_phone_number_to_provider,
                "send_email_to_provider": send_email_to_provider,
                "is_flexible": is_flexible
            },
            timeout_secs=timeout_secs
        )

    def refund_star_payment(
        self,
        user_id: int,
        telegram_payment_charge_id: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> True:
        return self._send_request(
            method="refundStarPayment",
            parameters={
                "user_id": user_id,
                "telegram_payment_charge_id": telegram_payment_charge_id
            },
            timeout_secs=timeout_secs
        )

    def answer_shipping_query(
        self,
        shipping_query_id: str,
        ok: bool,
        *,
        timeout_secs: Union[int, float, None] = None,
        shipping_options: Optional[list[ShippingOption]] = None,
        error_message: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="answerShippingQuery",
            parameters={
                "shipping_query_id": shipping_query_id,
                "ok": ok,
                "shipping_options": shipping_options,
                "error_message": error_message
            },
            timeout_secs=timeout_secs
        )

    def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: str,
        ok: bool,
        *,
        timeout_secs: Union[int, float, None] = None,
        error_message: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="answerPreCheckoutQuery",
            parameters={
                "pre_checkout_query_id": pre_checkout_query_id,
                "ok": ok,
                "error_message": error_message
            },
            timeout_secs=timeout_secs
        )

    def set_passport_data_errors(
        self,
        user_id: int,
        errors: list[PassportElementError],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setPassportDataErrors",
            parameters={
                "user_id": user_id,
                "errors": errors
            },
            timeout_secs=timeout_secs
        )

    def send_game(
        self,
        chat_id: int,
        game_short_name: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._converter.get_object(
            data=self._send_request(
                method="sendGame",
                parameters={
                    "chat_id": chat_id,
                    "game_short_name": game_short_name,
                    "business_connection_id": business_connection_id,
                    "message_thread_id": message_thread_id,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "message_effect_id": message_effect_id,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def set_game_score(
        self,
        user_id: int,
        score: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        force: Optional[bool] = None,
        disable_edit_message: Optional[bool] = None,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="setGameScore",
            parameters={
                "user_id": user_id,
                "score": score,
                "force": force,
                "disable_edit_message": disable_edit_message,
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._converter.get_object(
            data=data,
            class_=Message
        )

    def get_game_high_scores(
        self,
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None
    ) -> list[GameHighScore]:
        return [
            self._converter.get_object(data=i, class_=GameHighScore)
            for i in self._send_request(
                method="getGameHighScores",
                parameters={
                    "user_id": user_id,
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "inline_message_id": inline_message_id
                },
                timeout_secs=timeout_secs
            )
        ]

    def get_business_connection(
        self,
        business_connection_id: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> BusinessConnection:
        return self._converter.get_object(
            data=self._send_request(
                method="getBusinessConnection",
                parameters={
                    "business_connection_id": business_connection_id
                },
                timeout_secs=timeout_secs
            ),
            class_=BusinessConnection
        )

    def download_file(
        self,
        path: str,
        file: BinaryIO,
        *,
        timeout_secs: Union[int, float, None] = None,
        chunk_size: int = 64 * 1024
    ) -> None:
        if self.api_url == API_URL:
            with self.session.get(
                url=f"{API_URL}/file/bot{self.token}/{path}",
                stream=True,
                timeout=timeout_secs or self._timeout_secs
            ) as response:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    file.write(chunk)
        else:
            with open(path, "rb") as local_file:
                while True:
                    chunk = local_file.read(chunk_size)

                    if not chunk:
                        break

                    file.write(chunk)

    def _set_cached_file_id(self, file: Union[InputFile, str], file_id: str) -> None:
        if (
            isinstance(file, InputFile)
            and (file.type is InputFileType.PATH)
            and ((file.file, file.name) not in self._cached_file_ids)
        ):
            self._cached_file_ids[(file.file, file.name)] = file_id

    def _send_request(
        self,
        method: str,
        *,
        parameters: Optional[dict[str, Any]] = None,
        timeout_secs: Union[int, float, None] = None
    ) -> Any:
        parameters = {
            name: value
            for name, value in (parameters or {}).items()
            if value is not None
        }

        if parameters:
            data, opened_files = self._prepare_multipart_encoder(parameters)
            headers = {
                "Content-Type": data.content_type
            }
        else:
            data = headers = None
            opened_files = []

        url = self._get_api_url(method)
        timeout_secs = timeout_secs or self._timeout_secs
        retries = 0

        try:
            while True:
                try:
                    return self._process_response(
                        response=self.session.post(
                            url,
                            data=data,  # NOQA
                            headers=headers,
                            timeout=timeout_secs
                        ),
                        method=method,
                        parameters=parameters
                    )
                except (RequestException, InternalServerError):
                    if retries == self._retries:
                        raise

                    retries += 1
                    time.sleep(self._retry_delay_secs)
                except RetryAfterError as error:
                    if not self._wait_on_rate_limit:
                        raise

                    retries = 0
                    time.sleep(error.retry_after)
        finally:
            for i in opened_files:
                i.close()

    def _get_api_url(self, method: str) -> str:
        return f"{self.api_url}/bot{self.token}/{method}"

    def _get_parse_mode(
        self,
        parse_mode: Union[str, None, NotSet],
        *,
        with_entities: bool
    ) -> Optional[str]:
        if parse_mode is not NOT_SET:
            return parse_mode
        elif self._parse_mode is not NOT_SET and not with_entities:
            return self._parse_mode

    def _get_file(
        self,
        file: Union[InputFile, str]
    ) -> Union[InputFile, str]:
        if (
            self._use_cache
            and isinstance(file, InputFile)
            and (file.type is InputFileType.PATH)
        ):
            return self._cached_file_ids.get((file.file, file.name), file)

        return file

    def _prepare_multipart_encoder(
        self,
        parameters: dict[str, Any]
    ) -> tuple[MultipartEncoder, list[IO]]:
        fields: dict[str, Any] = {}
        opened_files: list[IO] = []

        for name, value in parameters.items():
            value = self._prepare_parameter_value(
                value,
                multipart_fields=fields,
                opened_files=opened_files,
                attach_files=False
            )

            if isinstance(value, (dict, list)):
                value = get_serialized_data(value)
            elif not isinstance(value, (str, tuple)):
                value = str(value)

            fields[name] = value

        return MultipartEncoder(fields), opened_files

    def _prepare_parameter_value(
        self,
        value: Any,
        multipart_fields: dict[str, Any],
        opened_files: list[IO],
        attach_files: bool = True
    ) -> Any:
        if isinstance(value, InputFile):
            if value.type is InputFileType.FILE:
                file = value.file
            elif value.type is InputFileType.PATH:
                file = value.file.open("rb")
                opened_files.append(file)
            else:
                raise ValueError("Incorrect file!")

            if attach_files:
                while True:
                    name = secrets.token_urlsafe(8)

                    if name not in multipart_fields:
                        break

                multipart_fields[name] = (value.name, file)

                return f"attach://{name}"

            return value.name, file
        elif is_dataclass(value):
            return {
                name: self._prepare_parameter_value(
                    value_,
                    multipart_fields=multipart_fields,
                    opened_files=opened_files
                )
                for name, value_ in self._converter.get_data(value).items()
                if value_ is not None
            }
        elif isinstance(value, datetime):
            return get_timestamp(value)
        elif isinstance(value, list):
            return [
                self._prepare_parameter_value(
                    i,
                    multipart_fields=multipart_fields,
                    opened_files=opened_files
                )
                for i in value
            ]

        return value

    def _process_response(
        self,
        response: Response,
        method: str,
        parameters: dict[str, Any]
    ) -> Any:
        data = response.json()

        if not data["ok"] or (response.status_code != HTTPStatus.OK):
            try:
                response_parameter_data = data["parameters"]
            except KeyError:
                response_parameters = None
            else:
                response_parameters = self._converter.get_object(
                    data=response_parameter_data,
                    class_=ResponseParameters
                )

            raise get_request_error(
                method=method,
                parameters=parameters,
                status_code=response.status_code,
                description=data["description"],
                response_parameters=response_parameters
            )

        return data["result"]

    def _get_prepared_inline_query_result(
        self,
        result: InlineQueryResult
    ) -> InlineQueryResult:
        if isinstance(
            result,
            (
                InlineQueryResultArticle,
                InlineQueryResultPhoto,
                InlineQueryResultGif,
                InlineQueryResultMpeg4Gif,
                InlineQueryResultVideo,
                InlineQueryResultAudio,
                InlineQueryResultVoice,
                InlineQueryResultDocument,
                InlineQueryResultLocation,
                InlineQueryResultVenue,
                InlineQueryResultContact,
                InlineQueryResultCachedPhoto,
                InlineQueryResultCachedGif,
                InlineQueryResultCachedMpeg4Gif,
                InlineQueryResultCachedSticker,
                InlineQueryResultCachedDocument,
                InlineQueryResultCachedVideo,
                InlineQueryResultCachedVoice,
                InlineQueryResultCachedAudio
            )
        ):
            class_ = type(result)
            data = self._converter.get_data(result)

            if (
                (data.get("input_message_content") is not None)
                and isinstance(result.input_message_content, InputTextMessageContent)
            ):
                data["input_message_content"]["parse_mode"] = self._get_parse_mode(
                    parse_mode=data["input_message_content"].get("parse_mode", NOT_SET),
                    with_entities=bool(
                        data["input_message_content"].get("entities")
                    )
                )

            if isinstance(
                result,
                (
                    InlineQueryResultPhoto,
                    InlineQueryResultGif,
                    InlineQueryResultMpeg4Gif,
                    InlineQueryResultVideo,
                    InlineQueryResultAudio,
                    InlineQueryResultVoice,
                    InlineQueryResultDocument,
                    InlineQueryResultCachedPhoto,
                    InlineQueryResultCachedGif,
                    InlineQueryResultCachedMpeg4Gif,
                    InlineQueryResultCachedDocument,
                    InlineQueryResultCachedVideo,
                    InlineQueryResultCachedVoice,
                    InlineQueryResultCachedAudio
                )
            ):
                data["parse_mode"] = self._get_parse_mode(
                    parse_mode=data.get("parse_mode", NOT_SET),
                    with_entities=bool(
                        data.get("caption_entities")
                    )
                )

            return self._converter.get_object(data=data, class_=class_)

        return result


class BotContext:

    def __init__(
        self,
        token: str,
        *,
        get_me: bool = True,
        api_url: str = API_URL,
        parse_mode: Union[str, NotSet] = NOT_SET,
        timeout_secs: Union[int, float, None] = 300,
        retries: int = 0,
        retry_delay_secs: Union[int, float] = 0,
        wait_on_rate_limit: bool = False,
        use_cache: bool = True
    ):
        self._token = token
        self._get_me = get_me
        self._api_url = api_url
        self._parse_mode = parse_mode
        self._timeout_secs = timeout_secs
        self._retries = retries
        self._retry_delay_secs = retry_delay_secs
        self._wait_on_rate_limit = wait_on_rate_limit
        self._use_cache = use_cache
        self._session: Optional[Session] = None

    def __enter__(self) -> Bot:
        self._session = Session()
        bot = Bot(
            self._session,
            token=self._token,
            api_url=self._api_url,
            parse_mode=self._parse_mode,
            timeout_secs=self._timeout_secs,
            retries=self._retries,
            retry_delay_secs=self._retry_delay_secs,
            wait_on_rate_limit=self._wait_on_rate_limit,
            use_cache=self._use_cache
        )

        if self._get_me:
            bot.get_me()

        return bot

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()


def get_bot(
    token: str,
    *,
    get_me: bool = True,
    api_url: str = API_URL,
    parse_mode: Union[str, NotSet] = NOT_SET,
    timeout_secs: Union[int, float, None] = 300,
    retries: int = 0,
    retry_delay_secs: Union[int, float] = 0,
    wait_on_rate_limit: bool = False,
    use_cache: bool = True
) -> BotContext:
    return BotContext(
        token,
        get_me=get_me,
        api_url=api_url,
        parse_mode=parse_mode,
        timeout_secs=timeout_secs,
        retries=retries,
        retry_delay_secs=retry_delay_secs,
        wait_on_rate_limit=wait_on_rate_limit,
        use_cache=use_cache
    )
