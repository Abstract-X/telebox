from typing import Union

from telebox.bot.types.types.inline_query_result_article import (
    InlineQueryResultArticle
)
from telebox.bot.types.types.inline_query_result_photo import (
    InlineQueryResultPhoto
)
from telebox.bot.types.types.inline_query_result_gif import (
    InlineQueryResultGif
)
from telebox.bot.types.types.inline_query_result_mpeg4_gif import (
    InlineQueryResultMpeg4Gif
)
from telebox.bot.types.types.inline_query_result_video import (
    InlineQueryResultVideo
)
from telebox.bot.types.types.inline_query_result_audio import (
    InlineQueryResultAudio
)
from telebox.bot.types.types.inline_query_result_voice import (
    InlineQueryResultVoice
)
from telebox.bot.types.types.inline_query_result_document import (
    InlineQueryResultDocument
)
from telebox.bot.types.types.inline_query_result_location import (
    InlineQueryResultLocation
)
from telebox.bot.types.types.inline_query_result_venue import (
    InlineQueryResultVenue
)
from telebox.bot.types.types.inline_query_result_contact import (
    InlineQueryResultContact
)
from telebox.bot.types.types.inline_query_result_game import (
    InlineQueryResultGame
)
from telebox.bot.types.types.inline_query_result_cached_photo import (
    InlineQueryResultCachedPhoto
)
from telebox.bot.types.types.inline_query_result_cached_gif import (
    InlineQueryResultCachedGif
)
from telebox.bot.types.types.inline_query_result_cached_mpeg4_gif import (
    InlineQueryResultCachedMpeg4Gif
)
from telebox.bot.types.types.inline_query_result_cached_sticker import (
    InlineQueryResultCachedSticker
)
from telebox.bot.types.types.inline_query_result_cached_document import (
    InlineQueryResultCachedDocument
)
from telebox.bot.types.types.inline_query_result_cached_video import (
    InlineQueryResultCachedVideo
)
from telebox.bot.types.types.inline_query_result_cached_voice import (
    InlineQueryResultCachedVoice
)
from telebox.bot.types.types.inline_query_result_cached_audio import (
    InlineQueryResultCachedAudio
)


InlineQueryResult = Union[InlineQueryResultArticle,
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
                          InlineQueryResultGame,
                          InlineQueryResultCachedPhoto,
                          InlineQueryResultCachedGif,
                          InlineQueryResultCachedMpeg4Gif,
                          InlineQueryResultCachedSticker,
                          InlineQueryResultCachedDocument,
                          InlineQueryResultCachedVideo,
                          InlineQueryResultCachedVoice,
                          InlineQueryResultCachedAudio]
