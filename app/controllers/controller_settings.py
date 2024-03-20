from dataclasses import dataclass
from config.settings import DATABASE, USERNAME, PASSWORD, HOST, PORT, TOKEN, CHAT_ID


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
    chat_id: int


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config() -> Config:

    return Config(
        tg_bot=TgBot(token=TOKEN, chat_id=CHAT_ID),
        db=DatabaseConfig(
            database=DATABASE,
            username=USERNAME,
            password=PASSWORD,
            host=HOST,
            port=PORT,
        ),
    )
