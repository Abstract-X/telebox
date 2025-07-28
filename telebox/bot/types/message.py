from datetime import datetime
from typing import Optional, Literal, Any, TYPE_CHECKING

from attrs import define, field

from telebox.bot.consts import chat_types
from telebox.bot.utils.deep_links import get_message_public_link, get_message_private_link
from telebox.bot.utils.formatters.formatter import AbstractFormatter
from telebox.bot.utils.formatters.formatters.html import HTMLFormatter
from telebox.bot.utils.formatters.formatters.markdown import MarkdownFormatter
from telebox.bot.utils.ids import get_unprefixed_chat_id
from telebox.bot.enums.message_content_type import MessageContentType
from telebox.bot.type import Type
from telebox.bot.types.user import User
from telebox.bot.types.message_entity import MessageEntity
from telebox.bot.types.animation import Animation
from telebox.bot.types.audio import Audio
from telebox.bot.types.document import Document
from telebox.bot.types.story import Story
from telebox.bot.types.photo_size import PhotoSize
from telebox.bot.types.sticker import Sticker
from telebox.bot.types.video import Video
from telebox.bot.types.video_note import VideoNote
from telebox.bot.types.voice import Voice
from telebox.bot.types.contact import Contact
from telebox.bot.types.dice import Dice
from telebox.bot.types.game import Game
from telebox.bot.types.poll import Poll
from telebox.bot.types.venue import Venue
from telebox.bot.types.location import Location
from telebox.bot.types.invoice import Invoice
from telebox.bot.types.successful_payment import SuccessfulPayment
from telebox.bot.types.users_shared import UsersShared
from telebox.bot.types.chat_shared import ChatShared
from telebox.bot.types.write_access_allowed import WriteAccessAllowed
from telebox.bot.types.passport_data import PassportData
from telebox.bot.types.proximity_alert_triggered import ProximityAlertTriggered
from telebox.bot.types.chat_boost_added import ChatBoostAdded
from telebox.bot.types.forum_topic_created import ForumTopicCreated
from telebox.bot.types.forum_topic_edited import ForumTopicEdited
from telebox.bot.types.forum_topic_closed import ForumTopicClosed
from telebox.bot.types.forum_topic_reopened import ForumTopicReopened
from telebox.bot.types.general_forum_topic_hidden import GeneralForumTopicHidden
from telebox.bot.types.general_forum_topic_unhidden import GeneralForumTopicUnhidden
from telebox.bot.types.video_chat_scheduled import VideoChatScheduled
from telebox.bot.types.video_chat_started import VideoChatStarted
from telebox.bot.types.video_chat_ended import VideoChatEnded
from telebox.bot.types.web_app_data import WebAppData
from telebox.bot.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.bot.types.message_auto_delete_timer_changed import (
    MessageAutoDeleteTimerChanged
)
from telebox.bot.types.video_chat_participants_invited import (
    VideoChatParticipantsInvited
)
from telebox.bot.types.external_reply_info import ExternalReplyInfo
from telebox.bot.types.text_quote import TextQuote
from telebox.bot.types.link_preview_options import LinkPreviewOptions
from telebox.bot.types.giveaway_created import GiveawayCreated
from telebox.bot.types.giveaway import Giveaway
from telebox.bot.types.giveaway_winners import GiveawayWinners
from telebox.bot.types.message_origin import MessageOrigin
from telebox.bot.types.chat_background import ChatBackground
from telebox.bot.types.chat import Chat
from telebox.bot.types.paid_media_info import PaidMediaInfo
from telebox.bot.types.refunded_payment import RefundedPayment
from telebox.utils.text import get_text_with_surrogates, get_text_without_surrogates
if TYPE_CHECKING:
    from telebox.bot.types.giveaway_completed import GiveawayCompleted
    from telebox.bot.types.maybe_inaccessible_message import MaybeInaccessibleMessage


_html_formatter = HTMLFormatter()
_markdown_formatter = MarkdownFormatter()


@define(repr=False)
class Message(Type):
    message_id: int
    date: datetime
    chat: Chat
    sender_business_bot: Optional[User] = None
    business_connection_id: Optional[str] = None
    forward_origin: Optional[MessageOrigin] = None
    message_thread_id: Optional[int] = None
    from_: Optional[User] = None
    sender_chat: Optional[Chat] = None
    sender_boost_count: Optional[int] = None
    is_topic_message: Optional[Literal[True]] = None
    is_automatic_forward: Optional[Literal[True]] = None
    reply_to_message: Optional["Message"] = None
    external_reply: Optional[ExternalReplyInfo] = None
    quote: Optional[TextQuote] = None
    reply_to_story: Optional[Story] = None
    via_bot: Optional[User] = None
    edit_date: Optional[datetime] = None
    has_protected_content: Optional[Literal[True]] = None
    is_from_offline: Optional[Literal[True]] = None
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
    text: Optional[str] = None
    entities: Optional[list[MessageEntity]] = None
    link_preview_options: Optional[LinkPreviewOptions] = None
    effect_id: Optional[str] = None
    animation: Optional[Animation] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    paid_media: Optional[PaidMediaInfo] = None
    photo: Optional[list[PhotoSize]] = None
    sticker: Optional[Sticker] = None
    story: Optional[Story] = None
    video: Optional[Video] = None
    video_note: Optional[VideoNote] = None
    voice: Optional[Voice] = None
    caption: Optional[str] = None
    caption_entities: Optional[list[MessageEntity]] = None
    show_caption_above_media: Optional[Literal[True]] = None
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
    pinned_message: Optional["MaybeInaccessibleMessage"] = None
    invoice: Optional[Invoice] = None
    successful_payment: Optional[SuccessfulPayment] = None
    refunded_payment: Optional[RefundedPayment] = None
    users_shared: Optional[UsersShared] = None
    chat_shared: Optional[ChatShared] = None
    connected_website: Optional[str] = None
    write_access_allowed: Optional[WriteAccessAllowed] = None
    passport_data: Optional[PassportData] = None
    proximity_alert_triggered: Optional[ProximityAlertTriggered] = None
    boost_added: Optional[ChatBoostAdded] = None
    chat_background_set: Optional[ChatBackground] = None
    forum_topic_created: Optional[ForumTopicCreated] = None
    forum_topic_edited: Optional[ForumTopicEdited] = None
    forum_topic_closed: Optional[ForumTopicClosed] = None
    forum_topic_reopened: Optional[ForumTopicReopened] = None
    general_forum_topic_hidden: Optional[GeneralForumTopicHidden] = None
    general_forum_topic_unhidden: Optional[GeneralForumTopicUnhidden] = None
    giveaway_created: Optional[GiveawayCreated] = None
    giveaway: Optional[Giveaway] = None
    giveaway_winners: Optional[GiveawayWinners] = None
    giveaway_completed: Optional["GiveawayCompleted"] = None
    video_chat_scheduled: Optional[VideoChatScheduled] = None
    video_chat_started: Optional[VideoChatStarted] = None
    video_chat_ended: Optional[VideoChatEnded] = None
    video_chat_participants_invited: Optional[VideoChatParticipantsInvited] = None
    web_app_data: Optional[WebAppData] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    content: Optional[Any] = field(init=False)
    content_type: Optional[MessageContentType] = field(init=False)

    def __attrs_post_init__(self) -> None:
        if self.text is not None:
            self.content = self.text
            self.content_type = MessageContentType.TEXT
        elif self.animation is not None:
            self.content = self.animation
            self.content_type = MessageContentType.ANIMATION
        elif self.audio is not None:
            self.content = self.audio
            self.content_type = MessageContentType.AUDIO
        elif self.document is not None:
            self.content = self.document
            self.content_type = MessageContentType.DOCUMENT
        elif self.paid_media is not None:
            self.content = self.paid_media
            self.content_type = MessageContentType.PAID_MEDIA
        elif self.photo is not None:
            self.content = self.photo
            self.content_type = MessageContentType.PHOTO
        elif self.sticker is not None:
            self.content = self.sticker
            self.content_type = MessageContentType.STICKER
        elif self.story is not None:
            self.content = self.story
            self.content_type = MessageContentType.STORY
        elif self.video is not None:
            self.content = self.video
            self.content_type = MessageContentType.VIDEO
        elif self.video_note is not None:
            self.content = self.video_note
            self.content_type = MessageContentType.VIDEO_NOTE
        elif self.voice is not None:
            self.content = self.voice
            self.content_type = MessageContentType.VOICE
        elif self.contact is not None:
            self.content = self.contact
            self.content_type = MessageContentType.CONTACT
        elif self.dice is not None:
            self.content = self.dice
            self.content_type = MessageContentType.DICE
        elif self.game is not None:
            self.content = self.game
            self.content_type = MessageContentType.GAME
        elif self.poll is not None:
            self.content = self.poll
            self.content_type = MessageContentType.POLL
        elif self.venue is not None:
            self.content = self.venue
            self.content_type = MessageContentType.VENUE
        elif self.location is not None:
            self.content = self.location
            self.content_type = MessageContentType.LOCATION
        elif self.new_chat_members is not None:
            self.content = self.new_chat_members
            self.content_type = MessageContentType.NEW_CHAT_MEMBERS
        elif self.left_chat_member is not None:
            self.content = self.left_chat_member
            self.content_type = MessageContentType.LEFT_CHAT_MEMBER
        elif self.new_chat_title is not None:
            self.content = self.new_chat_title
            self.content_type = MessageContentType.NEW_CHAT_TITLE
        elif self.new_chat_photo is not None:
            self.content = self.new_chat_photo
            self.content_type = MessageContentType.NEW_CHAT_PHOTO
        elif self.delete_chat_photo is not None:
            self.content = self.delete_chat_photo
            self.content_type = MessageContentType.DELETE_CHAT_PHOTO
        elif self.group_chat_created is not None:
            self.content = self.group_chat_created
            self.content_type = MessageContentType.GROUP_CHAT_CREATED
        elif self.supergroup_chat_created is not None:
            self.content = self.supergroup_chat_created
            self.content_type = MessageContentType.SUPERGROUP_CHAT_CREATED
        elif self.channel_chat_created is not None:
            self.content = self.channel_chat_created
            self.content_type = MessageContentType.CHANNEL_CHAT_CREATED
        elif self.message_auto_delete_timer_changed is not None:
            self.content = self.message_auto_delete_timer_changed
            self.content_type = MessageContentType.MESSAGE_AUTO_DELETE_TIMER_CHANGED
        elif self.migrate_to_chat_id is not None:
            self.content = self.migrate_to_chat_id
            self.content_type = MessageContentType.MIGRATE_TO_CHAT_ID
        elif self.migrate_from_chat_id is not None:
            self.content = self.migrate_from_chat_id
            self.content_type = MessageContentType.MIGRATE_FROM_CHAT_ID
        elif self.pinned_message is not None:
            self.content = self.pinned_message
            self.content_type = MessageContentType.PINNED_MESSAGE
        elif self.invoice is not None:
            self.content = self.invoice
            self.content_type = MessageContentType.INVOICE
        elif self.successful_payment is not None:
            self.content = self.successful_payment
            self.content_type = MessageContentType.SUCCESSFUL_PAYMENT
        elif self.refunded_payment is not None:
            self.content = self.refunded_payment
            self.content_type = MessageContentType.REFUNDED_PAYMENT
        elif self.users_shared is not None:
            self.content = self.users_shared
            self.content_type = MessageContentType.USERS_SHARED
        elif self.chat_shared is not None:
            self.content = self.chat_shared
            self.content_type = MessageContentType.CHAT_SHARED
        elif self.connected_website is not None:
            self.content = self.connected_website
            self.content_type = MessageContentType.CONNECTED_WEBSITE
        elif self.write_access_allowed is not None:
            self.content = self.write_access_allowed
            self.content_type = MessageContentType.WRITE_ACCESS_ALLOWED
        elif self.passport_data is not None:
            self.content = self.passport_data
            self.content_type = MessageContentType.PASSPORT_DATA
        elif self.proximity_alert_triggered is not None:
            self.content = self.proximity_alert_triggered
            self.content_type = MessageContentType.PROXIMITY_ALERT_TRIGGERED
        elif self.boost_added is not None:
            self.content = self.boost_added
            self.content_type = MessageContentType.BOOST_ADDED
        elif self.chat_background_set is not None:
            self.content = self.chat_background_set
            self.content_type = MessageContentType.CHAT_BACKGROUND_SET
        elif self.forum_topic_created is not None:
            self.content = self.forum_topic_created
            self.content_type = MessageContentType.FORUM_TOPIC_CREATED
        elif self.forum_topic_edited is not None:
            self.content = self.forum_topic_edited
            self.content_type = MessageContentType.FORUM_TOPIC_EDITED
        elif self.forum_topic_closed is not None:
            self.content = self.forum_topic_closed
            self.content_type = MessageContentType.FORUM_TOPIC_CLOSED
        elif self.forum_topic_reopened is not None:
            self.content = self.forum_topic_reopened
            self.content_type = MessageContentType.FORUM_TOPIC_REOPENED
        elif self.general_forum_topic_hidden is not None:
            self.content = self.general_forum_topic_hidden
            self.content_type = MessageContentType.GENERAL_FORUM_TOPIC_HIDDEN
        elif self.general_forum_topic_unhidden is not None:
            self.content = self.general_forum_topic_unhidden
            self.content_type = MessageContentType.GENERAL_FORUM_TOPIC_UNHIDDEN
        elif self.giveaway_created is not None:
            self.content = self.giveaway_created
            self.content_type = MessageContentType.GIVEAWAY_CREATED
        elif self.giveaway is not None:
            self.content = self.giveaway
            self.content_type = MessageContentType.GIVEAWAY
        elif self.giveaway_winners is not None:
            self.content = self.giveaway_winners
            self.content_type = MessageContentType.GIVEAWAY_WINNERS
        elif self.giveaway_completed is not None:
            self.content = self.giveaway_completed
            self.content_type = MessageContentType.GIVEAWAY_COMPLETED
        elif self.video_chat_scheduled is not None:
            self.content = self.video_chat_scheduled
            self.content_type = MessageContentType.VIDEO_CHAT_SCHEDULED
        elif self.video_chat_started is not None:
            self.content = self.video_chat_started
            self.content_type = MessageContentType.VIDEO_CHAT_STARTED
        elif self.video_chat_ended is not None:
            self.content = self.video_chat_ended
            self.content_type = MessageContentType.VIDEO_CHAT_ENDED
        elif self.video_chat_participants_invited is not None:
            self.content = self.video_chat_participants_invited
            self.content_type = MessageContentType.VIDEO_CHAT_PARTICIPANTS_INVITED
        elif self.web_app_data is not None:
            self.content = self.web_app_data
            self.content_type = MessageContentType.WEB_APP_DATA
        else:
            self.content = self.content_type = None

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
    def unprefixed_sender_chat_id(self) -> Optional[int]:
        if self.sender_chat_id is not None:
            return get_unprefixed_chat_id(
                chat_id=self.sender_chat_id,
                chat_type=self.sender_chat.type
            )

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
        return self.forward_origin is not None

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
            return None

        entities = self.get_entities()

        return formatter.get_formatted_text(text, entities)
