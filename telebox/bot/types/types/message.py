from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal, Union, TYPE_CHECKING

from telebox.bot.consts import chat_types
from telebox.bot.utils.deep_links import get_message_public_link, get_message_private_link
from telebox.bot.utils.formatters.formatter import AbstractFormatter
from telebox.bot.utils.formatters.formatters.html import HTMLFormatter
from telebox.bot.utils.formatters.formatters.markdown import MarkdownFormatter
from telebox.bot.utils.ids import get_unprefixed_chat_id
from telebox.bot.enums.message_content_type import MessageContentType
from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.bot.types.types.animation import Animation
from telebox.bot.types.types.audio import Audio
from telebox.bot.types.types.document import Document
from telebox.bot.types.types.photo_size import PhotoSize
from telebox.bot.types.types.sticker import Sticker
from telebox.bot.types.types.video import Video
from telebox.bot.types.types.video_note import VideoNote
from telebox.bot.types.types.voice import Voice
from telebox.bot.types.types.contact import Contact
from telebox.bot.types.types.dice import Dice
from telebox.bot.types.types.game import Game
from telebox.bot.types.types.poll import Poll
from telebox.bot.types.types.venue import Venue
from telebox.bot.types.types.location import Location
from telebox.bot.types.types.invoice import Invoice
from telebox.bot.types.types.successful_payment import SuccessfulPayment
from telebox.bot.types.types.user_shared import UserShared
from telebox.bot.types.types.chat_shared import ChatShared
from telebox.bot.types.types.write_access_allowed import WriteAccessAllowed
from telebox.bot.types.types.passport_data import PassportData
from telebox.bot.types.types.proximity_alert_triggered import ProximityAlertTriggered
from telebox.bot.types.types.forum_topic_created import ForumTopicCreated
from telebox.bot.types.types.forum_topic_edited import ForumTopicEdited
from telebox.bot.types.types.forum_topic_closed import ForumTopicClosed
from telebox.bot.types.types.forum_topic_reopened import ForumTopicReopened
from telebox.bot.types.types.general_forum_topic_hidden import GeneralForumTopicHidden
from telebox.bot.types.types.general_forum_topic_unhidden import GeneralForumTopicUnhidden
from telebox.bot.types.types.video_chat_scheduled import VideoChatScheduled
from telebox.bot.types.types.video_chat_started import VideoChatStarted
from telebox.bot.types.types.video_chat_ended import VideoChatEnded
from telebox.bot.types.types.web_app_data import WebAppData
from telebox.bot.types.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.bot.types.types.message_auto_delete_timer_changed import (
    MessageAutoDeleteTimerChanged
)
from telebox.bot.types.types.video_chat_participants_invited import (
    VideoChatParticipantsInvited
)
from telebox.utils.text import get_text_with_surrogates, get_text_without_surrogates
if TYPE_CHECKING:
    from telebox.bot.types.types.chat import Chat


_html_formatter = HTMLFormatter()
_markdown_formatter = MarkdownFormatter()


@dataclass
class Message(Type):
    message_id: int
    date: datetime
    chat: "Chat"
    message_thread_id: Optional[int] = None
    from_: Optional[User] = None
    sender_chat: Optional["Chat"] = None
    forward_from: Optional[User] = None
    forward_from_chat: Optional["Chat"] = None
    forward_from_message_id: Optional[int] = None
    forward_signature: Optional[str] = None
    forward_sender_name: Optional[str] = None
    forward_date: Optional[datetime] = None
    is_topic_message: Optional[Literal[True]] = None
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
    has_media_spoiler: Optional[Literal[True]] = None
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
    user_shared: Optional[UserShared] = None
    chat_shared: Optional[ChatShared] = None
    connected_website: Optional[str] = None
    write_access_allowed: Optional[WriteAccessAllowed] = None
    passport_data: Optional[PassportData] = None
    proximity_alert_triggered: Optional[ProximityAlertTriggered] = None
    forum_topic_created: Optional[ForumTopicCreated] = None
    forum_topic_edited: Optional[ForumTopicEdited] = None
    forum_topic_closed: Optional[ForumTopicClosed] = None
    forum_topic_reopened: Optional[ForumTopicReopened] = None
    general_forum_topic_hidden: Optional[GeneralForumTopicHidden] = None
    general_forum_topic_unhidden: Optional[GeneralForumTopicUnhidden] = None
    video_chat_scheduled: Optional[VideoChatScheduled] = None
    video_chat_started: Optional[VideoChatStarted] = None
    video_chat_ended: Optional[VideoChatEnded] = None
    video_chat_participants_invited: Optional[VideoChatParticipantsInvited] = None
    web_app_data: Optional[WebAppData] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None

    def __post_init__(self) -> None:
        if self.text is not None:
            self._content = self.text
            self._content_type = MessageContentType.TEXT
        elif self.animation is not None:
            self._content = self.animation
            self._content_type = MessageContentType.ANIMATION
        elif self.audio is not None:
            self._content = self.audio
            self._content_type = MessageContentType.AUDIO
        elif self.document is not None:
            self._content = self.document
            self._content_type = MessageContentType.DOCUMENT
        elif self.photo is not None:
            self._content = self.photo
            self._content_type = MessageContentType.PHOTO
        elif self.sticker is not None:
            self._content = self.sticker
            self._content_type = MessageContentType.STICKER
        elif self.video is not None:
            self._content = self.video
            self._content_type = MessageContentType.VIDEO
        elif self.video_note is not None:
            self._content = self.video_note
            self._content_type = MessageContentType.VIDEO_NOTE
        elif self.voice is not None:
            self._content = self.voice
            self._content_type = MessageContentType.VOICE
        elif self.contact is not None:
            self._content = self.contact
            self._content_type = MessageContentType.CONTACT
        elif self.dice is not None:
            self._content = self.dice
            self._content_type = MessageContentType.DICE
        elif self.game is not None:
            self._content = self.game
            self._content_type = MessageContentType.GAME
        elif self.poll is not None:
            self._content = self.poll
            self._content_type = MessageContentType.POLL
        elif self.venue is not None:
            self._content = self.venue
            self._content_type = MessageContentType.VENUE
        elif self.location is not None:
            self._content = self.location
            self._content_type = MessageContentType.LOCATION
        elif self.new_chat_members is not None:
            self._content = self.new_chat_members
            self._content_type = MessageContentType.NEW_CHAT_MEMBERS
        elif self.left_chat_member is not None:
            self._content = self.left_chat_member
            self._content_type = MessageContentType.LEFT_CHAT_MEMBER
        elif self.new_chat_title is not None:
            self._content = self.new_chat_title
            self._content_type = MessageContentType.NEW_CHAT_TITLE
        elif self.new_chat_photo is not None:
            self._content = self.new_chat_photo
            self._content_type = MessageContentType.NEW_CHAT_PHOTO
        elif self.delete_chat_photo is not None:
            self._content = self.delete_chat_photo
            self._content_type = MessageContentType.DELETE_CHAT_PHOTO
        elif self.group_chat_created is not None:
            self._content = self.group_chat_created
            self._content_type = MessageContentType.GROUP_CHAT_CREATED
        elif self.supergroup_chat_created is not None:
            self._content = self.supergroup_chat_created
            self._content_type = MessageContentType.SUPERGROUP_CHAT_CREATED
        elif self.channel_chat_created is not None:
            self._content = self.channel_chat_created
            self._content_type = MessageContentType.CHANNEL_CHAT_CREATED
        elif self.message_auto_delete_timer_changed is not None:
            self._content = self.message_auto_delete_timer_changed
            self._content_type = MessageContentType.MESSAGE_AUTO_DELETE_TIMER_CHANGED
        elif self.migrate_to_chat_id is not None:
            self._content = self.migrate_to_chat_id
            self._content_type = MessageContentType.MIGRATE_TO_CHAT_ID
        elif self.migrate_from_chat_id is not None:
            self._content = self.migrate_from_chat_id
            self._content_type = MessageContentType.MIGRATE_FROM_CHAT_ID
        elif self.pinned_message is not None:
            self._content = self.pinned_message
            self._content_type = MessageContentType.PINNED_MESSAGE
        elif self.invoice is not None:
            self._content = self.invoice
            self._content_type = MessageContentType.INVOICE
        elif self.successful_payment is not None:
            self._content = self.successful_payment
            self._content_type = MessageContentType.SUCCESSFUL_PAYMENT
        elif self.user_shared is not None:
            self._content = self.user_shared
            self._content_type = MessageContentType.USER_SHARED
        elif self.chat_shared is not None:
            self._content = self.chat_shared
            self._content_type = MessageContentType.CHAT_SHARED
        elif self.connected_website is not None:
            self._content = self.connected_website
            self._content_type = MessageContentType.CONNECTED_WEBSITE
        elif self.write_access_allowed is not None:
            self._content = self.write_access_allowed
            self._content_type = MessageContentType.WRITE_ACCESS_ALLOWED
        elif self.passport_data is not None:
            self._content = self.passport_data
            self._content_type = MessageContentType.PASSPORT_DATA
        elif self.proximity_alert_triggered is not None:
            self._content = self.proximity_alert_triggered
            self._content_type = MessageContentType.PROXIMITY_ALERT_TRIGGERED
        elif self.forum_topic_created is not None:
            self._content = self.forum_topic_created
            self._content_type = MessageContentType.FORUM_TOPIC_CREATED
        elif self.forum_topic_edited is not None:
            self._content = self.forum_topic_edited
            self._content_type = MessageContentType.FORUM_TOPIC_EDITED
        elif self.forum_topic_closed is not None:
            self._content = self.forum_topic_closed
            self._content_type = MessageContentType.FORUM_TOPIC_CLOSED
        elif self.forum_topic_reopened is not None:
            self._content = self.forum_topic_reopened
            self._content_type = MessageContentType.FORUM_TOPIC_REOPENED
        elif self.general_forum_topic_hidden is not None:
            self._content = self.general_forum_topic_hidden
            self._content_type = MessageContentType.GENERAL_FORUM_TOPIC_HIDDEN
        elif self.general_forum_topic_unhidden is not None:
            self._content = self.general_forum_topic_unhidden
            self._content_type = MessageContentType.GENERAL_FORUM_TOPIC_UNHIDDEN
        elif self.video_chat_scheduled is not None:
            self._content = self.video_chat_scheduled
            self._content_type = MessageContentType.VIDEO_CHAT_SCHEDULED
        elif self.video_chat_started is not None:
            self._content = self.video_chat_started
            self._content_type = MessageContentType.VIDEO_CHAT_STARTED
        elif self.video_chat_ended is not None:
            self._content = self.video_chat_ended
            self._content_type = MessageContentType.VIDEO_CHAT_ENDED
        elif self.video_chat_participants_invited is not None:
            self._content = self.video_chat_participants_invited
            self._content_type = MessageContentType.VIDEO_CHAT_PARTICIPANTS_INVITED
        elif self.web_app_data is not None:
            self._content = self.web_app_data
            self._content_type = MessageContentType.WEB_APP_DATA
        else:
            self._content = self._content_type = None

    @property
    def content(self) -> Optional["MessageContent"]:
        return self._content

    @property
    def content_type(self) -> Optional[MessageContentType]:
        return self._content_type

    @property
    def chat_type(self) -> str:
        return self.chat.type

    @property
    def chat_id(self) -> int:
        return self.chat.id

    @property
    def unprefixed_chat_id(self) -> int:
        return get_unprefixed_chat_id(self.chat_id, self.chat_type)

    @property
    def sender_chat_id(self) -> Optional[int]:
        return self.sender_chat.id if self.sender_chat is not None else None

    @property
    def user_id(self) -> Optional[int]:
        return self.from_.id if self.from_ is not None else None

    @property
    def message_topic_id(self) -> Optional[int]:
        if self.is_topic_message:
            return self.message_thread_id

    @property
    def best_photo(self) -> Optional[PhotoSize]:
        if self.photo:
            return self.photo[-1]

    @property
    def is_forwarded(self) -> bool:
        return self.forward_date is not None

    @property
    def is_reply(self) -> bool:
        return self.reply_to_message is not None

    @property
    def link(self) -> Optional[str]:
        if self.chat.type in frozenset((chat_types.CHANNEL, chat_types.SUPERGROUP)):
            if self.chat.username is not None:
                return get_message_public_link(self.chat.username, self.message_id)
            else:
                return get_message_private_link(self.unprefixed_chat_id, self.message_id)

    def get_text(self) -> Optional[str]:
        if self.text is not None:
            return self.text
        elif self.caption is not None:
            return self.caption

    def get_html_text(self) -> Optional[str]:
        return self._get_formatted_text(_html_formatter)

    def get_markdown_text(self) -> Optional[str]:
        return self._get_formatted_text(_markdown_formatter)

    def get_entity_text(self, entity: MessageEntity) -> Optional[str]:
        text = self.get_text()

        if text is not None:
            text = get_text_with_surrogates(text)

            return get_text_without_surrogates(text[entity.offset * 2:entity.end_offset * 2])

    def get_entities(self) -> list[MessageEntity]:
        if self.entities is not None:
            return self.entities
        elif self.caption_entities is not None:
            return self.caption_entities

        return []

    def get_command_args(self) -> list[str]:
        text = self.get_text()
        args = []

        if text is not None:
            for i in text.split(" ")[1:]:
                if i:
                    args.append(i)

        return args

    def _get_formatted_text(self, formatter: AbstractFormatter) -> Optional[str]:
        text = self.get_text()

        if text is None:
            return

        entities = self.get_entities()

        return formatter.get_formatted_text(text, entities)


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
    ForumTopicCreated,
    ForumTopicClosed,
    ForumTopicReopened,
    VideoChatScheduled,
    VideoChatStarted,
    VideoChatEnded,
    VideoChatParticipantsInvited,
    WebAppData
]
