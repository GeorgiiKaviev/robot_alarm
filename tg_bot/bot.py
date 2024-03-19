import asyncio
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from aiogram.types import Message
from aiogram.contrib.middlewares.logging import LoggingMiddleware  ##??
from aiogram.types import ParseMode

config: Config = load_config("~\.env")  #'путь к файлу .env'

bot = Bot(token=config.tg_bot.token)
dp = Dispatcher()


## ???
async def send_message(message_text: str):
    await bot.send_message(
        chat_id="YOUR_CHAT_ID", text=message_text, parse_mode=ParseMode.HTML
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
