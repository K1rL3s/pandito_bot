import os
from dataclasses import dataclass


@dataclass
class ServerConfig:
    host: str  # для запуска aiohttp сервака
    port: int
    url: str

    def build_url(self, path: str) -> str:
        return f"{self.url}{path}"


def create_server_config_from_env() -> ServerConfig:
    host = os.environ.get("SERVER_HOST")
    port = int(os.environ.get("SERVER_PORT"))
    url = os.environ.get("SERVER_URL")
    return ServerConfig(host=host, port=port, url=url)