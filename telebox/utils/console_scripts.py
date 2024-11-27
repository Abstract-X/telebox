from argparse import ArgumentParser, Namespace
from pathlib import Path

from telebox.bot.bot import get_bot
from telebox.bot.errors import UnauthorizedError, NotFoundError
from telebox.utils.code_generation.generation import create_app


def process_command() -> None:
    parser = ArgumentParser(prog="telebox")
    subparsers = parser.add_subparsers()

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("name")
    create_parser.add_argument("--full", action="store_true")
    create_parser.set_defaults(func=create)

    info_parser = subparsers.add_parser("info")
    info_parser.add_argument("token")
    info_parser.set_defaults(func=info)

    namespace = parser.parse_args()

    try:
        namespace.func(namespace)
    except AttributeError:
        print("You didn't specify a command.")


def create(namespace: Namespace) -> None:
    app_name = namespace.name
    current_path = Path.cwd()

    try:
        create_app(
            name=app_name,
            path=current_path,
            full=namespace.full
        )
    except Exception as error:
        print(error)


def info(namespace: Namespace) -> None:
    token = namespace.token

    try:
        with get_bot(token) as bot:
            short_description = bot.get_my_short_description().short_description
            description = bot.get_my_description().description
            commands = bot.get_my_commands()
            webhook_info = bot.get_webhook_info()
    except (UnauthorizedError, NotFoundError):
        print("Invalid token!")
    else:
        if short_description:
            short_description = repr(short_description)
        else:
            short_description = "—"

        if description:
            description = repr(description)
        else:
            description = "—"

        can_join_groups = _get_yes_or_no(bot.user.can_join_groups)
        can_read_all_group_messages = _get_yes_or_no(bot.user.can_read_all_group_messages)
        supports_inline_queries = _get_yes_or_no(bot.user.supports_inline_queries)
        can_connect_to_business = _get_yes_or_no(bot.user.can_connect_to_business)

        if commands:
            commands = "\n" + "\n".join(f"      • /{i.command} - {i.description}" for i in commands)
        else:
            commands = "...................... —"

        if webhook_info.url:
            has_custom_certificate = _get_yes_or_no(webhook_info.has_custom_certificate)

            if webhook_info.allowed_updates:
                allowed_updates = "\n" + "\n".join(
                    f"            • {i}" for i in webhook_info.allowed_updates
                )
            else:
                allowed_updates = "Default"

            webhook_info_text = (
                f"\n      • URL: {webhook_info.url}"
                f"\n      • Has custom certificate: {has_custom_certificate}"
                f"\n      • Pending update count: {webhook_info.pending_update_count}"
                f"\n      • Allowed updates: {allowed_updates}"
            )
        else:
            webhook_info_text = ".................. —"

        text = (
            f"• ID: ............................ {bot.user.id}"
            f"\n• Name: .......................... {bot.user.full_name}"
            f"\n• Username: ...................... @{bot.user.username}"
            f"\n• Short description: ............. {short_description}"
            f"\n• Description: ................... {description}"
            f"\n• Can join groups: ............... {can_join_groups}"
            f"\n• Can read all group messages: ... {can_read_all_group_messages}"
            f"\n• Supports inline queries: ....... {supports_inline_queries}"
            f"\n• Can connect to business: ....... {can_connect_to_business}"
            f"\n• Commands: {commands}"
            f"\n• Webhook info: {webhook_info_text}"
        )
        print(text)


def _get_yes_or_no(value: bool) -> str:
    return "Yes" if value else "No"
