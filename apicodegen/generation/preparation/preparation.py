import re
import keyword
from typing import Optional

from getpycode import ImportBuilder  # noqa

from apicodegen.documentation.types import Type, Method, Field, Parameter
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
CONTEXT_PARAMETERS = [
    "chat_id",
    "user_id",
    "message_thread_id",
    "business_connection_id",
    "sender_chat_id",
    "message_id",
    "callback_query_id",
    "inline_query_id",
    "shipping_query_id",
    "pre_checkout_query_id"
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
    parameters.sort(key=_get_parameter_priority)

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
        import_builder.add("typing", "Union")

        for i in prepared_type.types:
            import_builder.add(f"telebox.bot.types.{get_snake_case_string(i)}", i)

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


def _get_parameter_priority(parameter: PreparedParameter) -> int:
    if not parameter.is_optional and not parameter.is_context:
        return 0
    elif parameter.is_context:
        return 1
    elif parameter.is_optional:
        return 2
    else:
        return 3


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
            import_builder.add(module_path, entity)
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
            import_builder.add(module_path, entity)
    else:
        additional_code = ""

    additional_code += TYPE_ADDITIONAL_CODES.get(type_.name, "")

    if additional_code:
        type_.additional_code = additional_code

        for module_path, entity in TYPE_ADDITIONAL_CODE_IMPORTS.get(type_.name, ()):
            import_builder.add(module_path, entity)


def _prepare_field(
    field: Field,
    type_names: set[str],
    import_builder: ImportBuilder
) -> PreparedField:
    is_optional = _check_field_is_optional(field)

    return PreparedField(
        name=_get_safe_name(field.name),
        types=field.types,
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
    is_context = parameter.name in CONTEXT_PARAMETERS

    return PreparedParameter(
        name=_get_safe_name(parameter.name),
        type_hint=_prepare_entity_type_hint(
            name=parameter.name,
            types=parameter.types,
            array_nesting=parameter.array_nesting,
            type_names=type_names,
            import_builder=import_builder,
            is_optional=parameter.is_optional,
            is_context=is_context,
            description=parameter.description
        ),
        description=_get_description(parameter.description),
        is_optional=parameter.is_optional,
        is_context=is_context
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
    is_context: bool = False,
    name: Optional[str] = None,
    description: Optional[str] = None,
    value: Optional[str] = None
) -> str:
    hint_types = []

    for i in types:
        if name and _check_entity_timestamp_type(name=name, type_=i):
            hint_types.append("datetime")
            import_builder.add("datetime", "datetime")
        elif i == "String":
            if value is not None:
                hint_types.append(f'Literal["{value}"]')
                import_builder.add("typing", "Literal")
            elif description and ("attach://" in description.lower()):
                hint_types.append("str")
                hint_types.append("InputFile")
                import_builder.add("telebox.bot.types.input_file", "InputFile")
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
            import_builder.add("telebox.bot.types.input_file", "InputFile")
        elif i == "True":
            hint_types.append("Literal[True]")
            import_builder.add("typing", "Literal")
        elif i in type_names:
            hint_types.append(i)
            import_builder.add(f"telebox.bot.types.{get_snake_case_string(i)}", i)
        else:
            raise ValueError(f"Unknown type {i!r} (description={description!r})!")

    if is_context:
        hint_types.append("Context")
        import_builder.add("telebox.dispatcher.context", "Context")

    if len(hint_types) > 1:
        hint = f"Union[{', '.join(hint_types)}]"
        import_builder.add("typing", "Union")
    else:
        hint = hint_types[0]

    for _ in range(array_nesting):
        hint = f"list[{hint}]"

    if is_optional:
        optional_types = ["None"]

        if not is_context:
            optional_types.append("Unset")
            import_builder.add("telebox.utils.unset", "Unset")

        if len(hint_types) > 1 and not array_nesting:
            hint = f"Union[{', '.join(hint_types)}, {', '.join(optional_types)}]"
        else:
            hint = f"Union[{hint}, {', '.join(optional_types)}]"

        import_builder.add("typing", "Union")

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
