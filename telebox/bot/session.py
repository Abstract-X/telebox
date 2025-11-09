from datetime import datetime
from typing import Optional, Any, Union, IO, BinaryIO
import secrets
import time

from httpx import Client, Response, RequestError

from telebox.utils.unset import Unset, UNSET
from telebox.bot.errors import get_request_error, InternalServerError
from telebox.bot.converter import Converter, get_timestamp
from telebox.utils.serialization import get_serialized_data, get_deserialized_data
from telebox.bot.types.response_parameters import ResponseParameters
from telebox.bot.types.input_file import InputFile
from telebox.bot.types.message_entity import MessageEntity
from telebox.bot.types.link_preview_options import LinkPreviewOptions
from telebox.bot.enums.input_file_type import InputFileType
from telebox.bot.default_parameters import DefaultParameterSet


API_URL = "https://api.telegram.org"


class Session:
    def __init__(
        self,
        token: str,
        converter: Converter,
        default_parameters: DefaultParameterSet,
        api_url: str,
        retries: int,
        retry_delay_secs: Union[int, float],
        timeout_secs: Union[int, float]
    ):
        self._token = token
        self._converter = converter
        self._default_parameters = default_parameters
        self._api_url = api_url
        self._retries = retries
        self._retry_delay_secs = retry_delay_secs
        self._timeout_secs = timeout_secs
        self._client = Client()

    def send_request(
        self,
        method: str,
        *,
        parameters: Optional[dict[str, Any]] = None,
        timeout_secs: Union[int, float, None] = None
    ) -> Any:
        url = self._get_api_url(method)
        data, files, opened_files = self._get_payload(parameters)
        timeout_secs = timeout_secs or self._timeout_secs
        retries = 0

        try:
            while True:
                try:
                    return self._process_response(
                        response=self._client.post(
                            url=url,
                            data=data,
                            files=files,
                            timeout=timeout_secs
                        ),
                        method=method,
                        parameters=data
                    )
                except (RequestError, InternalServerError):
                    if retries == self._retries:
                        raise

                    for i in opened_files:
                        i.seek(0)

                    retries += 1
                    time.sleep(self._retry_delay_secs)
        finally:
            for i in opened_files:
                i.close()

    def download_file(
        self,
        path: str,
        file: BinaryIO,
        chunk_size: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> None:
        if self._api_url == API_URL:
            with self._client.stream(
                method="GET",
                url=f"{API_URL}/file/bot{self._token}/{path}",
                timeout=timeout_secs
            ) as response:
                response.raise_for_status()

                for i in response.iter_bytes(chunk_size=chunk_size):
                    file.write(i)
        else:
            with open(path, "rb") as local_file:
                while True:
                    chunk = local_file.read(chunk_size)

                    if not chunk:
                        break

                    file.write(chunk)

    def close(self) -> None:
        self._client.close()

    def _get_api_url(self, method: str) -> str:
        return f"{self._api_url}/bot{self._token}/{method}"

    def _get_payload(
        self,
        parameters: Optional[dict[str, Any]] = None
    ) -> tuple[dict[str, Any], dict[str, IO], list[IO]]:
        data = {}
        files = {}
        opened_files = []

        if parameters:
            for parameter, value in parameters.items():
                if parameter.endswith("parse_mode"):
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

                value = self._prepare_payload_value(
                    value=value,
                    files=files,
                    opened_files=opened_files
                )

                if isinstance(value, (dict, list)):
                    value = get_serialized_data(value)
                elif not isinstance(value, tuple):
                    value = str(value)

                data[parameter] = value

        return data, files, opened_files

    def _prepare_payload_value(
        self,
        value: Any,
        files: dict[str, tuple[str, IO]],
        opened_files: list[IO],
        attach: bool = False
    ) -> Any:
        if isinstance(value, InputFile):
            if value.type is InputFileType.FILE:
                file = value.file
            elif value.type is InputFileType.PATH:
                file = value.file.open("rb")
                opened_files.append(file)
            else:
                raise ValueError("Incorrect file!")

            if attach:
                while True:
                    field_name = secrets.token_urlsafe(8)

                    if field_name not in files:
                        break

                files[field_name] = (value.name, file)

                return f"attach://{field_name}"

            return value.name, file
        elif self._converter.check_class(type(value)):
            return {
                name: self._prepare_payload_value(
                    value=value_,
                    files=files,
                    opened_files=opened_files,
                    attach=True
                )
                for name, value_ in self._converter.get_data(value).items()
            }
        elif isinstance(value, datetime):
            return get_timestamp(value)
        elif isinstance(value, list):
            return [
                self._prepare_payload_value(
                    value=i,
                    files=files,
                    opened_files=opened_files,
                    attach=True
                )
                for i in value
            ]

        return value

    def _process_response(
        self,
        response: Response,
        method: str,
        parameters: dict[str, Any]
    ) -> Any:
        data = get_deserialized_data(response.content)

        if not data["ok"] or (response.status_code != 200):
            try:
                response_parameter_data = data["parameters"]
            except KeyError:
                response_parameters = None
            else:
                response_parameters = self._converter.get_object(
                    data=response_parameter_data,
                    class_=ResponseParameters
                )

            raise get_request_error(
                method=method,
                parameters=parameters,
                status_code=response.status_code,
                description=data["description"],
                response_parameters=response_parameters
            )

        return data["result"]

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
