from typing import Type, TypeVar, Any, Optional, Callable
from datetime import datetime as datetime_, timezone
import dataclasses

from dataclass_factory import Factory, Schema

from telebox.bot.types.types.chat_member_owner import ChatMemberOwner
from telebox.bot.types.types.chat_member_administrator import ChatMemberAdministrator
from telebox.bot.types.types.chat_member_member import ChatMemberMember
from telebox.bot.types.types.chat_member_restricted import ChatMemberRestricted
from telebox.bot.types.types.chat_member_left import ChatMemberLeft
from telebox.bot.types.types.chat_member_banned import ChatMemberBanned
from telebox.bot.types.types.bot_command_scope_default import (
    BotCommandScopeDefault
)
from telebox.bot.types.types.bot_command_scope_all_private_chats import (
    BotCommandScopeAllPrivateChats
)
from telebox.bot.types.types.bot_command_scope_all_group_chats import (
    BotCommandScopeAllGroupChats
)
from telebox.bot.types.types.bot_command_scope_all_chat_administrators import (
    BotCommandScopeAllChatAdministrators
)
from telebox.bot.types.types.bot_command_scope_chat import (
    BotCommandScopeChat
)
from telebox.bot.types.types.bot_command_scope_chat_administrators import (
    BotCommandScopeChatAdministrators
)
from telebox.bot.types.types.bot_command_scope_chat_member import (
    BotCommandScopeChatMember
)
from telebox.bot.types.types.menu_button_commands import MenuButtonCommands
from telebox.bot.types.types.menu_button_web_app import MenuButtonWebApp
from telebox.bot.types.types.menu_button_default import MenuButtonDefault
from telebox.bot.types.types.input_media_photo import InputMediaPhoto
from telebox.bot.types.types.input_media_video import InputMediaVideo
from telebox.bot.types.types.input_media_animation import InputMediaAnimation
from telebox.bot.types.types.input_media_audio import InputMediaAudio
from telebox.bot.types.types.input_media_document import InputMediaDocument
from telebox.bot.types.types.force_reply import ForceReply
from telebox.bot.types.types.reply_keyboard_remove import ReplyKeyboardRemove
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
from telebox.bot.types.types.inline_query_result_game import InlineQueryResultGame
from telebox.bot.types.types.input_file import InputFile
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
from telebox.bot.types.types.passport_element_error_data_field import (
    PassportElementErrorDataField
)
from telebox.bot.types.types.passport_element_error_front_side import (
    PassportElementErrorFrontSide
)
from telebox.bot.types.types.passport_element_error_reverse_side import (
    PassportElementErrorReverseSide
)
from telebox.bot.types.types.passport_element_error_selfie import (
    PassportElementErrorSelfie
)
from telebox.bot.types.types.passport_element_error_file import (
    PassportElementErrorFile
)
from telebox.bot.types.types.passport_element_error_files import (
    PassportElementErrorFiles
)
from telebox.bot.types.types.passport_element_error_translation_file import (
    PassportElementErrorTranslationFile
)
from telebox.bot.types.types.passport_element_error_translation_files import (
    PassportElementErrorTranslationFiles
)
from telebox.bot.types.types.passport_element_error_unspecified import (
    PassportElementErrorUnspecified
)
from telebox.bot.types.types.reaction_type_emoji import ReactionTypeEmoji
from telebox.bot.types.types.reaction_type_custom_emoji import ReactionTypeCustomEmoji
from telebox.bot.types.types.reaction_type_paid import ReactionTypePaid
from telebox.bot.types.types.message_origin_user import MessageOriginUser
from telebox.bot.types.types.message_origin_hidden_user import MessageOriginHiddenUser
from telebox.bot.types.types.message_origin_chat import MessageOriginChat
from telebox.bot.types.types.message_origin_channel import MessageOriginChannel
from telebox.bot.types.types.chat_boost_source_premium import ChatBoostSourcePremium
from telebox.bot.types.types.chat_boost_source_gift_code import ChatBoostSourceGiftCode
from telebox.bot.types.types.chat_boost_source_giveaway import ChatBoostSourceGiveaway
from telebox.bot.types.types.background_fill_solid import BackgroundFillSolid
from telebox.bot.types.types.background_fill_gradient import BackgroundFillGradient
from telebox.bot.types.types.background_fill_freeform_gradient import BackgroundFillFreeformGradient
from telebox.bot.types.types.background_type_fill import BackgroundTypeFill
from telebox.bot.types.types.background_type_wallpaper import BackgroundTypeWallpaper
from telebox.bot.types.types.background_type_pattern import BackgroundTypePattern
from telebox.bot.types.types.background_type_chat_theme import BackgroundTypeChatTheme
from telebox.bot.types.types.revenue_withdrawal_state_pending import RevenueWithdrawalStatePending
from telebox.bot.types.types.revenue_withdrawal_state_succeeded import (
    RevenueWithdrawalStateSucceeded
)
from telebox.bot.types.types.revenue_withdrawal_state_failed import RevenueWithdrawalStateFailed
from telebox.bot.types.types.transaction_partner_user import TransactionPartnerUser
from telebox.bot.types.types.transaction_partner_fragment import TransactionPartnerFragment
from telebox.bot.types.types.transaction_partner_telegram_ads import TransactionPartnerTelegramAds
from telebox.bot.types.types.transaction_partner_other import TransactionPartnerOther
from telebox.bot.types.types.input_paid_media_photo import InputPaidMediaPhoto
from telebox.bot.types.types.input_paid_media_video import InputPaidMediaVideo
from telebox.bot.types.types.paid_media_preview import PaidMediaPreview
from telebox.bot.types.types.paid_media_photo import PaidMediaPhoto
from telebox.bot.types.types.paid_media_video import PaidMediaVideo
from telebox.utils.not_set import NotSet, NOT_SET


DataclassObject = TypeVar("DataclassObject")
_DEFAULT_POST_SERIALIZATION_CLASSES = (
    ForceReply,
    ReplyKeyboardRemove,

    ChatMemberOwner,
    ChatMemberAdministrator,
    ChatMemberMember,
    ChatMemberRestricted,
    ChatMemberLeft,
    ChatMemberBanned,

    BotCommandScopeDefault,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeChat,
    BotCommandScopeChatAdministrators,
    BotCommandScopeChatMember,

    MenuButtonCommands,
    MenuButtonWebApp,
    MenuButtonDefault,

    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,

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
    InlineQueryResultGame,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedGif,
    InlineQueryResultCachedMpeg4Gif,
    InlineQueryResultCachedSticker,
    InlineQueryResultCachedDocument,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedVoice,
    InlineQueryResultCachedAudio,

    PassportElementErrorDataField,
    PassportElementErrorFrontSide,
    PassportElementErrorReverseSide,
    PassportElementErrorSelfie,
    PassportElementErrorFile,
    PassportElementErrorFiles,
    PassportElementErrorTranslationFile,
    PassportElementErrorTranslationFiles,
    PassportElementErrorUnspecified,

    ReactionTypeEmoji,
    ReactionTypeCustomEmoji,
    ReactionTypePaid,

    MessageOriginUser,
    MessageOriginHiddenUser,
    MessageOriginChat,
    MessageOriginChannel,

    ChatBoostSourcePremium,
    ChatBoostSourceGiftCode,
    ChatBoostSourceGiveaway,

    BackgroundFillSolid,
    BackgroundFillGradient,
    BackgroundFillFreeformGradient,

    BackgroundTypeFill,
    BackgroundTypeWallpaper,
    BackgroundTypePattern,
    BackgroundTypeChatTheme,

    RevenueWithdrawalStatePending,
    RevenueWithdrawalStateSucceeded,
    RevenueWithdrawalStateFailed,

    TransactionPartnerUser,
    TransactionPartnerFragment,
    TransactionPartnerTelegramAds,
    TransactionPartnerOther,

    InputPaidMediaPhoto,
    InputPaidMediaVideo,

    PaidMediaPreview,
    PaidMediaPhoto,
    PaidMediaVideo
)


def get_timestamp(datetime: Optional[datetime_]) -> int:
    return int(datetime.timestamp()) if datetime is not None else 0


def get_datetime(timestamp: int) -> Optional[datetime_]:
    return datetime_.fromtimestamp(timestamp, tz=timezone.utc) if timestamp else None


class DataclassConverter:

    # noinspection PyMethodMayBeStatic
    def get_object(
        self,
        data: dict[str, Any],
        class_: Type[DataclassObject]
    ) -> DataclassObject:
        return _dataclass_factory.load(data, class_)

    # noinspection PyMethodMayBeStatic
    def get_data(self, object_: Any) -> dict[str, Any]:
        return _dataclass_factory.dump(object_)


def _get_dataclass_factory() -> Factory:
    schemas = {
        datetime_: Schema(
            serializer=get_timestamp,
            parser=get_datetime
        ),
        InputFile: Schema(
            serializer=lambda file: file,
            parser=lambda file: file
        ),
        NotSet: Schema(
            serializer=lambda not_set: NOT_SET,
            parser=lambda not_set: NOT_SET
        )
    }

    for class_ in _DEFAULT_POST_SERIALIZATION_CLASSES:
        for field in dataclasses.fields(class_):
            if field.default not in frozenset((None, dataclasses.MISSING)):
                schemas[class_] = Schema(
                    post_serialize=_get_post_default_serializer(field.name, field.default)
                )

    return Factory(
        default_schema=Schema(
            omit_default=True
        ),
        schemas=schemas
    )


def _get_post_default_serializer(
    key: str,
    value: Any
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    def _serializer(data: dict[str, Any]) -> dict[str, Any]:
        data[key] = value

        return data

    return _serializer


_dataclass_factory = _get_dataclass_factory()
