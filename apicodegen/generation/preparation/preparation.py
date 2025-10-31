import re
import keyword
from typing import Optional

from apicodegen.documentation.types import Type, Method, Field, Parameter
from apicodegen.generation.import_builder import ImportBuilder
from apicodegen.generation.preparation.additional_codes import (
    TYPE_ADDITIONAL_CODES,
    TYPE_ADDITIONAL_CODE_IMPORTS
)
from apicodegen.generation.preparation.types import (
    PreparedType,
    PreparedParameter,
    PreparedField,
    PreparedMethod
)


snake_case_replacing_patterns = (
    re.compile(r"(.)([A-Z][a-z]+)"),
    re.compile(r"([a-z0-9])([A-Z])")
)
MESSAGE_TYPES = [
    "TEXT",
    "ANIMATION",
    "AUDIO",
    "DOCUMENT",
    "PAID_MEDIA",
    "PHOTO",
    "STICKER",
    "STORY",
    "VIDEO",
    "VIDEO_NOTE",
    "VOICE",
    "CHECKLIST",
    "CONTACT",
    "DICE",
    "GAME",
    "POLL",
    "VENUE",
    "LOCATION",
    "NEW_CHAT_MEMBERS",
    "LEFT_CHAT_MEMBER",
    "NEW_CHAT_TITLE",
    "NEW_CHAT_PHOTO",
    "DELETE_CHAT_PHOTO",
    "GROUP_CHAT_CREATED",
    "SUPERGROUP_CHAT_CREATED",
    "CHANNEL_CHAT_CREATED",
    "MESSAGE_AUTO_DELETE_TIMER_CHANGED",
    "MIGRATE_TO_CHAT_ID",
    "MIGRATE_FROM_CHAT_ID",
    "PINNED_MESSAGE",
    "INVOICE",
    "SUCCESSFUL_PAYMENT",
    "REFUNDED_PAYMENT",
    "USERS_SHARED",
    "CHAT_SHARED",
    "GIFT",
    "UNIQUE_GIFT",
    "CONNECTED_WEBSITE",
    "WRITE_ACCESS_ALLOWED",
    "PASSPORT_DATA",
    "PROXIMITY_ALERT_TRIGGERED",
    "BOOST_ADDED",
    "CHAT_BACKGROUND_SET",
    "CHECKLIST_TASKS_DONE",
    "CHECKLIST_TASKS_ADDED",
    "DIRECT_MESSAGE_PRICE_CHANGED",
    "FORUM_TOPIC_CREATED",
    "FORUM_TOPIC_EDITED",
    "FORUM_TOPIC_CLOSED",
    "FORUM_TOPIC_REOPENED",
    "GENERAL_FORUM_TOPIC_HIDDEN",
    "GENERAL_FORUM_TOPIC_UNHIDDEN",
    "GIVEAWAY_CREATED",
    "GIVEAWAY",
    "GIVEAWAY_WINNERS",
    "GIVEAWAY_COMPLETED",
    "PAID_MESSAGE_PRICE_CHANGED",
    "SUGGESTED_POST_APPROVED",
    "SUGGESTED_POST_APPROVAL_FAILED",
    "SUGGESTED_POST_DECLINED",
    "SUGGESTED_POST_PAID",
    "SUGGESTED_POST_REFUNDED",
    "VIDEO_CHAT_SCHEDULED",
    "VIDEO_CHAT_STARTED",
    "VIDEO_CHAT_ENDED",
    "VIDEO_CHAT_PARTICIPANTS_INVITED",
    "WEB_APP_DATA"
]


def prepare_method(
    method: Method,
    type_names: set[str],
    import_builder: ImportBuilder
) -> PreparedMethod:
    parameters = [
        _prepare_parameter(
            parameter=i,
            type_names=type_names,
            import_builder=import_builder
        )
        for i in method.parameters
    ]
    parameters.sort(key=lambda parameter_: parameter_.is_optional)

    result_contains_object = any(i in type_names for i in method.result_types)

    if result_contains_object:
        result_object_type = next(i for i in method.result_types if i in type_names)
    else:
        result_object_type = None

    prepared_method = PreparedMethod(
        name=method.name,
        function_name=get_snake_case_string(method.name),
        description=_get_description(method.description),
        parameters=parameters,
        result_type_hint=_prepare_entity_type_hint(
            types=method.result_types,
            array_nesting=method.result_array_nesting,
            type_names=type_names,
            import_builder=import_builder
        ),
        result_array_nesting=method.result_array_nesting,
        result_contains_object=result_contains_object,
        result_is_object=(
            len(method.result_types) == 1
            and method.result_types[0] in type_names
        ),
        result_object_type=result_object_type
    )
    _set_prepared_method_value_codes(prepared_method)

    return prepared_method


def prepare_type(
    type_: Type,
    type_names: set[str],
    import_builder: ImportBuilder
) -> PreparedType:
    fields = [
        _prepare_field(
            field=i,
            type_names=type_names,
            import_builder=import_builder
        )
        for i in type_.fields
    ]
    fields.sort(key=lambda field_: (1 if field_.value else 0, field_.is_optional))

    prepared_type = PreparedType(
        name=type_.name,
        module_name=get_snake_case_string(type_.name),
        description=_get_description(type_.description),
        fields=fields,
        types=type_.types,
        is_union=type_.is_union
    )
    _set_prepared_type_additional_code(prepared_type, import_builder)

    if prepared_type.is_union:
        import_builder.add_import("typing", "Union")

        for i in prepared_type.types:
            import_builder.add_import(f"telebox.bot.types.{get_snake_case_string(i)}", i)

    return prepared_type


def get_snake_case_string(string: str) -> str:
    for i in snake_case_replacing_patterns:
        string = i.sub(r'\1_\2', string)

    return string.lower()


def get_update_types(update: PreparedType) -> list[str]:
    types = []

    for i in update.fields:
        if not i.is_optional:
            continue

        types.append(
            i.name.upper()
        )

    return types


def _set_prepared_type_additional_code(
    type_: PreparedType,
    import_builder: ImportBuilder
) -> None:
    if type_.name == "Message":
        additional_code = (
            "type: Optional[MessageType] = field(init=False)"
            "\n\n    def __attrs_post_init__(self) -> None:"
        )

        for i in MESSAGE_TYPES:
            additional_code += (
                f"\n        {'el' if i != MESSAGE_TYPES[0] else ''}if self.{i.lower()}:"
                f"\n            self.type = MessageType.{i}"
            )

        additional_code += (
            "\n        else:"
            "\n            self.type = None\n"
        )

        for module_path, entity in (
            ("typing", "Optional"),
            ("attrs", "field"),
            ("telebox.bot.enums.message_type", "MessageType")
        ):
            import_builder.add_import(module_path, entity)
    elif type_.name == "Update":
        additional_code = (
            "type: Optional[UpdateType] = field(init=False)"
            "\n    content: Any = field(init=False)"
            "\n\n    def __attrs_post_init__(self) -> None:"
        )
        update_types = get_update_types(type_)

        for i in update_types:
            additional_code += (
                f"\n        {'el' if i != update_types[0] else ''}if self.{i.lower()}:"
                f"\n            self.type = UpdateType.{i}"
                f"\n            self.content = self.{i.lower()}"
            )

        additional_code += (
            "\n        else:"
            "\n            self.type = None"
            "\n            self.content = None"
        )

        for module_path, entity in (
            ("typing", "Optional"),
            ("typing", "Any"),
            ("attrs", "field"),
            ("telebox.bot.enums.update_type", "UpdateType")
        ):
            import_builder.add_import(module_path, entity)
    else:
        additional_code = ""

    additional_code += TYPE_ADDITIONAL_CODES.get(type_.name, "")

    if additional_code:
        type_.additional_code = additional_code

        for module_path, entity in TYPE_ADDITIONAL_CODE_IMPORTS.get(type_.name, ()):
            import_builder.add_import(module_path, entity)


def _set_prepared_method_value_codes(method: PreparedMethod) -> None:
    for parameter in method.parameters:
        if parameter.name.endswith("parse_mode"):
            prefix = parameter.name.removesuffix("parse_mode")

            if prefix:
                entities_parameter_names = (f"{prefix}entities",)
            else:
                entities_parameter_names = ("entities", "caption_entities")

            for i in method.parameters:
                if i.name in entities_parameter_names:
                    entities_parameter = i
                    break
            else:
                raise ValueError(f"No entities parameter for {prefix!r} prefix!")

            parameter.value_code = f"self._get_parse_mode({parameter.name}, {entities_parameter.name})"
        elif parameter.name == "link_preview_options":
            parameter.value_code = f"self._get_link_preview_options({parameter.name})"
        elif parameter.name == "disable_notification":
            parameter.value_code = f"self._get_disable_notification({parameter.name})"
        elif parameter.name == "protect_content":
            parameter.value_code = f"self._get_protect_content({parameter.name})"
        else:
            parameter.value_code = parameter.name


def _prepare_field(
    field: Field,
    type_names: set[str],
    import_builder: ImportBuilder
) -> PreparedField:
    is_optional = _check_field_is_optional(field)

    return PreparedField(
        name=_get_safe_name(field.name),
        type_hint=_prepare_entity_type_hint(
            name=field.name,
            types=field.types,
            array_nesting=field.array_nesting,
            type_names=type_names,
            import_builder=import_builder,
            is_optional=is_optional,
            description=field.description,
            value=field.value
        ),
        description=_get_description(field.description),
        is_optional=is_optional,
        value=field.value
    )


def _prepare_parameter(
    parameter: Parameter,
    type_names: set[str],
    import_builder: ImportBuilder
) -> PreparedParameter:
    return PreparedParameter(
        name=_get_safe_name(parameter.name),
        type_hint=_prepare_entity_type_hint(
            name=parameter.name,
            types=parameter.types,
            array_nesting=parameter.array_nesting,
            type_names=type_names,
            import_builder=import_builder,
            is_optional=parameter.is_optional,
            description=parameter.description
        ),
        description=_get_description(parameter.description),
        is_optional=parameter.is_optional
    )


def _check_field_is_optional(field: Field) -> bool:
    for i in field.types:
        if (
            _check_entity_timestamp_type(
                name=field.name,
                type_=i
            )
            and ("if 0, then" in field.description.lower())
        ):
            return True

    return field.is_optional


# TODO: Prepare description
def _get_description(description: str) -> str:
    return description


def _prepare_entity_type_hint(
    types: list[str],
    array_nesting: int,
    type_names: set[str],
    import_builder: ImportBuilder,
    is_optional: bool = False,
    name: Optional[str] = None,
    description: Optional[str] = None,
    value: Optional[str] = None
) -> str:
    hint_types = []

    for i in types:
        if name and _check_entity_timestamp_type(name=name, type_=i):
            hint_types.append("datetime")
            import_builder.add_import("datetime", "datetime")
        elif i == "String":
            if value is not None:
                hint_types.append(f'Literal["{value}"]')
                import_builder.add_import("typing", "Literal")
            elif description and ("attach://" in description.lower()):
                hint_types.append("str")
                hint_types.append("InputFile")
                import_builder.add_import("telebox.bot.types.input_file", "InputFile")
            else:
                hint_types.append("str")
        elif i == "Integer":
            hint_types.append("int")
        elif i == "Boolean":
            hint_types.append("bool")
        elif i == "Float":
            hint_types.append("float")
        elif i == "InputFile":
            hint_types.append("InputFile")
            import_builder.add_import("telebox.bot.types.input_file", "InputFile")
        elif i == "True":
            hint_types.append("Literal[True]")
            import_builder.add_import("typing", "Literal")
        elif i in type_names:
            hint_types.append(i)
            import_builder.add_import(f"telebox.bot.types.{get_snake_case_string(i)}", i)
        else:
            raise ValueError(f"Unknown type {i!r} (description={description!r})!")

    if len(hint_types) > 1:
        hint = f"Union[{', '.join(hint_types)}]"
        import_builder.add_import("typing", "Union")
    else:
        hint = hint_types[0]

    for _ in range(array_nesting):
        hint = f"list[{hint}]"

    if is_optional:
        if len(hint_types) > 1 and not array_nesting:
            hint = f"Union[{', '.join(hint_types)}, None, Unset]"
        else:
            hint = f"Union[{hint}, None, Unset]"

        import_builder.add_import("telebox.utils.unset", "Unset")
        import_builder.add_import("typing", "Union")

    return hint


def _check_entity_timestamp_type(name: str, type_: str) -> bool:
    return (
        (type_ == "Integer")
        and (
            (name == "date")
            or name.endswith("_date")
        )
    )


def _get_safe_name(name: str) -> str:
    if keyword.iskeyword(name):
        name = f"{name}_"

    return name
