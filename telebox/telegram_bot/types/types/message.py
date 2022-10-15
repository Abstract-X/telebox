from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal, Union, TYPE_CHECKING

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.utils import get_message_public_url, get_message_private_url
from telebox.telegram_bot.consts import chat_types
from telebox.telegram_bot.enums.message_content_type import MessageContentType
from telebox.telegram_bot.errors import UnknownMessageContentError
from telebox.telegram_bot.types.types.user import User
from telebox.telegram_bot.types.types.message_entity import MessageEntity
from telebox.telegram_bot.types.types.animation import Animation
from telebox.telegram_bot.types.types.audio import Audio
from telebox.telegram_bot.types.types.document import Document
from telebox.telegram_bot.types.types.photo_size import PhotoSize
from telebox.telegram_bot.types.types.sticker import Sticker
from telebox.telegram_bot.types.types.video import Video
from telebox.telegram_bot.types.types.video_note import VideoNote
from telebox.telegram_bot.types.types.voice import Voice
from telebox.telegram_bot.types.types.contact import Contact
from telebox.telegram_bot.types.types.dice import Dice
from telebox.telegram_bot.types.types.game import Game
from telebox.telegram_bot.types.types.poll import Poll
from telebox.telegram_bot.types.types.venue import Venue
from telebox.telegram_bot.types.types.location import Location
from telebox.telegram_bot.types.types.invoice import Invoice
from telebox.telegram_bot.types.types.successful_payment import SuccessfulPayment
from telebox.telegram_bot.types.types.passport_data import PassportData
from telebox.telegram_bot.types.types.proximity_alert_triggered import ProximityAlertTriggered
from telebox.telegram_bot.types.types.video_chat_scheduled import VideoChatScheduled
from telebox.telegram_bot.types.types.video_chat_started import VideoChatStarted
from telebox.telegram_bot.types.types.video_chat_ended import VideoChatEnded
from telebox.telegram_bot.types.types.web_app_data import WebAppData
from telebox.telegram_bot.types.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.telegram_bot.types.types.message_auto_delete_timer_changed import (
    MessageAutoDeleteTimerChanged
)
from telebox.telegram_bot.types.types.video_chat_participants_invited import (
    VideoChatParticipantsInvited
)
if TYPE_CHECKING:
    from telebox.telegram_bot.types.types.chat import Chat


@dataclass(unsafe_hash=True)
class Message(Type):
    message_id: int
    date: datetime
    chat: "Chat"
    from_: Optional[User] = None
    sender_chat: Optional["Chat"] = None
    forward_from: Optional[User] = None
    forward_from_chat: Optional["Chat"] = None
    forward_from_message_id: Optional[int] = None
    forward_signature: Optional[str] = None
    forward_sender_name: Optional[str] = None
    forward_date: Optional[datetime] = None
    is_automatic_forward: Optional[Literal[True]] = None
    reply_to_message: Optional["Message"] = None
    via_bot: Optional[User] = None
    edit_date: Optional[datetime] = None
    has_protected_content: Optional[Literal[True]] = None
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
    text: Optional[str] = None
    entities: Optional[list[MessageEntity]] = None
    animation: Optional[Animation] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    photo: Optional[list[PhotoSize]] = None
    sticker: Optional[Sticker] = None
    video: Optional[Video] = None
    video_note: Optional[VideoNote] = None
    voice: Optional[Voice] = None
    caption: Optional[str] = None
    caption_entities: Optional[list[MessageEntity]] = None
    contact: Optional[Contact] = None
    dice: Optional[Dice] = None
    game: Optional[Game] = None
    poll: Optional[Poll] = None
    venue: Optional[Venue] = None
    location: Optional[Location] = None
    new_chat_members: Optional[list[User]] = None
    left_chat_member: Optional[User] = None
    new_chat_title: Optional[str] = None
    new_chat_photo: Optional[list[PhotoSize]] = None
    delete_chat_photo: Optional[Literal[True]] = None
    group_chat_created: Optional[Literal[True]] = None
    supergroup_chat_created: Optional[Literal[True]] = None
    channel_chat_created: Optional[Literal[True]] = None
    message_auto_delete_timer_changed: Optional[MessageAutoDeleteTimerChanged] = None
    migrate_to_chat_id: Optional[int] = None
    migrate_from_chat_id: Optional[int] = None
    pinned_message: Optional["Message"] = None
    invoice: Optional[Invoice] = None
    successful_payment: Optional[SuccessfulPayment] = None
    connected_website: Optional[str] = None
    passport_data: Optional[PassportData] = None
    proximity_alert_triggered: Optional[ProximityAlertTriggered] = None
    video_chat_scheduled: Optional[VideoChatScheduled] = None
    video_chat_started: Optional[VideoChatStarted] = None
    video_chat_ended: Optional[VideoChatEnded] = None
    video_chat_participants_invited: Optional[VideoChatParticipantsInvited] = None
    web_app_data: Optional[WebAppData] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None

    @property
    def content(self) -> tuple["MessageContent", MessageContentType]:
        if self.text is not None:
            return self.text, MessageContentType.TEXT
        elif self.animation is not None:
            return self.animation, MessageContentType.ANIMATION
        elif self.audio is not None:
            return self.audio, MessageContentType.AUDIO
        elif self.document is not None:
            return self.document, MessageContentType.DOCUMENT
        elif self.photo is not None:
            return self.photo, MessageContentType.PHOTO
        elif self.sticker is not None:
            return self.sticker, MessageContentType.STICKER
        elif self.video is not None:
            return self.video, MessageContentType.VIDEO
        elif self.video_note is not None:
            return self.video_note, MessageContentType.VIDEO_NOTE
        elif self.voice is not None:
            return self.voice, MessageContentType.VOICE
        elif self.contact is not None:
            return self.contact, MessageContentType.CONTACT
        elif self.dice is not None:
            return self.dice, MessageContentType.DICE
        elif self.game is not None:
            return self.game, MessageContentType.GAME
        elif self.poll is not None:
            return self.poll, MessageContentType.POLL
        elif self.venue is not None:
            return self.venue, MessageContentType.VENUE
        elif self.location is not None:
            return self.location, MessageContentType.LOCATION
        elif self.new_chat_members is not None:
            return self.new_chat_members, MessageContentType.NEW_CHAT_MEMBERS
        elif self.left_chat_member is not None:
            return self.left_chat_member, MessageContentType.LEFT_CHAT_MEMBER
        elif self.new_chat_title is not None:
            return self.new_chat_title, MessageContentType.NEW_CHAT_TITLE
        elif self.new_chat_photo is not None:
            return self.new_chat_photo, MessageContentType.NEW_CHAT_PHOTO
        elif self.delete_chat_photo is not None:
            return self.delete_chat_photo, MessageContentType.DELETE_CHAT_PHOTO
        elif self.group_chat_created is not None:
            return self.group_chat_created, MessageContentType.GROUP_CHAT_CREATED
        elif self.supergroup_chat_created is not None:
            return self.supergroup_chat_created, MessageContentType.SUPERGROUP_CHAT_CREATED
        elif self.channel_chat_created is not None:
            return self.channel_chat_created, MessageContentType.CHANNEL_CHAT_CREATED
        elif self.message_auto_delete_timer_changed is not None:
            return (
                self.message_auto_delete_timer_changed,
                MessageContentType.MESSAGE_AUTO_DELETE_TIMER_CHANGED
            )
        elif self.migrate_to_chat_id is not None:
            return self.migrate_to_chat_id, MessageContentType.MIGRATE_TO_CHAT_ID
        elif self.migrate_from_chat_id is not None:
            return self.migrate_from_chat_id, MessageContentType.MIGRATE_FROM_CHAT_ID
        elif self.pinned_message is not None:
            return self.pinned_message, MessageContentType.PINNED_MESSAGE
        elif self.invoice is not None:
            return self.invoice, MessageContentType.INVOICE
        elif self.successful_payment is not None:
            return self.successful_payment, MessageContentType.SUCCESSFUL_PAYMENT
        elif self.connected_website is not None:
            return self.connected_website, MessageContentType.CONNECTED_WEBSITE
        elif self.passport_data is not None:
            return self.passport_data, MessageContentType.PASSPORT_DATA
        elif self.proximity_alert_triggered is not None:
            return self.proximity_alert_triggered, MessageContentType.PROXIMITY_ALERT_TRIGGERED
        elif self.video_chat_scheduled is not None:
            return self.video_chat_scheduled, MessageContentType.VIDEO_CHAT_SCHEDULED
        elif self.video_chat_started is not None:
            return self.video_chat_started, MessageContentType.VIDEO_CHAT_STARTED
        elif self.video_chat_ended is not None:
            return self.video_chat_ended, MessageContentType.VIDEO_CHAT_ENDED
        elif self.video_chat_participants_invited is not None:
            return (
                self.video_chat_participants_invited,
                MessageContentType.VIDEO_CHAT_PARTICIPANTS_INVITED
            )
        elif self.web_app_data is not None:
            return self.web_app_data, MessageContentType.WEB_APP_DATA

        raise UnknownMessageContentError("Unknown message type!")

    @property
    def chat_type(self) -> str:
        return self.chat.type

    @property
    def chat_id(self) -> int:
        return self.chat.id

    @property
    def sender_chat_id(self) -> Optional[int]:
        return self.sender_chat.id if self.sender_chat is not None else None

    @property
    def user_id(self) -> Optional[int]:
        return self.from_.id if self.from_ is not None else None

    @property
    def is_forwarded(self) -> bool:
        return self.forward_date is not None

    @property
    def is_reply(self) -> bool:
        return self.reply_to_message is not None

    @property
    def url(self) -> Optional[str]:
        if self.chat.type in {chat_types.CHANNEL, chat_types.SUPERGROUP}:
            if self.chat.username is not None:
                return get_message_public_url(self.chat.username, self.message_id)
            else:
                return get_message_private_url(self.chat.id, self.message_id)


MessageContent = Union[
    str,
    Animation,
    Audio,
    Document,
    list[PhotoSize],
    Sticker,
    Video,
    VideoNote,
    Voice,
    Contact,
    Dice,
    Game,
    Poll,
    Venue,
    Location,
    list[User],
    User,
    Literal[True],
    MessageAutoDeleteTimerChanged,
    int,
    Message,
    Invoice,
    SuccessfulPayment,
    PassportData,
    ProximityAlertTriggered,
    VideoChatScheduled,
    VideoChatStarted,
    VideoChatEnded,
    VideoChatParticipantsInvited,
    WebAppData
]
