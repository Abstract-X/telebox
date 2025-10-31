from datetime import datetime
from typing import Optional, Any, Union, IO, BinaryIO
import secrets
import time

from httpx import Client, Response, RequestError

from telebox.utils.unset import UNSET
from telebox.bot.errors import get_request_error, RetryAfterError, InternalServerError
from telebox.bot.utils.converter import Converter, get_timestamp
from telebox.utils.serialization import get_serialized_data, get_deserialized_data
from telebox.bot.types.response_parameters import ResponseParameters
from telebox.bot.types.input_file import InputFile
from telebox.bot.enums.input_file_type import InputFileType


API_URL = "https://api.telegram.org"


class Session:
    def __init__(
        self,
        token: str,
        converter: Converter,
        api_url: str,
        retries: int,
        retry_delay_secs: Union[int, float],
        timeout_secs: Union[int, float],
        wait_on_rate_limit: bool
    ):
        self._token = token
        self._converter = converter
        self._api_url = api_url
        self._retries = retries
        self._retry_delay_secs = retry_delay_secs
        self._timeout_secs = timeout_secs
        self._wait_on_rate_limit = wait_on_rate_limit
        self._client = Client()

    def send_request(
        self,
        method: str,
        *,
        parameters: Optional[dict[str, Any]] = None,
        timeout_secs: Union[int, float, None] = None
    ):
        parameters = {
            name: value
            for name, value in (parameters or {}).items()
            if value is not None and value is not UNSET
        }
        timeout_secs = timeout_secs or self._timeout_secs
        retries = 0
        url = self._get_api_url(method)
        data, files, opened_files = self._get_payload(parameters)

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
                        parameters=parameters
                    )
                except (RequestError, InternalServerError):
                    if retries == self._retries:
                        raise

                    retries += 1
                    time.sleep(self._retry_delay_secs)
                except RetryAfterError as error:
                    if not self._wait_on_rate_limit:
                        raise

                    retries = 0
                    time.sleep(error.retry_after)
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
        parameters: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, IO], list[IO]]:
        data = {}
        files = {}
        opened_files = []

        for name, value in parameters.items():
            value = self._prepare_payload_value(
                value=value,
                files=files,
                opened_files=opened_files
            )

            if isinstance(value, (dict, list)):
                value = get_serialized_data(value)
            elif not isinstance(value, tuple):
                value = str(value)

            data[name] = value

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
