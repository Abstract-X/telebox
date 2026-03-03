from typing import Optional, Any
from http import HTTPStatus

from telebox.errors import TeleboxError
from telebox.bot.types.response_parameters import ResponseParameters


class BotError(TeleboxError):
    pass


class RequestError(BotError):
    """Telegram Bot API request error."""

    def __init__(
        self,
        message: str = "",
        *,
        method: str,
        parameters: dict[str, Any],
        status_code: int,
        description: str
    ):
        super().__init__(message=message)
        self.method = method
        self.parameters = parameters
        self.status_code = status_code
        self.description = description


class BadRequestError(RequestError):
    """Error with 400 status code."""


class ChatNotFoundError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: chat not found',
        'error_code': 400,
        'ok': False
    }
    """


class UserNotFoundError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: user not found',
        'error_code': 400,
        'ok': False
    }
    """


class MessageIsNotModifiedError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: message is not modified',
        'error_code': 400,
        'ok': False
    }
    """


class ChatDescriptionIsNotModifiedError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: chat description is not modified',
        'error_code': 400,
        'ok': False
    }
    """


class MessageToForwardNotFoundError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: message to forward not found',
        'error_code': 400,
        'ok': False
    }
    """


class MessageToDeleteNotFoundError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: message to delete not found',
        'error_code': 400,
        'ok': False
    }
    """


class MessageToEditNotFoundError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: message to edit not found',
        'error_code': 400,
        'ok': False
    }
    """


class PollAlreadyClosedError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: poll has already been closed',
        'error_code': 400,
        'ok': False
    }
    """


class PollMustHaveMoreOptionsError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: poll must have at least 2 option',
        'error_code': 400,
        'ok': False
    }
    """


class PollCannotHaveMoreOptionsError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: poll can't have more than 10 options',
        'error_code': 400,
        'ok': False
    }
    """


class PollOptionsMustBeNonEmptyError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: poll options must be non-empty',
        'error_code': 400,
        'ok': False
    }
    """


class PollQuestionMustBeNonEmptyError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: poll question must be non-empty',
        'error_code': 400,
        'ok': False
    }
    """


class PollOptionsLengthIsTooLongError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: poll options length must not exceed 100',
        'error_code': 400,
        'ok': False
    }
    """


class PollQuestionLengthIsTooLongError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: poll question length must not exceed 255',
        'error_code': 400,
        'ok': False
    }
    """


class MessageWithPollToStopNotFoundError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: message with poll to stop not found',
        'error_code': 400,
        'ok': False
    }
    """


class MessageIsNotPollError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: message is not a poll',
        'error_code': 400,
        'ok': False
    }
    """


class InvalidMessageIDError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: MESSAGE_ID_INVALID',
        'error_code': 400,
        'ok': False
    }
    """


class PrivateChannelError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: CHANNEL_PRIVATE',
        'error_code': 400,
        'ok': False
    }
    """


class WriteToChatForbiddenError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: CHAT_WRITE_FORBIDDEN',
        'error_code': 400,
        'ok': False
    }
    """


class MessageToPinNotFoundError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: message to pin not found',
        'error_code': 400,
        'ok': False
    }
    """


class NoRightsToManagePinnedMessagesError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: not enough rights to manage pinned messages in the chat',
        'error_code': 400,
        'ok': False
    }
    """


class NoRightsToExportChatInviteLinkError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: not enough rights to export chat invite link',
        'error_code': 400,
        'ok': False
    }
    """


class NoRightsToRestrictUnrestrictChatMemberError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: not enough rights to restrict/unrestrict chat member',
        'error_code': 400,
        'ok': False
    }
    """


class NoRightsToSendMessageError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: have no rights to send a message',
        'error_code': 400,
        'ok': False
    }
    """


class RepliedMessageNotFoundError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: replied message not found',
        'error_code': 400,
        'ok': False
    }
    """


class MessageIDIsNotSpecifiedError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: message identifier is not specified',
        'error_code': 400,
        'ok': False
    }
    """


class MessageTextIsEmptyError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: message text is empty',
        'error_code': 400,
        'ok': False
    }
    """


class MessageCannotBeEditedError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: message can't be edited',
        'error_code': 400,
        'ok': False
    }
    """


class MessageCannotBeDeletedError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: message can't be deleted',
        'error_code': 400,
        'ok': False
    }
    """


class GroupWasUpgradedToSupergroupError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: group chat was upgraded to a supergroup chat',
        'error_code': 400,
        'ok': False,
        'parameters': {
            'migrate_to_chat_id': -100123456789
        }
    }
    """

    def __init__(
        self,
        message: str = "", *,
        method: str,
        parameters: dict[str, Any],
        status_code: int,
        description: str,
        migrate_to_chat_id: int
    ):
        super().__init__(
            message=message,
            method=method,
            parameters=parameters,
            status_code=status_code,
            description=description
        )
        self.migrate_to_chat_id = migrate_to_chat_id


class MessageIsTooLongError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: message is too long',
        'error_code': 400,
        'ok': False
    }
    """


class QueryIsTooOldOrInvalidIDError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: query is too old and response timeout expired or query ID is invalid',
        'error_code': 400,
        'ok': False
    }
    """


class InvalidButtonURLError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: BUTTON_URL_INVALID',
        'error_code': 400,
        'ok': False
    }
    """


class InvalidButtonDataError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: BUTTON_DATA_INVALID',
        'error_code': 400,
        'ok': False
    }
    """


class InlineKeyboardButtonParsingError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: can't parse inline keyboard button: Text buttons are unallowed in the inline keyboard',
        'error_code': 400,
        'ok': False
    }
    """


class WrongFileIDError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: wrong file id',
        'error_code': 400,
        'ok': False
    }
    """


class GroupIsDeactivatedError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: group is deactivated',
        'error_code': 400,
        'ok': False
    }
    """


class PhotoShouldBeUploadedAsInputFileError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: photo should be uploaded as an InputFile',
        'error_code': 400,
        'ok': False
    }
    """


class InvalidStickerSetError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: STICKERSET_INVALID',
        'error_code': 400,
        'ok': False
    }
    """


class TooMuchMessagesToSendAsAlbumError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: too much messages to send as an album',
        'error_code': 400,
        'ok': False
    }
    """


class DemoteChatCreatorError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: can't demote chat creator',
        'error_code': 400,
        'ok': False
    }
    """


class SelfRestrictError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: can't restrict self',
        'error_code': 400,
        'ok': False
    }
    """


class WebhookURLMustBeHTTPSError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: bad webhook: HTTPS url must be provided for webhook',
        'error_code': 400,
        'ok': False
    }
    """


class URLParsingError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: can't parse URL',
        'error_code': 400,
        'ok': False
    }
    """


class BadWebhookPortError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: bad webhook: Webhook can be set up only on ports 80, 88, 443 or 8443',
        'error_code': 400,
        'ok': False
    }
    """


class UnknownWebhookHostError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: bad webhook: Failed to resolve host: Name or service not known',
        'error_code': 400,
        'ok': False
    }
    """


class MessageEntitiesParsingError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: can't parse entities',
        'error_code': 400,
        'ok': False
    }
    """


class WrongHTTPURLError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: wrong HTTP URL',
        'error_code': 400,
        'ok': False
    }
    """


class InvalidFileIDError(BadRequestError):
    """Error for this response:
    {
        'description': 'Bad Request: invalid file id',
        'error_code': 400,
        'ok': False
    }
    """


class UnauthorizedError(RequestError):
    """Error with 401 status code."""


class ForbiddenError(RequestError):
    """Error with 403 status code."""


class NotFoundError(RequestError):
    """Error with 404 status code."""


class BotWasBlockedByUserError(ForbiddenError):
    """Error for this response:
    {
        'description': 'Forbidden: bot was blocked by the user',
        'error_code': 403,
        'ok': False
    }
    """


class UserIsDeactivatedError(ForbiddenError):
    """Error for this response:
    {
        'description': 'Forbidden: user is deactivated',
        'error_code': 403,
        'ok': False
    }
    """


class BotWasKickedFromGroupError(ForbiddenError):
    """Error for this response:
    {
        'description': 'Forbidden: bot was kicked from the group chat',
        'error_code': 403,
        'ok': False
    }
    """


class BotWasKickedFromSupergroupError(ForbiddenError):
    """Error for this response:
    {
        'description': 'Forbidden: bot was kicked from the supergroup chat',
        'error_code': 403,
        'ok': False
    }
    """


class BotCannotInitiateConversationWithUserError(ForbiddenError):
    """Error for this response:
    {
        'description': 'Forbidden: bot can't initiate conversation with a user',
        'error_code': 403,
        'ok': False
    }
    """


class DeleteMessageForbiddenError(ForbiddenError):
    """Error for this response:
    {
        'description': 'Forbidden: MESSAGE_DELETE_FORBIDDEN',
        'error_code': 403,
        'ok': False
    }
    """


class BotIsNotSupergroupMemberError(ForbiddenError):
    """Error for this response:
    {
        'description': 'Forbidden: bot is not a member of the supergroup chat',
        'error_code': 403,
        'ok': False
    }
    """


class BotIsNotChannelMemberError(ForbiddenError):
    """Error for this response:
    {
        'description': 'Forbidden: bot is not a member of the channel chat',
        'error_code': 403,
        'ok': False
    }
    """


class BotCannotSendMessagesToBotsError(ForbiddenError):
    """Error for this response:
    {
        'description': 'Forbidden: bot can't send messages to bots',
        'error_code': 403,
        'ok': False
    }
    """


class ConflictError(RequestError):
    """Error with 409 status code."""


class MultipleGetUpdatesError(ConflictError):
    """Error for this response:
    {
        'description': 'Conflict: terminated by other getUpdates request; make sure that only one bot instance is running',
        'error_code': 409,
        'ok': False
    }
    """


class CannotUseGetUpdatesWhileWebhookIsActiveError(ConflictError):
    """Error for this response:
    {
        'description': 'Conflict: can't use getUpdates method while webhook is active; use deleteWebhook to delete the webhook first',
        'error_code': 409,
        'ok': False
    }
    """


class RequestEntityTooLargeError(RequestError):
    """Error with 413 status code."""


class TooManyRequestsError(RequestError):
    """Error with 429 status code."""


class RetryAfterError(TooManyRequestsError):
    """Error for this response:
    {
        'description': 'Too Many Requests: retry after 42',
        'error_code': 429,
        'ok': False,
        'parameters': {
            'retry_after': 42
        }
    }
    """

    def __init__(
        self,
        message: str = "",
        *,
        method: str,
        parameters: dict[str, Any],
        status_code: int,
        description: str,
        retry_after: int):
        super().__init__(
            message=message,
            method=method,
            parameters=parameters,
            status_code=status_code,
            description=description
        )
        self.retry_after = retry_after


class InternalServerError(RequestError):
    """Error with 500+ status code."""


class ServerIsRestartingError(InternalServerError):
    """Error for this response:
    {
        'description': 'Internal Server Error: restart',
        'error_code': 500,
        'ok': False
    }
    """


class BadGatewayError(InternalServerError):
    """Error for this response:
        {
            'description': 'Bad Gateway',
            'error_code': 502,
            'ok': False
        }
    """


def get_request_error(
    method: str,
    parameters: dict[str, Any],
    status_code: int,
    description: str,
    *,
    response_parameters: Optional[ResponseParameters] = None
) -> RequestError:
    kwargs = {
        "message": "\n".join((
            "Telegram Bot API request failed!",
            f"├─ Method: {method!r}",
            f"├─ Parameters: {parameters!r}",
            f"├─ Status code: {status_code!r}",
            f"└─ Description: {description!r}"
        )),
        "method": method,
        "parameters": parameters,
        "status_code": status_code,
        "description": description
    }

    if status_code == HTTPStatus.BAD_REQUEST:
        return _get_bad_request_error(kwargs, response_parameters)
    elif status_code == HTTPStatus.UNAUTHORIZED:
        return _get_unauthorized_error(kwargs)
    elif status_code == HTTPStatus.FORBIDDEN:
        return _get_forbidden_error(kwargs)
    elif status_code == HTTPStatus.NOT_FOUND:
        return _get_not_found_error(kwargs)
    elif status_code == HTTPStatus.CONFLICT:
        return _get_conflict_error(kwargs)
    elif status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
        return _get_request_entity_too_large_error(kwargs)
    elif status_code == HTTPStatus.TOO_MANY_REQUESTS:
        return _get_too_many_requests_error(kwargs, response_parameters)
    elif status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
        return _get_internal_server_error(kwargs)

    return RequestError(**kwargs)


def _get_bad_request_error(
    kwargs: dict[str, Any],
    response_parameters: ResponseParameters
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
        ("not enough rights to manage pinned messages in the chat", NoRightsToManagePinnedMessagesError),
        ("not enough rights to export chat invite link", NoRightsToExportChatInviteLinkError),
        ("not enough rights to restrict/unrestrict chat member", NoRightsToRestrictUnrestrictChatMemberError),
        ("have no rights to send a message", NoRightsToSendMessageError),
        ("replied message not found", RepliedMessageNotFoundError),
        ("message identifier is not specified", MessageIDIsNotSpecifiedError),
        ("message text is empty", MessageTextIsEmptyError),
        ("message can't be edited", MessageCannotBeEditedError),
        ("message can't be deleted", MessageCannotBeDeletedError),
        ("message is too long", MessageIsTooLongError),
        ("query is too old and response timeout expired or query id is invalid", QueryIsTooOldOrInvalidIDError),
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
            return error_type(**kwargs)

    if "group chat was upgraded to a supergroup chat" in lowered_description:
        return GroupWasUpgradedToSupergroupError(
            **kwargs,
            migrate_to_chat_id=response_parameters.migrate_to_chat_id
        )

    return BadRequestError(**kwargs)


def _get_unauthorized_error(kwargs: dict[str, Any]) -> UnauthorizedError:
    return UnauthorizedError(**kwargs)


def _get_forbidden_error(kwargs: dict[str, Any]) -> ForbiddenError:
    lowered_description = kwargs["description"].lower()

    for message, error_type in (
        ("bot was blocked by the user", BotWasBlockedByUserError),
        ("user is deactivated", UserIsDeactivatedError),
        ("bot was kicked from the group chat", BotWasKickedFromGroupError),
        ("bot was kicked from the supergroup chat", BotWasKickedFromSupergroupError),
        ("bot can't initiate conversation with a user", BotCannotInitiateConversationWithUserError),
        ("message_delete_forbidden", DeleteMessageForbiddenError),
        ("bot is not a member of the supergroup chat", BotIsNotSupergroupMemberError),
        ("bot is not a member of the channel chat", BotIsNotChannelMemberError),
        ("bot can't send messages to bots", BotCannotSendMessagesToBotsError)
    ):
        if message in lowered_description:
            return error_type(**kwargs)

    return ForbiddenError(**kwargs)


def _get_not_found_error(kwargs: dict[str, Any]) -> NotFoundError:
    return NotFoundError(**kwargs)


def _get_conflict_error(kwargs: dict[str, Any]) -> ConflictError:
    lowered_description = kwargs["description"].lower()

    for message, error_type in (
        ("terminated by other getupdates request", MultipleGetUpdatesError),
        ("can't use getupdates method while webhook is active", CannotUseGetUpdatesWhileWebhookIsActiveError)
    ):
        if message in lowered_description:
            return error_type(**kwargs)

    return ConflictError(**kwargs)


def _get_request_entity_too_large_error(kwargs: dict[str, Any]) -> RequestEntityTooLargeError:
    return RequestEntityTooLargeError(**kwargs)


def _get_too_many_requests_error(
    kwargs: dict[str, Any],
    response_parameters: ResponseParameters
) -> TooManyRequestsError:
    lowered_description = kwargs["description"].lower()

    if "retry after" in lowered_description:
        return RetryAfterError(**kwargs, retry_after=response_parameters.retry_after)

    return TooManyRequestsError(**kwargs)


def _get_internal_server_error(kwargs: dict[str, Any]) -> InternalServerError:
    lowered_description = kwargs["description"].lower()

    for message, error_type in (
        ("restart", ServerIsRestartingError),
        ("bad gateway", BadGatewayError)
    ):
        if message in lowered_description:
            return error_type(**kwargs)

    return InternalServerError(**kwargs)
