import contextlib
from typing import Optional, Any, Union, BinaryIO
import time

from httpx import Client, Response, RequestError

from telebox.bot.errors import get_request_error, InternalServerError
from telebox.bot.converter import Converter
from telebox.serialization import get_deserialized_data
from telebox.bot.types.response_parameters import ResponseParameters
from telebox.bot.default_parameters import DefaultParameterSet
from telebox.bot.payload import Payload


API_URL = "https://api.telegram.org"


class Session:
    def __init__(
        self,
        client: Client,
        token: str,
        converter: Converter,
        default_parameters: DefaultParameterSet,
        api_url: str,
        retries: int,
        retry_delay_secs: Union[int, float],
        timeout_secs: Union[int, float]
    ):
        self._client = client
        self._token = token
        self._converter = converter
        self._default_parameters = default_parameters
        self._api_url = api_url
        self._retries = retries
        self._retry_delay_secs = retry_delay_secs
        self._timeout_secs = timeout_secs

    def send_request(
        self,
        method: str,
        *,
        parameters: Optional[dict[str, Any]] = None,
        timeout_secs: Union[int, float, None] = None
    ) -> Any:
        url = self._get_api_url(method)
        payload = Payload(
            parameters=parameters or {},
            converter=self._converter,
            default_parameters=self._default_parameters
        )
        timeout_secs = timeout_secs or self._timeout_secs
        retries = 0

        try:
            while True:
                try:
                    return self._process_response(
                        response=self._client.post(
                            url=url,
                            data=payload.data,
                            files=payload.files,
                            timeout=timeout_secs
                        ),
                        method=method,
                        parameters=payload.data
                    )
                except (RequestError, InternalServerError):
                    if retries == self._retries:
                        raise

                    for i in payload.opened_files:
                        i.seek(0)

                    retries += 1
                    time.sleep(self._retry_delay_secs)
        finally:
            for i in payload.opened_files:
                with contextlib.suppress(Exception):
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

    def _get_api_url(self, method: str) -> str:
        return f"{self._api_url}/bot{self._token}/{method}"

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
