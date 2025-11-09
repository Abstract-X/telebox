import logging
from queue import Queue
from typing import Optional, Union
from pathlib import Path

from telebox.bot.types import Update
from telebox.bot.converter import Converter
from telebox.dispatcher.listener import AbstractListener
from telebox.utils.serialization import get_deserialized_data


logger = logging.getLogger(__name__)


class WebhookListener(AbstractListener):
    def __init__(
        self,
        converter: Converter,
        *,
        host: str = "0.0.0.0",
        port: int = 443,
        path: Optional[str] = None,
        secret_token: Optional[str] = None,
        certificate_path: Union[str, Path, None] = None,
        private_key_path: Union[str, Path, None] = None
    ):
        self._converter = converter
        self._host = host
        self._port = port
        self._path = path
        self._secret_token = secret_token
        self._certificate_path = certificate_path
        self._private_key_path = private_key_path

    def run(self, updates: Queue[Update]) -> None:
        try:
            import cherrypy  # noqa
        except ImportError:
            raise ImportError(
                "To use `WebhookListener` you need to install `CherryPy`:"
                "\npip install -U telebox[webhook]"
            ) from None

        cherrypy.config.update({
            "server.socket_host": self._host,
            "server.socket_port": self._port,
            "server.shutdown_timeout": 1,
            "log.screen": False,
            "environment": "production"
        })
        cherrypy.log.error_log.propagate = False
        cherrypy.log.access_log.propagate = False

        if (self._certificate_path is not None) and (self._private_key_path is not None):
            cherrypy.config.update({
                "server.ssl_module": "builtin",
                "server.ssl_certificate": str(self._certificate_path),
                "server.ssl_private_key": str(self._private_key_path),
            })

        server_root = _get_server_root(
            updates=updates,
            converter=self._converter,
            secret_token=self._secret_token
        )
        cherrypy.tree.mount(server_root, self._path)
        logger.info("Server started.")
        cherrypy.engine.start()
        cherrypy.engine.block()
        logger.info("Server stopped.")

    def stop(self) -> None:
        import cherrypy  # noqa

        logger.info("Server stopping...")
        cherrypy.engine.exit()


def _get_server_root(
    updates: Queue[Update],
    converter: Converter,
    secret_token: Optional[str] = None
):
    import cherrypy  # noqa

    class ServerRoot:
        @cherrypy.expose
        def index(self) -> str:
            if cherrypy.request.headers.get("X-Telegram-Bot-Api-Secret-Token") != secret_token:
                raise cherrypy.HTTPError(403)

            content_length = cherrypy.request.headers.get("Content-Length")

            if not content_length:
                raise cherrypy.HTTPError(403)

            update = converter.get_object(
                data=get_deserialized_data(
                    cherrypy.request.body.read(
                        int(content_length)
                    )
                ),
                class_=Update
            )
            updates.put(update)

            return ""

    return ServerRoot()
