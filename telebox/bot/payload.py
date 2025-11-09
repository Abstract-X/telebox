from typing import Any, Optional, Union
from datetime import datetime
import secrets

from telebox.bot.types.input_file import InputFile
from telebox.bot.types.message_entity import MessageEntity
from telebox.bot.types.link_preview_options import LinkPreviewOptions
from telebox.bot.enums.input_file_type import InputFileType
from telebox.bot.default_parameters import DefaultParameterSet
from telebox.bot.converter import Converter, get_timestamp
from telebox.dispatcher.context import Context, get_event_value
from telebox.utils.serialization import get_serialized_data
from telebox.utils.unset import Unset, UNSET


class Payload:
    __slots__ = ("_converter", "_default_parameters", "data", "files", "opened_files")

    def __init__(
        self,
        parameters: dict[str, Any],
        converter: Converter,
        default_parameters: DefaultParameterSet
    ):
        self._converter = converter
        self._default_parameters = default_parameters
        self.data = {}
        self.files = {}
        self.opened_files = []
        self._initialize(parameters)

    def _initialize(self, parameters: dict[str, Any]) -> None:
        for parameter, value in parameters.items():
            if isinstance(value, Context):
                value = get_event_value(parameter, optional=value.optional)
            elif parameter.endswith("parse_mode"):
                prefix = parameter.removesuffix("parse_mode")

                if prefix:
                    entities_parameter_names = (f"{prefix}entities",)
                else:
                    entities_parameter_names = ("entities", "caption_entities")

                for i in parameters:
                    if i in entities_parameter_names:
                        entities_parameter = i
                        break
                else:
                    raise ValueError(f"No entities parameter for {prefix!r} prefix!")

                value = self._get_parse_mode(
                    parse_mode=value,
                    entities=parameters[entities_parameter]
                )
            elif parameter == "link_preview_options":
                value = self._get_link_preview_options(value)
            elif parameter == "disable_notification":
                value = self._get_disable_notification(value)
            elif parameter == "protect_content":
                value = self._get_protect_content(value)

            if value is None or value is UNSET:
                continue

            if isinstance(value, InputFile):
                self._set_file(value, parameter=parameter)
            else:
                value = self._prepare_value(value)

                if isinstance(value, (dict, list)):
                    value = get_serialized_data(value)

                self.data[parameter] = str(value)

    def _prepare_value(self, value: Any) -> Any:
        if isinstance(value, InputFile):
            return self._set_file(value)
        elif self._converter.check_class(type(value)):
            return {
                name: self._prepare_value(value_)
                for name, value_ in self._converter.get_data(value).items()
            }
        elif isinstance(value, datetime):
            return get_timestamp(value)
        elif isinstance(value, list):
            return [self._prepare_value(i) for i in value]

        return value

    def _set_file(self, value: InputFile, parameter: Optional[str] = None) -> Optional[str]:
        if value.type is InputFileType.FILE:
            file = value.file
        elif value.type is InputFileType.PATH:
            file = value.file.open("rb")
            self.opened_files.append(file)
        else:
            raise ValueError("Incorrect file!")

        if parameter:
            self.files[parameter] = (value.name, file)
        else:
            while True:
                field_name = secrets.token_urlsafe(8)

                if field_name not in self.files:
                    break

            self.files[field_name] = (value.name, file)

            return f"attach://{field_name}"

    def _get_parse_mode(
        self,
        parse_mode: Union[str, None, Unset],
        entities: Optional[list[MessageEntity]] = None
    ) -> Optional[str]:
        if parse_mode is not UNSET:
            return parse_mode
        elif self._default_parameters.parse_mode is not UNSET and not entities:
            return self._default_parameters.parse_mode

    def _get_link_preview_options(
        self,
        options: Union[LinkPreviewOptions, None, Unset]
    ) -> Optional[LinkPreviewOptions]:
        if options:
            if options.is_disabled is not UNSET:
                return options
            elif self._default_parameters.disable_link_preview:
                data = self._converter.get_data(options)
                data["is_disabled"] = True

                return self._converter.get_object(
                    data=data,
                    class_=LinkPreviewOptions
                )
        elif self._default_parameters.disable_link_preview:
            return LinkPreviewOptions(is_disabled=True)

    def _get_disable_notification(
        self,
        disable_notification: Union[bool, None, Unset]
    ) -> Optional[bool]:
        if disable_notification is not UNSET:
            return disable_notification
        elif self._default_parameters.disable_notification:
            return True

    def _get_protect_content(
        self,
        protect_content: Union[bool, None, Unset]
    ) -> Optional[bool]:
        if protect_content is not UNSET:
            return protect_content
        elif self._default_parameters.protect_content:
            return True
