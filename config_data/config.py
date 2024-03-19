from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str
    username: str
    password: str
    host: str
    port: str


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN")),
        db=DatabaseConfig(
            database=env("DATABASE"),
            username=env("USER"),
            password=env("PASSWORD"),
            host=env("HOST"),
            port=env("PORT"),
        ),
    )
