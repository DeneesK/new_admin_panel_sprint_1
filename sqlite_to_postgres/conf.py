import logging

from pydantic import BaseSettings, PostgresDsn
from dotenv import load_dotenv


LOGGING = {
    "format": "%(asctime)s  - %(levelname)s - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "level": logging.INFO
}

load_dotenv()


class AppSettings(BaseSettings):
    postgres_dsn: PostgresDsn
    sqlite_path: str
    chunk_size: int

    class Config:
        env_file = '.env'


app_settings = AppSettings()
