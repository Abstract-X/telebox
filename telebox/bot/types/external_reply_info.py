from typing import Optional, Literal

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.message_origin import MessageOrigin
from telebox.bot.types.chat import Chat
from telebox.bot.types.link_preview_options import LinkPreviewOptions
from telebox.bot.types.animation import Animation
from telebox.bot.types.audio import Audio
from telebox.bot.types.document import Document
from telebox.bot.types.photo_size import PhotoSize
from telebox.bot.types.sticker import Sticker
from telebox.bot.types.story import Story
from telebox.bot.types.video import Video
from telebox.bot.types.video_note import VideoNote
from telebox.bot.types.voice import Voice
from telebox.bot.types.contact import Contact
from telebox.bot.types.dice import Dice
from telebox.bot.types.game import Game
from telebox.bot.types.giveaway import Giveaway
from telebox.bot.types.giveaway_winners import GiveawayWinners
from telebox.bot.types.invoice import Invoice
from telebox.bot.types.location import Location
from telebox.bot.types.poll import Poll
from telebox.bot.types.venue import Venue
from telebox.bot.types.paid_media_info import PaidMediaInfo


@define(repr=False)
class ExternalReplyInfo(Type):
    origin: MessageOrigin
    chat: Optional[Chat] = None
    message_id: Optional[int] = None
    link_preview_options: Optional[LinkPreviewOptions] = None
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
    has_media_spoiler: Optional[Literal[True]] = None
    contact: Optional[Contact] = None
    dice: Optional[Dice] = None
    game: Optional[Game] = None
    giveaway: Optional[Giveaway] = None
    giveaway_winners: Optional[GiveawayWinners] = None
    invoice: Optional[Invoice] = None
    location: Optional[Location] = None
    poll: Optional[Poll] = None
    venue: Optional[Venue] = None
