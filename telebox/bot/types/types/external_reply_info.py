from dataclasses import dataclass
from typing import Optional, Literal

from telebox.bot.types.type import Type
from telebox.bot.types.types.message_origin import MessageOrigin
from telebox.bot.types.types.chat import Chat
from telebox.bot.types.types.link_preview_options import LinkPreviewOptions
from telebox.bot.types.types.animation import Animation
from telebox.bot.types.types.audio import Audio
from telebox.bot.types.types.document import Document
from telebox.bot.types.types.photo_size import PhotoSize
from telebox.bot.types.types.sticker import Sticker
from telebox.bot.types.types.story import Story
from telebox.bot.types.types.video import Video
from telebox.bot.types.types.video_note import VideoNote
from telebox.bot.types.types.voice import Voice
from telebox.bot.types.types.contact import Contact
from telebox.bot.types.types.dice import Dice
from telebox.bot.types.types.game import Game
from telebox.bot.types.types.giveaway import Giveaway
from telebox.bot.types.types.giveaway_winners import GiveawayWinners
from telebox.bot.types.types.invoice import Invoice
from telebox.bot.types.types.location import Location
from telebox.bot.types.types.poll import Poll
from telebox.bot.types.types.venue import Venue


@dataclass
class ExternalReplyInfo(Type):
    origin: MessageOrigin
    chat: Optional[Chat] = None
    message_id: Optional[int] = None
    link_preview_options: Optional[LinkPreviewOptions] = None
    animation: Optional[Animation] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
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
