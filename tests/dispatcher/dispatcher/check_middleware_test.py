from unittest.mock import Mock

from telebox import Dispatcher, TelegramBot, Middleware


def test(token: str) -> None:
    bot = TelegramBot(session=Mock(), token=token)
    dispatcher = Dispatcher(bot)
    middleware = Middleware()

    assert dispatcher.check_middleware(middleware) is False

    dispatcher.add_middleware(middleware)

    assert dispatcher.check_middleware(middleware) is True
