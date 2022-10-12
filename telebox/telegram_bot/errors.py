from dataclasses import dataclass
from typing import Optional, Any, TYPE_CHECKING
from http import HTTPStatus

from telebox.errors import TeleboxError
if TYPE_CHECKING:
    from telebox.telegram_bot.types.types.response_parameters import ResponseParameters


@dataclass
class TelegramBotError(TeleboxError):
    """General class for Telegram Bot errors."""


@dataclass
class UnknownUpdateContentError(TelegramBotError):
    """Class for unknown update content error."""


@dataclass
class UnknownMessageContentError(TelegramBotError):
    """Class for unknown message content error."""


@dataclass
class RequestError(TelegramBotError):
    """Class for Telegram Bot API request error."""
    DEFAULT_TEMPLATE = "\n".join((
        "A request to the Telegram Bot API was unsuccessful!",
        "├─ Method: {method!r}",
        "├─ Parameters: {parameters!r}",
        "├─ Status code: {status_code!r}",
        "└─ Description: {description!r}"
    ))
    method: str
    parameters: dict[str, Any]
    status_code: int
    description: str


@dataclass
class BadRequestError(RequestError):
    """Error class for 400 status code."""


@dataclass
class ChatNotFoundError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: chat not found',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class UserNotFoundError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: user not found',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class MessageIsNotModifiedError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: message is not modified',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class ChatDescriptionIsNotModifiedError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: chat description is not modified',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class MessageToForwardNotFoundError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: message to forward not found',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class MessageToDeleteNotFoundError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: message to delete not found',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class MessageToEditNotFoundError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: message to edit not found',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class PollAlreadyClosedError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: poll has already been closed',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class PollMustHaveMoreOptionsError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: poll must have at least 2 option',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class PollCannotHaveMoreOptionsError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: poll can't have more than 10 options',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class PollOptionsMustBeNonEmptyError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: poll options must be non-empty',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class PollQuestionMustBeNonEmptyError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: poll question must be non-empty',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class PollOptionsLengthIsTooLongError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: poll options length must not exceed 100',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class PollQuestionLengthIsTooLongError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: poll question length must not exceed 255',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class MessageWithPollToStopNotFoundError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: message with poll to stop not found',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class MessageIsNotPollError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: message is not a poll',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class InvalidMessageIDError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: MESSAGE_ID_INVALID',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class PrivateChannelError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: CHANNEL_PRIVATE',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class WriteToChatForbiddenError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: CHAT_WRITE_FORBIDDEN',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class MessageToPinNotFoundError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: message to pin not found',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class NoRightsToManagePinnedMessagesError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: not enough rights to manage pinned messages in the chat',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class NoRightsToExportChatInviteLinkError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: not enough rights to export chat invite link',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class NoRightsToRestrictUnrestrictChatMemberError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: not enough rights to restrict/unrestrict chat member',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class NoRightsToSendMessageError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: have no rights to send a message',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class RepliedMessageNotFoundError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: replied message not found',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class MessageIDIsNotSpecifiedError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: message identifier is not specified',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class MessageTextIsEmptyError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: message text is empty',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class MessageCannotBeEditedError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: message can't be edited',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class MessageCannotBeDeletedError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: message can't be deleted',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class GroupWasUpgradedToSupergroupError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: group chat was upgraded to a supergroup chat',
        'error_code': 400,
        'ok': False,
        'parameters': {
            'migrate_to_chat_id': -100123456789
        }
    }
    """
    ALL_REPLACEMENT_FIELDS_IS_REQUIRED = False
    migrate_to_chat_id: int


@dataclass
class MessageIsTooLongError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: message is too long',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class QueryIsTooOldOrInvalidIDError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: query is too old and response timeout expired or query ID is invalid',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class InvalidButtonURLError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: BUTTON_URL_INVALID',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class InvalidButtonDataError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: BUTTON_DATA_INVALID',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class InlineKeyboardButtonParsingError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: can't parse inline keyboard button: Text buttons are unallowed in the inline keyboard',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class WrongFileIDError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: wrong file id',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class GroupIsDeactivatedError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: group is deactivated',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class PhotoShouldBeUploadedAsInputFileError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: photo should be uploaded as an InputFile',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class InvalidStickerSetError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: STICKERSET_INVALID',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class TooMuchMessagesToSendAsAlbumError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: too much messages to send as an album',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class DemoteChatCreatorError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: can't demote chat creator',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class SelfRestrictError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: can't restrict self',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class WebhookURLMustBeHTTPSError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: bad webhook: HTTPS url must be provided for webhook',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class URLParsingError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: can't parse URL',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class BadWebhookPortError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: bad webhook: Webhook can be set up only on ports 80, 88, 443 or 8443',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class UnknownWebhookHostError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: bad webhook: Failed to resolve host: Name or service not known',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class MessageEntitiesParsingError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: can't parse entities',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class WrongHTTPURLError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: wrong HTTP URL',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class InvalidFileIDError(BadRequestError):
    """Error class for this response:
    {
        'description': 'Bad Request: invalid file id',
        'error_code': 400,
        'ok': False
    }
    """


@dataclass
class UnauthorizedError(RequestError):
    """Error class for 401 status code."""


@dataclass
class ForbiddenError(RequestError):
    """Error class for 403 status code."""


@dataclass
class BotWasBlockedByUserError(ForbiddenError):
    """Error class for this response:
    {
        'description': 'Forbidden: bot was blocked by the user',
        'error_code': 403,
        'ok': False
    }
    """


@dataclass
class UserIsDeactivatedError(ForbiddenError):
    """Error class for this response:
    {
        'description': 'Forbidden: user is deactivated',
        'error_code': 403,
        'ok': False
    }
    """


@dataclass
class BotWasKickedFromGroupError(ForbiddenError):
    """Error class for this response:
    {
        'description': 'Forbidden: bot was kicked from the group chat',
        'error_code': 403,
        'ok': False
    }
    """


@dataclass
class BotWasKickedFromSupergroupError(ForbiddenError):
    """Error class for this response:
    {
        'description': 'Forbidden: bot was kicked from the supergroup chat',
        'error_code': 403,
        'ok': False
    }
    """


@dataclass
class BotCannotInitiateConversationWithUserError(ForbiddenError):
    """Error class for this response:
    {
        'description': 'Forbidden: bot can't initiate conversation with a user',
        'error_code': 403,
        'ok': False
    }
    """


@dataclass
class DeleteMessageForbiddenError(ForbiddenError):
    """Error class for this response:
    {
        'description': 'Forbidden: MESSAGE_DELETE_FORBIDDEN',
        'error_code': 403,
        'ok': False
    }
    """


@dataclass
class BotIsNotSupergroupMemberError(ForbiddenError):
    """Error class for this response:
    {
        'description': 'Forbidden: bot is not a member of the supergroup chat',
        'error_code': 403,
        'ok': False
    }
    """


@dataclass
class BotIsNotChannelMemberError(ForbiddenError):
    """Error class for this response:
    {
        'description': 'Forbidden: bot is not a member of the channel chat',
        'error_code': 403,
        'ok': False
    }
    """


@dataclass
class BotCannotSendMessagesToBotsError(ForbiddenError):
    """Error class for this response:
    {
        'description': 'Forbidden: bot can't send messages to bots',
        'error_code': 403,
        'ok': False
    }
    """


@dataclass
class ConflictError(RequestError):
    """Error class for 409 status code."""


@dataclass
class MultipleGetUpdatesError(ConflictError):
    """Error class for this response:
    {
        'description': 'Conflict: terminated by other getUpdates request; make sure that only one bot instance is running',
        'error_code': 409,
        'ok': False
    }
    """


@dataclass
class CannotUseGetUpdatesWhileWebhookIsActiveError(ConflictError):
    """Error class for this response:
    {
        'description': 'Conflict: can't use getUpdates method while webhook is active; use deleteWebhook to delete the webhook first',
        'error_code': 409,
        'ok': False
    }
    """


@dataclass
class RequestEntityTooLargeError(RequestError):
    """Error class for 413 status code."""


@dataclass
class TooManyRequestsError(RequestError):
    """Error class for 429 status code."""


@dataclass
class RetryAfterError(TooManyRequestsError):
    """Error class for this response:
    {
        'description': 'Too Many Requests: retry after 42',
        'error_code': 429,
        'ok': False,
        'parameters': {
            'retry_after': 42
        }
    }
    """
    ALL_REPLACEMENT_FIELDS_IS_REQUIRED = False
    retry_after: int


@dataclass
class InternalServerError(RequestError):
    """Error class for 500 status code."""


@dataclass
class ServerIsRestartingError(InternalServerError):
    """Error class for this response:
    {
        'description': 'Internal Server Error: restart',
        'error_code': 500,
        'ok': False
    }
    """


def get_request_error(
    method: str,
    parameters: dict[str, Any],
    status_code: int,
    description: str,
    *,
    response_parameters: Optional["ResponseParameters"] = None
) -> RequestError:
    kwargs = {
        "method": method,
        "parameters": {
            name: value
            for name, value in parameters.items()
            if value is not None
        },
        "status_code": status_code,
        "description": description
    }

    if status_code == HTTPStatus.BAD_REQUEST:
        return _get_bad_request_error(kwargs, response_parameters)
    elif status_code == HTTPStatus.UNAUTHORIZED:
        return _get_unauthorized_error(kwargs)
    elif status_code == HTTPStatus.FORBIDDEN:
        return _get_forbidden_error(kwargs)
    elif status_code == HTTPStatus.CONFLICT:
        return _get_conflict_error(kwargs)
    elif status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
        return _get_request_entity_too_large_error(kwargs)
    elif status_code == HTTPStatus.TOO_MANY_REQUESTS:
        return _get_too_many_requests_error(kwargs, response_parameters)
    elif status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        return _get_internal_server_error(kwargs)

    return RequestError(None, **kwargs)


def _get_bad_request_error(
    kwargs: dict[str, Any],
    response_parameters: "ResponseParameters"
) -> BadRequestError:
    lowered_description = kwargs["description"].lower()

    for message, error_type in (
        ("chat not found", ChatNotFoundError),
        ("user not found", UserNotFoundError),
        ("message is not modified", MessageIsNotModifiedError),
        ("chat description is not modified", ChatDescriptionIsNotModifiedError),
        ("message to forward not found", MessageToForwardNotFoundError),
        ("message to delete not found", MessageToDeleteNotFoundError),
        ("message to edit not found", MessageToEditNotFoundError),
        ("poll has already been closed", PollAlreadyClosedError),
        ("poll must have at least", PollMustHaveMoreOptionsError),
        ("poll can't have more than", PollCannotHaveMoreOptionsError),
        ("poll options must be non-empty", PollOptionsMustBeNonEmptyError),
        ("poll question must be non-empty", PollQuestionMustBeNonEmptyError),
        ("poll options length must not exceed", PollOptionsLengthIsTooLongError),
        ("poll question length must not exceed", PollQuestionLengthIsTooLongError),
        ("message with poll to stop not found", MessageWithPollToStopNotFoundError),
        ("message is not a poll", MessageIsNotPollError),
        ("message_id_invalid", InvalidMessageIDError),
        ("channel_private", PrivateChannelError),
        ("chat_write_forbidden", WriteToChatForbiddenError),
        ("message to pin not found", MessageToPinNotFoundError),
        (
            "not enough rights to manage pinned messages in the chat",
            NoRightsToManagePinnedMessagesError
        ),
        ("not enough rights to export chat invite link", NoRightsToExportChatInviteLinkError),
        (
            "not enough rights to restrict/unrestrict chat member",
            NoRightsToRestrictUnrestrictChatMemberError
        ),
        ("have no rights to send a message", NoRightsToSendMessageError),
        ("replied message not found", RepliedMessageNotFoundError),
        ("message identifier is not specified", MessageIDIsNotSpecifiedError),
        ("message text is empty", MessageTextIsEmptyError),
        ("message can't be edited", MessageCannotBeEditedError),
        ("message can't be deleted", MessageCannotBeDeletedError),
        ("group chat was upgraded to a supergroup chat", GroupWasUpgradedToSupergroupError),
        ("message is too long", MessageIsTooLongError),
        (
            "query is too old and response timeout expired or query id is invalid",
            QueryIsTooOldOrInvalidIDError
        ),
        ("button_url_invalid", InvalidButtonURLError),
        ("button_data_invalid", InvalidButtonDataError),
        ("can't parse inline keyboard button", InlineKeyboardButtonParsingError),
        ("wrong file id", WrongFileIDError),
        ("group is deactivated", GroupIsDeactivatedError),
        ("photo should be uploaded as an inputfile", PhotoShouldBeUploadedAsInputFileError),
        ("stickerset_invalid", InvalidStickerSetError),
        ("too much messages to send as an album", TooMuchMessagesToSendAsAlbumError),
        ("can't demote chat creator", DemoteChatCreatorError),
        ("can't restrict self", SelfRestrictError),
        ("https url must be provided for webhook", WebhookURLMustBeHTTPSError),
        ("can't parse url", URLParsingError),
        ("webhook can be set up only on ports", BadWebhookPortError),
        ("failed to resolve host: name or service not known", UnknownWebhookHostError),
        ("can't parse entities", MessageEntitiesParsingError),
        ("wrong http url", WrongHTTPURLError),
        ("invalid file id", InvalidFileIDError)
    ):
        if message in lowered_description:
            return error_type(None, **kwargs)

    if "group chat was upgraded to a supergroup chat" in lowered_description:
        return GroupWasUpgradedToSupergroupError(
            None,
            **kwargs,
            migrate_to_chat_id=response_parameters.migrate_to_chat_id
        )

    return BadRequestError(None, **kwargs)


def _get_unauthorized_error(kwargs: dict[str, Any]) -> UnauthorizedError:
    return UnauthorizedError(None, **kwargs)


def _get_forbidden_error(kwargs: dict[str, Any]) -> ForbiddenError:
    lowered_description = kwargs["description"].lower()

    for message, error_type in (
        ("bot was blocked by the user", BotWasBlockedByUserError),
        ("user is deactivated", UserIsDeactivatedError),
        ("bot was kicked from the group chat", BotWasKickedFromGroupError),
        ("bot was kicked from the supergroup chat", BotWasKickedFromSupergroupError),
        (
            "bot can't initiate conversation with a user",
            BotCannotInitiateConversationWithUserError
        ),
        ("message_delete_forbidden", DeleteMessageForbiddenError),
        ("bot is not a member of the supergroup chat", BotIsNotSupergroupMemberError),
        ("bot is not a member of the channel chat", BotIsNotChannelMemberError),
        ("bot can't send messages to bots", BotCannotSendMessagesToBotsError)
    ):
        if message in lowered_description:
            return error_type(None, **kwargs)

    return ForbiddenError(None, **kwargs)


def _get_conflict_error(kwargs: dict[str, Any]) -> ConflictError:
    lowered_description = kwargs["description"].lower()

    for message, error_type in (
        ("terminated by other getupdates request", MultipleGetUpdatesError),
        (
            "can't use getupdates method while webhook is active",
            CannotUseGetUpdatesWhileWebhookIsActiveError
        )
    ):
        if message in lowered_description:
            return error_type(None, **kwargs)

    return ConflictError(None, **kwargs)


def _get_request_entity_too_large_error(kwargs: dict[str, Any]) -> RequestEntityTooLargeError:
    return RequestEntityTooLargeError(None, **kwargs)


def _get_too_many_requests_error(
    kwargs: dict[str, Any],
    response_parameters: "ResponseParameters"
) -> TooManyRequestsError:
    lowered_description = kwargs["description"].lower()

    if "retry after" in lowered_description:
        return RetryAfterError(None, **kwargs, retry_after=response_parameters.retry_after)

    return TooManyRequestsError(None, **kwargs)


def _get_internal_server_error(kwargs: dict[str, Any]) -> InternalServerError:
    lowered_description = kwargs["description"].lower()

    if "restart" in lowered_description:
        return ServerIsRestartingError(None, **kwargs)

    return InternalServerError(None, **kwargs)
