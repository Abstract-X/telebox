from .update import Update
from .webhook_info import WebhookInfo
from .user import User
from .chat import Chat
from .message import Message
from .message_id import MessageId
from .message_entity import MessageEntity
from .photo_size import PhotoSize
from .animation import Animation
from .audio import Audio
from .document import Document
from .story import Story
from .video import Video
from .video_note import VideoNote
from .voice import Voice
from .contact import Contact
from .dice import Dice
from .poll_option import PollOption
from .poll_answer import PollAnswer
from .poll import Poll
from .location import Location
from .venue import Venue
from .web_app_data import WebAppData
from .proximity_alert_triggered import ProximityAlertTriggered
from .message_auto_delete_timer_changed import MessageAutoDeleteTimerChanged
from .forum_topic_created import ForumTopicCreated
from .forum_topic_edited import ForumTopicEdited
from .forum_topic_closed import ForumTopicClosed
from .forum_topic_reopened import ForumTopicReopened
from .general_forum_topic_hidden import GeneralForumTopicHidden
from .general_forum_topic_unhidden import GeneralForumTopicUnhidden
from .users_shared import UsersShared
from .chat_shared import ChatShared
from .video_chat_scheduled import VideoChatScheduled
from .video_chat_started import VideoChatStarted
from .video_chat_ended import VideoChatEnded
from .video_chat_participants_invited import VideoChatParticipantsInvited
from .user_profile_photos import UserProfilePhotos
from .file import File
from .web_app_info import WebAppInfo
from .reply_keyboard_markup import ReplyKeyboardMarkup
from .keyboard_button import KeyboardButton
from .keyboard_button_request_users import KeyboardButtonRequestUsers
from .keyboard_button_request_chat import KeyboardButtonRequestChat
from .keyboard_button_poll_type import KeyboardButtonPollType
from .reply_keyboard_remove import ReplyKeyboardRemove
from .inline_keyboard_markup import InlineKeyboardMarkup
from .inline_keyboard_button import InlineKeyboardButton
from .login_url import LoginUrl
from .callback_query import CallbackQuery
from .force_reply import ForceReply
from .chat_photo import ChatPhoto
from .chat_invite_link import ChatInviteLink
from .chat_administrator_rights import ChatAdministratorRights
from .chat_member import ChatMember
from .chat_member_owner import ChatMemberOwner
from .chat_member_administrator import ChatMemberAdministrator
from .chat_member_member import ChatMemberMember
from .chat_member_restricted import ChatMemberRestricted
from .chat_member_left import ChatMemberLeft
from .chat_member_banned import ChatMemberBanned
from .chat_member_updated import ChatMemberUpdated
from .chat_join_request import ChatJoinRequest
from .chat_permissions import ChatPermissions
from .chat_location import ChatLocation
from .forum_topic import ForumTopic
from .bot_command import BotCommand
from .bot_command_scope import BotCommandScope
from .bot_command_scope_default import BotCommandScopeDefault
from .bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats
from .bot_command_scope_all_group_chats import BotCommandScopeAllGroupChats
from .bot_command_scope_all_chat_administrators import BotCommandScopeAllChatAdministrators
from .bot_command_scope_chat import BotCommandScopeChat
from .bot_command_scope_chat_administrators import BotCommandScopeChatAdministrators
from .bot_command_scope_chat_member import BotCommandScopeChatMember
from .bot_description import BotDescription
from .bot_short_description import BotShortDescription
from .menu_button import MenuButton
from .menu_button_commands import MenuButtonCommands
from .menu_button_web_app import MenuButtonWebApp
from .menu_button_default import MenuButtonDefault
from .response_parameters import ResponseParameters
from .input_media import InputMedia
from .input_media_photo import InputMediaPhoto
from .input_media_video import InputMediaVideo
from .input_media_animation import InputMediaAnimation
from .input_media_audio import InputMediaAudio
from .input_media_document import InputMediaDocument
from .input_file import InputFile
from .sticker import Sticker
from .sticker_set import StickerSet
from .mask_position import MaskPosition
from .input_sticker import InputSticker
from .inline_query import InlineQuery
from .inline_query_results_button import InlineQueryResultsButton
from .inline_query_result import InlineQueryResult
from .inline_query_result_article import InlineQueryResultArticle
from .inline_query_result_photo import InlineQueryResultPhoto
from .inline_query_result_gif import InlineQueryResultGif
from .inline_query_result_mpeg4_gif import InlineQueryResultMpeg4Gif
from .inline_query_result_video import InlineQueryResultVideo
from .inline_query_result_audio import InlineQueryResultAudio
from .inline_query_result_voice import InlineQueryResultVoice
from .inline_query_result_document import InlineQueryResultDocument
from .inline_query_result_location import InlineQueryResultLocation
from .inline_query_result_venue import InlineQueryResultVenue
from .inline_query_result_contact import InlineQueryResultContact
from .inline_query_result_game import InlineQueryResultGame
from .inline_query_result_cached_photo import InlineQueryResultCachedPhoto
from .inline_query_result_cached_gif import InlineQueryResultCachedGif
from .inline_query_result_cached_mpeg4_gif import InlineQueryResultCachedMpeg4Gif
from .inline_query_result_cached_sticker import InlineQueryResultCachedSticker
from .inline_query_result_cached_document import InlineQueryResultCachedDocument
from .inline_query_result_cached_video import InlineQueryResultCachedVideo
from .inline_query_result_cached_voice import InlineQueryResultCachedVoice
from .inline_query_result_cached_audio import InlineQueryResultCachedAudio
from .input_message_content import InputMessageContent
from .input_text_message_content import InputTextMessageContent
from .input_location_message_content import InputLocationMessageContent
from .input_venue_message_content import InputVenueMessageContent
from .input_contact_message_content import InputContactMessageContent
from .input_invoice_message_content import InputInvoiceMessageContent
from .chosen_inline_result import ChosenInlineResult
from .sent_web_app_message import SentWebAppMessage
from .labeled_price import LabeledPrice
from .invoice import Invoice
from .shipping_address import ShippingAddress
from .order_info import OrderInfo
from .shipping_option import ShippingOption
from .successful_payment import SuccessfulPayment
from .write_access_allowed import WriteAccessAllowed
from .shipping_query import ShippingQuery
from .pre_checkout_query import PreCheckoutQuery
from .passport_data import PassportData
from .passport_file import PassportFile
from .encrypted_passport_element import EncryptedPassportElement
from .encrypted_credentials import EncryptedCredentials
from .passport_element_error import PassportElementError
from .passport_element_error_data_field import PassportElementErrorDataField
from .passport_element_error_front_side import PassportElementErrorFrontSide
from .passport_element_error_reverse_side import PassportElementErrorReverseSide
from .passport_element_error_selfie import PassportElementErrorSelfie
from .passport_element_error_file import PassportElementErrorFile
from .passport_element_error_files import PassportElementErrorFiles
from .passport_element_error_translation_file import PassportElementErrorTranslationFile
from .passport_element_error_translation_files import PassportElementErrorTranslationFiles
from .passport_element_error_unspecified import PassportElementErrorUnspecified
from .game import Game
from .callback_game import CallbackGame
from .game_high_score import GameHighScore
from .reaction_type import ReactionType
from .reaction_type_emoji import ReactionTypeEmoji
from .reaction_type_custom_emoji import ReactionTypeCustomEmoji
from .message_reaction_updated import MessageReactionUpdated
from .message_reaction_count_updated import MessageReactionCountUpdated
from .external_reply_info import ExternalReplyInfo
from .text_quote import TextQuote
from .reply_parameters import ReplyParameters
from .link_preview_options import LinkPreviewOptions
from .input_text_message_content import InputTextMessageContent
from .chat_boost_updated import ChatBoostUpdated
from .chat_boost_removed import ChatBoostRemoved
from .chat_boost_source import ChatBoostSource
from .chat_boost_source_premium import ChatBoostSourcePremium
from .chat_boost_source_gift_code import ChatBoostSourceGiftCode
from .chat_boost_source_giveaway import ChatBoostSourceGiveaway
from .giveaway import Giveaway
from .giveaway_created import GiveawayCreated
from .giveaway_winners import GiveawayWinners
from .giveaway_completed import GiveawayCompleted
from .message_origin import MessageOrigin
from .message_origin_user import MessageOriginUser
from .message_origin_hidden_user import MessageOriginHiddenUser
from .message_origin_chat import MessageOriginChat
from .message_origin_channel import MessageOriginChannel
from .maybe_inaccessible_message import MaybeInaccessibleMessage
from .inaccessible_message import InaccessibleMessage
from .business_connection import BusinessConnection
from .business_messages_deleted import BusinessMessagesDeleted
from .business_intro import BusinessIntro
from .business_location import BusinessLocation
from .business_opening_hours import BusinessOpeningHours
from .business_opening_hours_interval import BusinessOpeningHoursInterval
from .shared_user import SharedUser
from .birthdate import Birthdate
from .input_poll_option import InputPollOption
from .background_fill import BackgroundFill
from .background_fill_solid import BackgroundFillSolid
from .background_fill_gradient import BackgroundFillGradient
from .background_fill_freeform_gradient import BackgroundFillFreeformGradient
from .background_type import BackgroundType
from .background_type_fill import BackgroundTypeFill
from .background_type_wallpaper import BackgroundTypeWallpaper
from .background_type_pattern import BackgroundTypePattern
from .background_type_chat_theme import BackgroundTypeChatTheme
from .chat_background import ChatBackground
from .chat_full_info import ChatFullInfo
from .revenue_withdrawal_state import RevenueWithdrawalState
from .revenue_withdrawal_state_pending import RevenueWithdrawalStatePending
from .revenue_withdrawal_state_succeeded import RevenueWithdrawalStateSucceeded
from .revenue_withdrawal_state_failed import RevenueWithdrawalStateFailed
from .star_transaction import StarTransaction
from .star_transactions import StarTransactions
from .transaction_partner import TransactionPartner
from .transaction_partner_user import TransactionPartnerUser
from .transaction_partner_fragment import TransactionPartnerFragment
from .transaction_partner_telegram_ads import TransactionPartnerTelegramAds
from .transaction_partner_other import TransactionPartnerOther
from .paid_media_info import PaidMediaInfo
from .refunded_payment import RefundedPayment
from .web_app_init_data import WebAppInitData
from .web_app_user import WebAppUser
from .web_app_chat import WebAppChat
from .reaction_type_paid import ReactionTypePaid


__all__ = [
    "Update",
    "WebhookInfo",
    "User",
    "Chat",
    "Message",
    "MessageId",
    "MessageEntity",
    "PhotoSize",
    "Animation",
    "Audio",
    "Document",
    "Story",
    "Video",
    "VideoNote",
    "Voice",
    "Contact",
    "Dice",
    "PollOption",
    "PollAnswer",
    "Poll",
    "Location",
    "Venue",
    "WebAppData",
    "ProximityAlertTriggered",
    "MessageAutoDeleteTimerChanged",
    "ForumTopicCreated",
    "ForumTopicEdited",
    "ForumTopicClosed",
    "ForumTopicReopened",
    "GeneralForumTopicHidden",
    "GeneralForumTopicUnhidden",
    "UsersShared",
    "ChatShared",
    "VideoChatScheduled",
    "VideoChatStarted",
    "VideoChatEnded",
    "VideoChatParticipantsInvited",
    "UserProfilePhotos",
    "File",
    "WebAppInfo",
    "ReplyKeyboardMarkup",
    "KeyboardButton",
    "KeyboardButtonRequestUsers",
    "KeyboardButtonRequestChat",
    "KeyboardButtonPollType",
    "ReplyKeyboardRemove",
    "InlineKeyboardMarkup",
    "InlineKeyboardButton",
    "LoginUrl",
    "CallbackQuery",
    "ForceReply",
    "ChatPhoto",
    "ChatInviteLink",
    "ChatAdministratorRights",
    "ChatMember",
    "ChatMemberOwner",
    "ChatMemberAdministrator",
    "ChatMemberMember",
    "ChatMemberRestricted",
    "ChatMemberLeft",
    "ChatMemberBanned",
    "ChatMemberUpdated",
    "ChatJoinRequest",
    "ChatPermissions",
    "ChatLocation",
    "ForumTopic",
    "BotCommand",
    "BotCommandScope",
    "BotCommandScopeDefault",
    "BotCommandScopeAllPrivateChats",
    "BotCommandScopeAllGroupChats",
    "BotCommandScopeAllChatAdministrators",
    "BotCommandScopeChat",
    "BotCommandScopeChatAdministrators",
    "BotCommandScopeChatMember",
    "BotDescription",
    "BotShortDescription",
    "MenuButton",
    "MenuButtonCommands",
    "MenuButtonWebApp",
    "MenuButtonDefault",
    "ResponseParameters",
    "InputMedia",
    "InputMediaPhoto",
    "InputMediaVideo",
    "InputMediaAnimation",
    "InputMediaAudio",
    "InputMediaDocument",
    "InputFile",
    "Sticker",
    "StickerSet",
    "MaskPosition",
    "InputSticker",
    "InlineQuery",
    "InlineQueryResultsButton",
    "InlineQueryResult",
    "InlineQueryResultArticle",
    "InlineQueryResultPhoto",
    "InlineQueryResultGif",
    "InlineQueryResultMpeg4Gif",
    "InlineQueryResultVideo",
    "InlineQueryResultAudio",
    "InlineQueryResultVoice",
    "InlineQueryResultDocument",
    "InlineQueryResultLocation",
    "InlineQueryResultVenue",
    "InlineQueryResultContact",
    "InlineQueryResultGame",
    "InlineQueryResultCachedPhoto",
    "InlineQueryResultCachedGif",
    "InlineQueryResultCachedMpeg4Gif",
    "InlineQueryResultCachedSticker",
    "InlineQueryResultCachedDocument",
    "InlineQueryResultCachedVideo",
    "InlineQueryResultCachedVoice",
    "InlineQueryResultCachedAudio",
    "InputMessageContent",
    "InputTextMessageContent",
    "InputLocationMessageContent",
    "InputVenueMessageContent",
    "InputContactMessageContent",
    "InputInvoiceMessageContent",
    "ChosenInlineResult",
    "SentWebAppMessage",
    "LabeledPrice",
    "Invoice",
    "ShippingAddress",
    "OrderInfo",
    "ShippingOption",
    "SuccessfulPayment",
    "WriteAccessAllowed",
    "ShippingQuery",
    "PreCheckoutQuery",
    "PassportData",
    "PassportFile",
    "EncryptedPassportElement",
    "EncryptedCredentials",
    "PassportElementError",
    "PassportElementErrorDataField",
    "PassportElementErrorFrontSide",
    "PassportElementErrorReverseSide",
    "PassportElementErrorSelfie",
    "PassportElementErrorFile",
    "PassportElementErrorFiles",
    "PassportElementErrorTranslationFile",
    "PassportElementErrorTranslationFiles",
    "PassportElementErrorUnspecified",
    "Game",
    "CallbackGame",
    "GameHighScore",
    "ReactionType",
    "ReactionTypeEmoji",
    "ReactionTypeCustomEmoji",
    "MessageReactionUpdated",
    "MessageReactionCountUpdated",
    "ExternalReplyInfo",
    "TextQuote",
    "ReplyParameters",
    "LinkPreviewOptions",
    "InputTextMessageContent",
    "ChatBoostUpdated",
    "ChatBoostRemoved",
    "ChatBoostSource",
    "ChatBoostSourcePremium",
    "ChatBoostSourceGiftCode",
    "ChatBoostSourceGiveaway",
    "Giveaway",
    "GiveawayCreated",
    "GiveawayWinners",
    "GiveawayCompleted",
    "MessageOrigin",
    "MessageOriginUser",
    "MessageOriginHiddenUser",
    "MessageOriginChat",
    "MessageOriginChannel",
    "MaybeInaccessibleMessage",
    "InaccessibleMessage",
    "BusinessConnection",
    "BusinessMessagesDeleted",
    "BusinessIntro",
    "BusinessLocation",
    "BusinessOpeningHours",
    "BusinessOpeningHoursInterval",
    "SharedUser",
    "Birthdate",
    "InputPollOption",
    "BackgroundFill",
    "BackgroundFillSolid",
    "BackgroundFillGradient",
    "BackgroundFillFreeformGradient",
    "BackgroundType",
    "BackgroundTypeFill",
    "BackgroundTypeWallpaper",
    "BackgroundTypePattern",
    "BackgroundTypeChatTheme",
    "ChatBackground",
    "ChatFullInfo",
    "RevenueWithdrawalState",
    "RevenueWithdrawalStatePending",
    "RevenueWithdrawalStateSucceeded",
    "RevenueWithdrawalStateFailed",
    "StarTransaction",
    "StarTransactions",
    "TransactionPartner",
    "TransactionPartnerUser",
    "TransactionPartnerFragment",
    "TransactionPartnerTelegramAds",
    "TransactionPartnerOther",
    "PaidMediaInfo",
    "RefundedPayment",
    "WebAppInitData",
    "WebAppUser",
    "WebAppChat",
    "ReactionTypePaid"
]
