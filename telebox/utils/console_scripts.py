from argparse import ArgumentParser, Namespace
from pathlib import Path

from telebox.utils.code_generation.generation import create_app


def process_command() -> None:
    parser = ArgumentParser(prog="telebox")
    subparsers = parser.add_subparsers()
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("name")
    create_parser.add_argument("--full", action="store_true")
    create_parser.set_defaults(func=create)
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
