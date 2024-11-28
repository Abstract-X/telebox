from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from telebox.bot.consts import menu_button_types
from telebox.bot.types.types.bot_command_scope import BotCommandScope
from telebox.bot.types.types.bot_command import BotCommand
from telebox.bot.types.types.input_file import InputFile
from telebox.bot.types.types.menu_button_web_app import MenuButtonWebApp
if TYPE_CHECKING:
    from telebox.bot.bot import Bot


@dataclass
class Webhook:
    url: str
    certificate: Optional[InputFile] = None
    ip_address: Optional[str] = None
    max_connections: Optional[int] = None
    allowed_updates: Optional[list[str]] = None
    drop_pending_updates: Optional[bool] = None
    secret_token: Optional[str] = None


def set_up_bot(
    bot: "Bot",
    *,
    commands: Optional[list[tuple[BotCommandScope, list[BotCommand]]]] = None,
    description: Optional[str] = None,
    short_description: Optional[str] = None,
    menu_button: Optional[MenuButtonWebApp] = None,
    webhook: Optional[Webhook] = None
) -> None:
    commands = commands or []

    if commands and not bot.get_my_commands():
        for scope, commands_ in commands:
            bot.set_my_commands(commands=commands_, scope=scope)

    if (description is not None) and (not bot.get_my_description().description):
        bot.set_my_description(description=description)

    if (
        (short_description is not None)
        and (not bot.get_my_short_description().short_description)
    ):
        bot.set_my_short_description(short_description=short_description)

    if (
        (menu_button is not None)
        and (bot.get_chat_menu_button().type == menu_button_types.COMMANDS)
    ):
        bot.set_chat_menu_button(menu_button=menu_button)

    if webhook is not None:
        webhook_info = bot.get_webhook_info()

        if not webhook_info.url:
            bot.set_webhook(
                url=webhook.url,
                certificate=webhook.certificate,
                ip_address=webhook.ip_address,
                max_connections=webhook.max_connections,
                allowed_updates=webhook.allowed_updates,
                drop_pending_updates=webhook.drop_pending_updates,
                secret_token=webhook.secret_token
            )
