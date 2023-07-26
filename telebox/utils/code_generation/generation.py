from pathlib import Path
import re


def create_app(name: str, path: Path, full: bool) -> None:
    try:
        from jinja2 import Environment, PackageLoader
    except ImportError:
        raise ImportError(
            "To use code generation you need to install «Jinja2»:"
            "\npip install Jinja2"
        ) from None

    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name) is None:
        raise ValueError(f"«{name}» cannot be a package name.")
    elif (path / name).exists():
        raise FileExistsError(f"App directory «{name}» already exists.")

    environment = Environment(
        trim_blocks=True,
        keep_trailing_newline=True,
        loader=PackageLoader("telebox.utils.code_generation"),
        auto_reload=False
    )
    app_path = _create_package(name, path)
    _create_handlers_package(app_path, environment, name)
    _create_utils_package(app_path, environment, name)

    if full:
        _create_filters_package(app_path)
        _create_middlewares_package(app_path, environment)
        _create_markups_package(app_path, environment)
        _create_states_package(app_path, environment, name)

    _create_module(
        name="env",
        path=app_path,
        content=_get_code(
            "env.jinja",
            environment,
            app_name=name,
            full=full
        )
    )
    _create_module(
        name="config",
        path=app_path,
        content=_get_code("config.jinja", environment)
    )
    _create_module(
        name="__main__",
        path=app_path,
        content=_get_code(
            "__main__.jinja",
            environment,
            app_name=name,
            full=full
        )
    )


def _create_handlers_package(path: Path, environment, app_name: str) -> None:
    handlers_path = _create_package("handlers", path)
    sub_handlers_path = _create_package("handlers", handlers_path)
    _create_module(
        name="start",
        path=sub_handlers_path,
        content=_get_code(
            "handlers/handlers/start.jinja",
            environment,
            app_name=app_name
        )
    )
    _create_module(
        name="handler",
        path=handlers_path,
        content=_get_code(
            "handlers/handler.jinja",
            environment,
            app_name=app_name
        )
    )
    _create_module(
        name="group",
        path=handlers_path,
        content=_get_code(
            "handlers/group.jinja",
            environment,
            app_name=app_name
        )
    )
    _create_module(
        name="setting",
        path=handlers_path,
        content=_get_code(
            "handlers/setting.jinja",
            environment,
            app_name=app_name
        )
    )


def _create_utils_package(path: Path, environment, app_name: str) -> None:
    utils_path = _create_package("utils", path)
    _create_module(
        name="bot",
        path=utils_path,
        content=_get_code("utils/bot.jinja", environment)
    )
    _create_module(
        name="logging",
        path=utils_path,
        content=_get_code(
            "utils/logging.jinja",
            environment,
            app_name=app_name
        )
    )


def _create_filters_package(path: Path) -> None:
    filters_path = _create_package("filters", path)
    _create_package("factories", filters_path)
    _create_package("filters", filters_path)


def _create_middlewares_package(path: Path, environment) -> None:
    middlewares_path = _create_package("middlewares", path)
    _create_package("middlewares", middlewares_path)
    _create_module(
        "setting",
        middlewares_path,
        content=_get_code("middlewares/setting.jinja", environment)
    )


def _create_markups_package(path: Path, environment) -> None:
    markups_path = _create_package("markups", path)
    _create_module(
        "reply",
        markups_path,
        content=_get_code("markups/reply.jinja", environment)
    )
    _create_module(
        "inline",
        markups_path,
        content=_get_code("markups/inline.jinja", environment)
    )


def _create_states_package(path: Path, environment, app_name: str) -> None:
    states_path = _create_package("states", path)
    sub_states_path = _create_package("states", states_path)
    _create_module(
        name="initial",
        path=sub_states_path,
        content=_get_code(
            "states/states/initial.jinja",
            environment,
            app_name=app_name
        )
    )
    _create_module(
        name="state",
        path=states_path,
        content=_get_code(
            "states/state.jinja",
            environment,
            app_name=app_name
        )
    )
    _create_module(
        name="group",
        path=states_path,
        content=_get_code(
            "states/group.jinja",
            environment,
            app_name=app_name
        )
    )
    _create_module(
        name="storage",
        path=states_path,
        content=_get_code("states/storage.jinja", environment)
    )


def _get_code(template_path: str, environment, /, **fields) -> str:
    return environment.get_template(template_path).render(**fields)


def _create_package(name: str, path: Path) -> Path:
    package_path = path / name
    package_path.mkdir()
    _create_module("__init__", package_path)

    return package_path


def _create_module(name: str, path: Path, content: str = "") -> None:
    module_path = path / f"{name}.py"

    with module_path.open("w", encoding="UTF-8") as file:
        file.write(content)
