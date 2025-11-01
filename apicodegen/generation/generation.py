from pathlib import Path
import re

from getpycode import CodeGenerator, Package, Module  # noqa
from jinja2 import FileSystemLoader  # noqa

from apicodegen.documentation.documentation import Documentation
from apicodegen.generation.import_builder import ImportBuilder
from apicodegen.generation.preparation.types import PreparedType, PreparedMethod
from apicodegen.generation.preparation.preparation import (
    prepare_type,
    prepare_method,
    get_update_types,
    get_snake_case_string,
    MESSAGE_TYPES
)


telebox_dir = Path(__file__).parent.parent.parent / "telebox"
template_dir = Path(__file__).parent / "templates"
types_dir = telebox_dir / "bot" / "types"
bot_path = telebox_dir / "bot" / "bot.py"
message_type_path = telebox_dir / "bot" / "enums" / "message_type.py"
update_type_path = telebox_dir / "bot" / "enums" / "update_type.py"


def create_code(documentation: Documentation) -> None:
    bot_import_builder = ImportBuilder()
    type_import_builders = {
        i.name: ImportBuilder(
            exclude=(
                f"telebox.bot.types.{get_snake_case_string(i.name)}",
                i.name
            )
        )
        for i in documentation.types
    }

    prepared_methods = [
        prepare_method(
            method=i,
            type_names=documentation.type_names,
            import_builder=bot_import_builder
        )
        for i in documentation.methods
    ]
    prepared_types = {
        i.name: prepare_type(
            type_=i,
            type_names=documentation.type_names,
            import_builder=type_import_builders[i.name]
        )
        for i in documentation.types
    }

    generator = CodeGenerator(
        loader=FileSystemLoader(template_dir)
    )

    _create_types_package(
        generator=generator,
        import_builders=type_import_builders,
        types=prepared_types
    )
    _create_bot_module(
        generator=generator,
        import_builder=bot_import_builder,
        methods=prepared_methods
    )
    _create_message_type_module(
        generator=generator
    )
    _create_update_type_module(
        generator=generator,
        types=get_update_types(
            update=prepared_types["Update"]
        )
    )


def _create_types_package(
    generator: CodeGenerator,
    import_builders: dict[str, ImportBuilder],
    types: dict[str, PreparedType]
) -> None:
    init_import_builder = ImportBuilder()

    for i in types.values():
        init_import_builder.add_import(f".{i.module_name}", i.name)

    evaluating_types = _resolve_message_type_hints(types, import_builders)
    package = Package(
        types_dir,
        "types/__init__.j2",
        local_imports=init_import_builder.get_imports().local,
        types=types,
        evaluating_types=sorted(evaluating_types)
    )

    for type_ in types:
        if type_ == "InputFile":
            continue

        if not types[type_].is_union:
            import_builders[type_].add_import("attrs", "define")
            import_builders[type_].add_import("telebox.bot.type", "Type")

            if types[type_].fields:
                import_builders[type_].add_import("attrs", "field")

            if import_builders[type_].check_import("telebox.utils.unset", "Unset"):
                import_builders[type_].add_import("telebox.bot.utils.types", "default_factory")

        imports = import_builders[type_].get_imports()
        package.add_module(
            f"{types[type_].module_name}.py",
            "types/type.j2",
            standard_imports=imports.standard,
            third_party_imports=imports.third_party,
            local_imports=imports.local,
            type_checking_imports=imports.type_checking,
            type_=types[type_]
        )

    generator.create_package(package)


def _create_bot_module(
    generator: CodeGenerator,
    import_builder: ImportBuilder,
    methods: list[PreparedMethod]
) -> None:
    import_builder.add_import("telebox.bot.utils.converter", "Converter")

    for i in ("Session", "API_URL"):
        import_builder.add_import("telebox.bot.session", i)

    # For `download_file` method
    for i in ("Optional", "BinaryIO"):
        import_builder.add_import("typing", i)

    # For default values
    import_builder.add_import("telebox.utils.unset", "UNSET")

    # For `profile` property
    import_builder.add_import("telebox.bot.errors", "BotError")

    imports = import_builder.get_imports()
    generator.create_module(
        Module(
            bot_path,
            "bot.j2",
            standard_imports=imports.standard,
            third_party_imports=imports.third_party,
            local_imports=imports.local,
            methods=methods
        )
    )


def _create_message_type_module(
    generator: CodeGenerator
) -> None:
    generator.create_module(
        Module(
            message_type_path,
            "enums/type.j2",
            class_="MessageType",
            types=MESSAGE_TYPES
        )
    )


def _create_update_type_module(
    generator: CodeGenerator,
    types: list[str]
) -> None:
    generator.create_module(
        Module(
            update_type_path,
            "enums/type.j2",
            class_="UpdateType",
            types=types
        )
    )


def _resolve_message_type_hints(
    types: dict[str, PreparedType],
    import_builders: dict[str, ImportBuilder]
) -> set[str]:
    message = types["Message"]
    message_import_builder = import_builders["Message"]
    evaluating_types = {"Message"}

    for i in message.fields:
        i.type_hint = re.sub(r"\bMessage\b", '"Message"', i.type_hint)

    for type_ in types:
        if not import_builders[type_].check_import("telebox.bot.types.message", "Message"):
            continue

        for i in message.fields:
            if not message_import_builder.check_import(
                f"telebox.bot.types.{types[type_].module_name}",
                type_
            ):
                continue

            i.type_hint = re.sub(rf"\b{type_}\b", f'"{type_}"', i.type_hint)
            evaluating_types.add(type_)
            message_import_builder.add_import(
                f"telebox.bot.types.{types[type_].module_name}",
                type_,
                for_type_checking=True
            )

    return evaluating_types
