from typing import Union, Optional, Any, Literal
from datetime import datetime
from dataclasses import is_dataclass
import secrets
from http import HTTPStatus

from requests import Session, Response

from telebox.telegram_bot.serialization import DataclassSerializer, convert_datetime_to_timestamp
from telebox.telegram_bot.errors import get_error
from telebox.telegram_bot.consts import chat_member_statuses
from telebox.telegram_bot.types.types.response_parameters import ResponseParameters
from telebox.telegram_bot.types.types.update import Update
from telebox.telegram_bot.types.types.webhook_info import WebhookInfo
from telebox.telegram_bot.types.types.user import User
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.message_entity import MessageEntity
from telebox.telegram_bot.types.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.telegram_bot.types.types.reply_keyboard_markup import ReplyKeyboardMarkup
from telebox.telegram_bot.types.types.reply_keyboard_remove import ReplyKeyboardRemove
from telebox.telegram_bot.types.types.force_reply import ForceReply
from telebox.telegram_bot.types.types.input_file import InputFile
from telebox.telegram_bot.types.types.message_id import MessageId
from telebox.telegram_bot.types.types.input_media import InputMedia
from telebox.telegram_bot.types.types.input_media_audio import InputMediaAudio
from telebox.telegram_bot.types.types.input_media_document import InputMediaDocument
from telebox.telegram_bot.types.types.input_media_photo import InputMediaPhoto
from telebox.telegram_bot.types.types.input_media_video import InputMediaVideo
from telebox.telegram_bot.types.types.user_profile_photos import UserProfilePhotos
from telebox.telegram_bot.types.types.chat_permissions import ChatPermissions
from telebox.telegram_bot.types.types.file import File
from telebox.telegram_bot.types.types.chat_invite_link import ChatInviteLink
from telebox.telegram_bot.types.types.chat import Chat
from telebox.telegram_bot.types.types.bot_command import BotCommand
from telebox.telegram_bot.types.types.bot_command_scope import BotCommandScope
from telebox.telegram_bot.types.types.menu_button import MenuButton
from telebox.telegram_bot.types.types.chat_administrator_rights import ChatAdministratorRights
from telebox.telegram_bot.types.types.poll import Poll
from telebox.telegram_bot.types.types.sticker import Sticker
from telebox.telegram_bot.types.types.sticker_set import StickerSet
from telebox.telegram_bot.types.types.mask_position import MaskPosition
from telebox.telegram_bot.types.types.inline_query_result import InlineQueryResult
from telebox.telegram_bot.types.types.sent_web_app_message import SentWebAppMessage
from telebox.telegram_bot.types.types.labeled_price import LabeledPrice
from telebox.telegram_bot.types.types.shipping_option import ShippingOption
from telebox.telegram_bot.types.types.passport_element_error import PassportElementError
from telebox.telegram_bot.types.types.game_high_score import GameHighScore
from telebox.telegram_bot.types.types.chat_member import ChatMember
from telebox.telegram_bot.types.types.chat_member_owner import ChatMemberOwner
from telebox.telegram_bot.types.types.chat_member_administrator import ChatMemberAdministrator
from telebox.telegram_bot.types.types.chat_member_member import ChatMemberMember
from telebox.telegram_bot.types.types.chat_member_restricted import ChatMemberRestricted
from telebox.telegram_bot.types.types.chat_member_left import ChatMemberLeft
from telebox.telegram_bot.types.types.chat_member_banned import ChatMemberBanned
from telebox.telegram_bot.request_timeout import RequestTimeout
from telebox.utils import NotSetValue, NOT_SET_VALUE


API_URL = "https://api.telegram.org"
_CHAT_MEMBER_TYPES = {
    chat_member_statuses.CREATOR: ChatMemberOwner,
    chat_member_statuses.ADMINISTRATOR: ChatMemberAdministrator,
    chat_member_statuses.MEMBER: ChatMemberMember,
    chat_member_statuses.RESTRICTED: ChatMemberRestricted,
    chat_member_statuses.LEFT: ChatMemberLeft,
    chat_member_statuses.KICKED: ChatMemberBanned
}


class TelegramBot:

    def __init__(
        self,
        session: Session,
        token: str,
        *,
        api_url: str = API_URL,
        default_parse_mode: Union[str, NotSetValue] = NOT_SET_VALUE,
        default_request_timeout: Optional[RequestTimeout] = None
    ):
        self._session = session
        self._token = token
        self._api_url = api_url
        self._default_parse_mode = default_parse_mode
        self._default_request_timeout = default_request_timeout or RequestTimeout(150, 150)
        self._dataclass_serializer = DataclassSerializer()

    def get_updates(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        timeout: Optional[int] = None,
        allowed_updates: Optional[list[str]] = None
    ) -> list[Update]:
        return [
            self._dataclass_serializer.get_object(data=i, class_=Update)
            for i in self._send_request(
                method="getUpdates",
                parameters={
                    "offset": offset,
                    "limit": limit,
                    "timeout": timeout,
                    "allowed_updates": allowed_updates
                },
                timeout=request_timeout
            )
        ]

    def set_webhook(
        self,
        url: str,
        *,
        request_timeout: Optional[RequestTimeout] = None,
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
            timeout=request_timeout
        )

    def delete_webhook(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        drop_pending_updates: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteWebhook",
            parameters={
                "drop_pending_updates": drop_pending_updates
            },
            timeout=request_timeout
        )

    def get_webhook_info(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> WebhookInfo:
        return self._dataclass_serializer.get_object(
            data=self._send_request(method="getWebhookInfo", timeout=request_timeout),
            class_=WebhookInfo
        )

    def get_me(self, *, request_timeout: Optional[RequestTimeout] = None) -> User:
        return self._dataclass_serializer.get_object(
            data=self._send_request(method="getMe", timeout=request_timeout),
            class_=User
        )

    def log_out(self, *, request_timeout: Optional[RequestTimeout] = None) -> Literal[True]:
        return self._send_request(method="logOut", timeout=request_timeout)

    def close(self, *, request_timeout: Optional[RequestTimeout] = None) -> Literal[True]:
        return self._send_request(method="close", timeout=request_timeout)

    def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        parse_mode: Union[str, None, NotSetValue] = NOT_SET_VALUE,
        entities: Optional[list[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendMessage",
                parameters={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": self._get_parse_mode(parse_mode),
                    "entities": entities,
                    "disable_web_page_preview": disable_web_page_preview,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def forward_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="forwardMessage",
                parameters={
                    "chat_id": chat_id,
                    "from_chat_id": from_chat_id,
                    "message_id": message_id,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def copy_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSetValue] = NOT_SET_VALUE,
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
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="copyMessage",
                parameters={
                    "chat_id": chat_id,
                    "from_chat_id": from_chat_id,
                    "message_id": message_id,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(parse_mode),
                    "caption_entities": caption_entities,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=MessageId
        )

    def send_photo(
        self,
        chat_id: Union[int, str],
        photo: Union[InputFile, str],
        *,
        request_timeout: Optional[RequestTimeout] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSetValue] = NOT_SET_VALUE,
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
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendPhoto",
                parameters={
                    "chat_id": chat_id,
                    "photo": photo,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(parse_mode),
                    "caption_entities": caption_entities,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def send_audio(
        self,
        chat_id: Union[int, str],
        audio: Union[InputFile, str],
        *,
        request_timeout: Optional[RequestTimeout] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSetValue] = NOT_SET_VALUE,
        caption_entities: Optional[list[MessageEntity]] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumb: Union[InputFile, str, None] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendAudio",
                parameters={
                    "chat_id": chat_id,
                    "audio": audio,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(parse_mode),
                    "caption_entities": caption_entities,
                    "duration": duration,
                    "performer": performer,
                    "title": title,
                    "thumb": thumb,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def send_document(
        self,
        chat_id: Union[int, str],
        document: Union[InputFile, str],
        *,
        request_timeout: Optional[RequestTimeout] = None,
        thumb: Union[InputFile, str, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSetValue] = NOT_SET_VALUE,
        caption_entities: Optional[list[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendDocument",
                parameters={
                    "chat_id": chat_id,
                    "document": document,
                    "thumb": thumb,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(parse_mode),
                    "caption_entities": caption_entities,
                    "disable_content_type_detection": disable_content_type_detection,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def send_video(
        self,
        chat_id: Union[int, str],
        video: Union[InputFile, str],
        *,
        request_timeout: Optional[RequestTimeout] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumb: Union[InputFile, str, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSetValue] = NOT_SET_VALUE,
        caption_entities: Optional[list[MessageEntity]] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendVideo",
                parameters={
                    "chat_id": chat_id,
                    "video": video,
                    "duration": duration,
                    "width": width,
                    "height": height,
                    "thumb": thumb,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(parse_mode),
                    "caption_entities": caption_entities,
                    "supports_streaming": supports_streaming,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def send_animation(
        self,
        chat_id: Union[int, str],
        animation: Union[InputFile, str],
        *,
        request_timeout: Optional[RequestTimeout] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumb: Union[InputFile, str, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSetValue] = NOT_SET_VALUE,
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
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendAnimation",
                parameters={
                    "chat_id": chat_id,
                    "animation": animation,
                    "duration": duration,
                    "width": width,
                    "height": height,
                    "thumb": thumb,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(parse_mode),
                    "caption_entities": caption_entities,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def send_voice(
        self,
        chat_id: Union[int, str],
        voice: Union[InputFile, str],
        *,
        request_timeout: Optional[RequestTimeout] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSetValue] = NOT_SET_VALUE,
        caption_entities: Optional[list[MessageEntity]] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendVoice",
                parameters={
                    "chat_id": chat_id,
                    "voice": voice,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(parse_mode),
                    "caption_entities": caption_entities,
                    "duration": duration,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def send_video_note(
        self,
        chat_id: Union[int, str],
        video_note: Union[InputFile, str],
        *,
        request_timeout: Optional[RequestTimeout] = None,
        duration: Optional[int] = None,
        length: Optional[int] = None,
        thumb: Union[InputFile, str, None] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendVideoNote",
                parameters={
                    "chat_id": chat_id,
                    "video_note": video_note,
                    "duration": duration,
                    "length": length,
                    "thumb": thumb,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def send_media_group(
        self,
        chat_id: Union[int, str],
        media: Union[list[InputMediaAudio],
                     list[InputMediaDocument],
                     list[InputMediaPhoto],
                     list[InputMediaVideo]],
        *,
        request_timeout: Optional[RequestTimeout] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None
    ) -> list[Message]:
        return [
            self._dataclass_serializer.get_object(data=i, class_=Message)
            for i in self._send_request(
                method="sendMediaGroup",
                parameters={
                    "chat_id": chat_id,
                    "media": media,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply
                },
                timeout=request_timeout
            )
        ]

    def send_location(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendLocation",
                parameters={
                    "chat_id": chat_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "horizontal_accuracy": horizontal_accuracy,
                    "live_period": live_period,
                    "heading": heading,
                    "proximity_alert_radius": proximity_alert_radius,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def edit_message_live_location(
        self,
        latitude: float,
        longitude: float,
        *,
        request_timeout: Optional[RequestTimeout] = None,
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
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "horizontal_accuracy": horizontal_accuracy,
                "heading": heading,
                "proximity_alert_radius": proximity_alert_radius,
                "reply_markup": reply_markup
            },
            timeout=request_timeout
        )

        return data if data is True else self._dataclass_serializer.get_object(
            data=data,
            class_=Message
        )

    def stop_message_live_location(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="stopMessageLiveLocation",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "reply_markup": reply_markup
            },
            timeout=request_timeout
        )

        return data if data is True else self._dataclass_serializer.get_object(
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
        request_timeout: Optional[RequestTimeout] = None,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendVenue",
                parameters={
                    "chat_id": chat_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "title": title,
                    "address": address,
                    "foursquare_id": foursquare_id,
                    "foursquare_type": foursquare_type,
                    "google_place_id": google_place_id,
                    "google_place_type": google_place_type,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def send_contact(
        self,
        chat_id: Union[int, str],
        phone_number: str,
        first_name: str,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendContact",
                parameters={
                    "chat_id": chat_id,
                    "phone_number": phone_number,
                    "first_name": first_name,
                    "last_name": last_name,
                    "vcard": vcard,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def send_poll(
        self,
        chat_id: Union[int, str],
        question: str,
        options: list[str],
        *,
        request_timeout: Optional[RequestTimeout] = None,
        is_anonymous: Optional[bool] = None,
        type_: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        correct_option_id: Optional[int] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Union[str, None, NotSetValue] = NOT_SET_VALUE,
        explanation_entities: Optional[list[MessageEntity]] = None,
        open_period: Optional[int] = None,
        close_date: Optional[datetime] = None,
        is_closed: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendPoll",
                parameters={
                    "chat_id": chat_id,
                    "question": question,
                    "options": options,
                    "is_anonymous": is_anonymous,
                    "type": type_,
                    "allows_multiple_answers": allows_multiple_answers,
                    "correct_option_id": correct_option_id,
                    "explanation": explanation,
                    "explanation_parse_mode": self._get_parse_mode(explanation_parse_mode),
                    "explanation_entities": explanation_entities,
                    "open_period": open_period,
                    "close_date": close_date,
                    "is_closed": is_closed,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def send_dice(
        self,
        chat_id: Union[int, str],
        *,
        request_timeout: Optional[RequestTimeout] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendDice",
                parameters={
                    "chat_id": chat_id,
                    "emoji": emoji,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def send_chat_action(
        self,
        chat_id: Union[int, str],
        action: str,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="sendChatAction",
            parameters={
                "chat_id": chat_id,
                "action": action
            },
            timeout=request_timeout
        )

    def get_user_profile_photos(
        self,
        user_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> UserProfilePhotos:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="getUserProfilePhotos",
                parameters={
                    "user_id": user_id,
                    "offset": offset,
                    "limit": limit
                },
                timeout=request_timeout
            ),
            class_=UserProfilePhotos
        )

    def get_file(
        self,
        file_id: str,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> File:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="getFile",
                parameters={
                    "file_id": file_id
                },
                timeout=request_timeout
            ),
            class_=File
        )

    def ban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None,
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
            timeout=request_timeout
        )

    def unban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        only_if_banned: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unbanChatMember",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id,
                "only_if_banned": only_if_banned
            },
            timeout=request_timeout
        )

    def restrict_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        permissions: ChatPermissions,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        until_date: Optional[datetime] = None
    ) -> Literal[True]:
        return self._send_request(
            method="restrictChatMember",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id,
                "permissions": permissions,
                "until_date": until_date
            },
            timeout=request_timeout
        )

    def promote_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None,
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
        can_pin_messages: Optional[bool] = None
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
                "can_pin_messages": can_pin_messages
            },
            timeout=request_timeout
        )

    def set_chat_administrator_custom_title(
        self,
        chat_id: Union[int, str],
        user_id: int,
        custom_title: str,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatAdministratorCustomTitle",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id,
                "custom_title": custom_title
            },
            timeout=request_timeout
        )

    def ban_chat_sender_chat(
        self,
        chat_id: Union[int, str],
        sender_chat_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="banChatSenderChat",
            parameters={
                "chat_id": chat_id,
                "sender_chat_id": sender_chat_id
            },
            timeout=request_timeout
        )

    def unban_chat_sender_chat(
        self,
        chat_id: Union[int, str],
        sender_chat_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unbanChatSenderChat",
            parameters={
                "chat_id": chat_id,
                "sender_chat_id": sender_chat_id
            },
            timeout=request_timeout
        )

    def set_chat_permissions(
        self,
        chat_id: Union[int, str],
        permissions: ChatPermissions,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatPermissions",
            parameters={
                "chat_id": chat_id,
                "permissions": permissions
            },
            timeout=request_timeout
        )

    def export_chat_invite_link(
        self,
        chat_id: Union[int, str],
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> str:
        return self._send_request(
            method="exportChatInviteLink",
            parameters={
                "chat_id": chat_id
            },
            timeout=request_timeout
        )

    def create_chat_invite_link(
        self,
        chat_id: Union[int, str],
        *,
        request_timeout: Optional[RequestTimeout] = None,
        name: Optional[str] = None,
        expire_date: Optional[datetime] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None
    ) -> ChatInviteLink:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="createChatInviteLink",
                parameters={
                    "chat_id": chat_id,
                    "name": name,
                    "expire_date": expire_date,
                    "member_limit": member_limit,
                    "creates_join_request": creates_join_request
                },
                timeout=request_timeout
            ),
            class_=ChatInviteLink
        )

    def edit_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        name: Optional[str] = None,
        expire_date: Optional[datetime] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None
    ) -> ChatInviteLink:
        return self._dataclass_serializer.get_object(
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
                timeout=request_timeout
            ),
            class_=ChatInviteLink
        )

    def revoke_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> ChatInviteLink:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="revokeChatInviteLink",
                parameters={
                    "chat_id": chat_id,
                    "invite_link": invite_link
                },
                timeout=request_timeout
            ),
            class_=ChatInviteLink
        )

    def approve_chat_join_request(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="approveChatJoinRequest",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id
            },
            timeout=request_timeout
        )

    def decline_chat_join_request(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="declineChatJoinRequest",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id
            },
            timeout=request_timeout
        )

    def set_chat_photo(
        self,
        chat_id: Union[int, str],
        photo: InputFile,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatPhoto",
            parameters={
                "chat_id": chat_id,
                "photo": photo
            },
            timeout=request_timeout
        )

    def delete_chat_photo(
        self,
        chat_id: Union[int, str],
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteChatPhoto",
            parameters={
                "chat_id": chat_id
            },
            timeout=request_timeout
        )
    
    def set_chat_title(
        self,
        chat_id: Union[int, str],
        title: str,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatTitle",
            parameters={
                "chat_id": chat_id,
                "title": title
            },
            timeout=request_timeout
        )

    def set_chat_description(
        self,
        chat_id: Union[int, str],
        description: str,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatDescription",
            parameters={
                "chat_id": chat_id,
                "description": description
            },
            timeout=request_timeout
        )

    def pin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        disable_notification: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="pinChatMessage",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id,
                "disable_notification": disable_notification
            },
            timeout=request_timeout
        )

    def unpin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unpinChatMessage",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id
            },
            timeout=request_timeout
        )

    def unpin_all_chat_messages(
        self,
        chat_id: Union[int, str],
        *,
        request_timeout: Optional[RequestTimeout] = None,
    ) -> Literal[True]:
        return self._send_request(
            method="unpinAllChatMessages",
            parameters={
                "chat_id": chat_id
            },
            timeout=request_timeout
        )

    def leave_chat(
        self,
        chat_id: Union[int, str],
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="leaveChat",
            parameters={
                "chat_id": chat_id
            },
            timeout=request_timeout
        )

    def get_chat(
        self,
        chat_id: Union[int, str],
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Chat:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="getChat",
                parameters={
                    "chat_id": chat_id
                },
                timeout=request_timeout
            ),
            class_=Chat
        )

    def get_chat_administrators(
        self,
        chat_id: Union[int, str],
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> list[Union[ChatMemberOwner,
                    ChatMemberAdministrator]]:
        return [
            self._dataclass_serializer.get_object(data=i, class_=_CHAT_MEMBER_TYPES[i["status"]])
            for i in self._send_request(
                method="getChatAdministrators",
                parameters={
                    "chat_id": chat_id
                },
                timeout=request_timeout
            )
        ]

    def get_chat_member_count(
        self,
        chat_id: Union[int, str],
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> int:
        return self._send_request(
            method="getChatMemberCount",
            parameters={
                "chat_id": chat_id
            },
            timeout=request_timeout
        )

    def get_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> ChatMember:
        data = self._send_request(
            method="getChatMember",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id
            },
            timeout=request_timeout
        )

        return self._dataclass_serializer.get_object(
            data=data,
            class_=_CHAT_MEMBER_TYPES[data["status"]]
        )

    def set_chat_sticker_set(
        self,
        chat_id: Union[int, str],
        sticker_set_name: str,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatStickerSet",
            parameters={
                "chat_id": chat_id,
                "sticker_set_name": sticker_set_name
            },
            timeout=request_timeout
        )

    def delete_chat_sticker_set(
        self,
        chat_id: Union[int, str],
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteChatStickerSet",
            parameters={
                "chat_id": chat_id
            },
            timeout=request_timeout
        )

    def answer_callback_query(
        self,
        callback_query_id: str,
        *,
        request_timeout: Optional[RequestTimeout] = None,
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
            timeout=request_timeout
        )

    def set_my_commands(
        self,
        commands: list[BotCommand],
        *,
        request_timeout: Optional[RequestTimeout] = None,
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
            timeout=request_timeout
        )

    def delete_my_commands(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteMyCommands",
            parameters={
                "scope": scope,
                "language_code": language_code
            },
            timeout=request_timeout
        )

    def get_my_commands(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None
    ) -> list[BotCommand]:
        return [
            self._dataclass_serializer.get_object(data=i, class_=BotCommand)
            for i in self._send_request(
                method="getMyCommands",
                parameters={
                    "scope": scope,
                    "language_code": language_code
                },
                timeout=request_timeout
            )
        ]

    def set_chat_menu_button(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        chat_id: Optional[int] = None,
        menu_button: Optional[MenuButton] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatMenuButton",
            parameters={
                "chat_id": chat_id,
                "menu_button": menu_button
            },
            timeout=request_timeout
        )

    def get_chat_menu_button(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        chat_id: Optional[int] = None
    ) -> Literal[True]:
        return self._send_request(
            method="getChatMenuButton",
            parameters={
                "chat_id": chat_id
            },
            timeout=request_timeout
        )

    def set_my_default_administrator_rights(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        rights: Optional[ChatAdministratorRights] = None,
        for_channels: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setMyDefaultAdministratorRights",
            parameters={
                "rights": rights,
                "for_channels": for_channels
            },
            timeout=request_timeout
        )

    def get_my_default_administrator_rights(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        for_channels: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="getMyDefaultAdministratorRights",
            parameters={
                "for_channels": for_channels
            },
            timeout=request_timeout
        )

    def edit_message_text(
        self,
        text: str,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        parse_mode: Union[str, None, NotSetValue] = NOT_SET_VALUE,
        entities: Optional[list[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[ReplyKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="editMessageText",
            parameters={
                "text": text,
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "parse_mode": self._get_parse_mode(parse_mode),
                "entities": entities,
                "disable_web_page_preview": disable_web_page_preview,
                "reply_markup": reply_markup
            },
            timeout=request_timeout
        )

        return data if data is True else self._dataclass_serializer.get_object(
            data=data,
            class_=Message
        )

    def edit_message_caption(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSetValue] = NOT_SET_VALUE,
        caption_entities: Optional[list[MessageEntity]] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="editMessageCaption",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "caption": caption,
                "parse_mode": self._get_parse_mode(parse_mode),
                "caption_entities": caption_entities,
                "reply_markup": reply_markup
            },
            timeout=request_timeout
        )

        return data if data is True else self._dataclass_serializer.get_object(
            data=data,
            class_=Message
        )

    def edit_message_media(
        self,
        media: InputMedia,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="editMessageMedia",
            parameters={
                "media": media,
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "reply_markup": reply_markup
            },
            timeout=request_timeout
        )

        return data if data is True else self._dataclass_serializer.get_object(
            data=data,
            class_=Message
        )

    def edit_message_reply_markup(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="editMessageReplyMarkup",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "reply_markup": reply_markup
            },
            timeout=request_timeout
        )

        return data if data is True else self._dataclass_serializer.get_object(
            data=data,
            class_=Message
        )

    def stop_poll(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Poll:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="stopPoll",
                parameters={
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Poll
        )

    def delete_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteMessage",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id
            },
            timeout=request_timeout
        )

    def send_sticker(
        self,
        chat_id: Union[int, str],
        sticker: Union[InputFile, str],
        *,
        request_timeout: Optional[RequestTimeout] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendSticker",
                parameters={
                    "chat_id": chat_id,
                    "sticker": sticker,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def get_sticker_set(
        self,
        name: str,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> StickerSet:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="getStickerSet",
                parameters={
                    "name": name
                },
                timeout=request_timeout
            ),
            class_=StickerSet
        )

    def get_custom_emoji_stickers(
        self,
        custom_emoji_ids: list[str],
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> list[Sticker]:
        return [
            self._dataclass_serializer.get_object(data=i, class_=Sticker)
            for i in self._send_request(
                method="getCustomEmojiStickers",
                parameters={
                    "custom_emoji_ids": custom_emoji_ids
                },
                timeout=request_timeout
            )
        ]

    def upload_sticker_file(
        self,
        user_id: int,
        png_sticker: InputFile,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> File:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="uploadStickerFile",
                parameters={
                    "user_id": user_id,
                    "png_sticker": png_sticker
                },
                timeout=request_timeout
            ),
            class_=File
        )

    def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        emojis: str,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        png_sticker: Union[InputFile, str, None] = None,
        tgs_sticker: Optional[InputFile] = None,
        webm_sticker: Optional[InputFile] = None,
        contains_masks: Optional[bool] = None,
        mask_position: Optional[MaskPosition] = None
    ) -> Literal[True]:
        return self._send_request(
            method="createNewStickerSet",
            parameters={
                "user_id": user_id,
                "name": name,
                "title": title,
                "emojis": emojis,
                "png_sticker": png_sticker,
                "tgs_sticker": tgs_sticker,
                "webm_sticker": webm_sticker,
                "contains_masks": contains_masks,
                "mask_position": mask_position
            },
            timeout=request_timeout
        )

    def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        emojis: str,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        png_sticker: Union[InputFile, str, None] = None,
        tgs_sticker: Optional[InputFile] = None,
        webm_sticker: Optional[InputFile] = None,
        mask_position: Optional[MaskPosition] = None
    ) -> Literal[True]:
        return self._send_request(
            method="addStickerToSet",
            parameters={
                "user_id": user_id,
                "name": name,
                "emojis": emojis,
                "png_sticker": png_sticker,
                "tgs_sticker": tgs_sticker,
                "webm_sticker": webm_sticker,
                "mask_position": mask_position
            },
            timeout=request_timeout
        )

    def set_sticker_position_in_set(
        self,
        sticker: str,
        position: int,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerPositionInSet",
            parameters={
                "sticker": sticker,
                "position": position
            },
            timeout=request_timeout
        )

    def delete_sticker_from_set(
        self,
        sticker: str,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteStickerFromSet",
            parameters={
                "sticker": sticker
            },
            timeout=request_timeout
        )

    def set_sticker_set_thumb(
        self,
        name: str,
        user_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        thumb: Union[InputFile, str, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerSetThumb",
            parameters={
                "name": name,
                "user_id": user_id,
                "thumb": thumb
            },
            timeout=request_timeout
        )

    def answer_inline_query(
        self,
        inline_query_id: str,
        results: list[InlineQueryResult],
        *,
        request_timeout: Optional[RequestTimeout] = None,
        cache_time: Optional[int] = None,
        is_personal: Optional[bool] = None,
        next_offset: Optional[str] = None,
        switch_pm_text: Optional[str] = None,
        switch_pm_parameter: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="answerInlineQuery",
            parameters={
                "inline_query_id": inline_query_id,
                "results": results,
                "cache_time": cache_time,
                "is_personal": is_personal,
                "next_offset": next_offset,
                "switch_pm_text": switch_pm_text,
                "switch_pm_parameter": switch_pm_parameter
            },
            timeout=request_timeout
        )

    def answer_web_app_query(
        self,
        web_app_query_id: str,
        result: InlineQueryResult,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> SentWebAppMessage:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="answerWebAppQuery",
                parameters={
                    "web_app_query_id": web_app_query_id,
                    "result": result
                },
                timeout=request_timeout
            ),
            class_=SentWebAppMessage
        )

    def send_invoice(
        self,
        chat_id: Union[int, str],
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: list[LabeledPrice],
        *,
        request_timeout: Optional[RequestTimeout] = None,
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
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendInvoice",
                parameters={
                    "chat_id": chat_id,
                    "title": title,
                    "description": description,
                    "payload": payload,
                    "provider_token": provider_token,
                    "currency": currency,
                    "prices": prices,
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
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def create_invoice_link(
        self,
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: list[LabeledPrice],
        *,
        request_timeout: Optional[RequestTimeout] = None,
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
                "provider_token": provider_token,
                "currency": currency,
                "prices": prices,
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
            timeout=request_timeout
        )

    def answer_shipping_query(
        self,
        shipping_query_id: str,
        ok: bool,
        *,
        request_timeout: Optional[RequestTimeout] = None,
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
            timeout=request_timeout
        )

    def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: str,
        ok: bool,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        error_message: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="answerPreCheckoutQuery",
            parameters={
                "pre_checkout_query_id": pre_checkout_query_id,
                "ok": ok,
                "error_message": error_message
            },
            timeout=request_timeout
        )

    def set_passport_data_errors(
        self,
        user_id: int,
        errors: list[PassportElementError],
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setPassportDataErrors",
            parameters={
                "user_id": user_id,
                "errors": errors
            },
            timeout=request_timeout
        )

    def send_game(
        self,
        chat_id: int,
        game_short_name: str,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._dataclass_serializer.get_object(
            data=self._send_request(
                method="sendGame",
                parameters={
                    "chat_id": chat_id,
                    "game_short_name": game_short_name,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_to_message_id": reply_to_message_id,
                    "allow_sending_without_reply": allow_sending_without_reply,
                    "reply_markup": reply_markup
                },
                timeout=request_timeout
            ),
            class_=Message
        )

    def set_game_score(
        self,
        user_id: int,
        score: int,
        *,
        request_timeout: Optional[RequestTimeout] = None,
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
            timeout=request_timeout
        )

        return data if data is True else self._dataclass_serializer.get_object(
            data=data,
            class_=Message
        )

    def get_game_high_scores(
        self,
        user_id: int,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None
    ) -> list[GameHighScore]:
        return [
            self._dataclass_serializer.get_object(data=i, class_=GameHighScore)
            for i in self._send_request(
                method="getGameHighScores",
                parameters={
                    "user_id": user_id,
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "inline_message_id": inline_message_id
                },
                timeout=request_timeout
            )
        ]

    def _send_request(
        self,
        method: str,
        *,
        parameters: Optional[dict[str, Any]] = None,
        timeout: Optional[RequestTimeout] = None
    ) -> Any:
        parameters = parameters or {}
        url = self._get_api_url(method)
        data, files = self._get_prepared_parameters(parameters)
        timeout = timeout or self._default_request_timeout
        response = self._session.post(
            url=url,
            json=data,
            files=files,
            timeout=(timeout.connect_secs, timeout.read_secs)
        )

        return self._process_response(response, method, parameters)

    def _get_api_url(self, method: str) -> str:
        return f"{self._api_url}/bot{self._token}/{method}"

    def _get_parse_mode(self, parse_mode: Union[str, None, NotSetValue]) -> Optional[str]:
        if parse_mode is not NOT_SET_VALUE:
            return parse_mode
        elif self._default_parse_mode is not NOT_SET_VALUE:
            return self._default_parse_mode

    def _get_prepared_parameters(
        self,
        parameters: dict[str, Any]
    ) -> tuple[dict[str, Any], list[tuple[str, tuple[str, bytes]]]]:
        data = {}
        files = []

        for name, value in parameters.items():
            if value is not None:
                if isinstance(value, InputFile):
                    files.append((name, (value.name or secrets.token_urlsafe(16), value.content)))
                else:
                    if isinstance(value, datetime):
                        value = convert_datetime_to_timestamp(value)
                    elif is_dataclass(value):
                        value = self._dataclass_serializer.get_data(value)

                    data[name] = value

        return data, files

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
                response_parameters = self._dataclass_serializer.get_object(
                    data=response_parameter_data,
                    class_=ResponseParameters
                )

            raise get_error(
                method=method,
                parameters=parameters,
                status_code=response.status_code,
                description=data["description"],
                response_parameters=response_parameters
            )

        return data["result"]