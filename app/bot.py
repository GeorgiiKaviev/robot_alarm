import aiohttp
import asyncio
from app.controllers.controller_settings import Config, load_config

connect: Config = load_config()
token = connect.tg_bot.token
chat_id = connect.tg_bot.token
type_send = ("sendmessege", "sendvideo")

URL = f"https://api.telegram.org/bot{token}/getMe"
sendurl = "https://api.telegram.org/bot{0}/{1}?chat_id={2}&text={3}"


async def send_messege(*args):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            sendurl.format(token, type_send[0], chat_id, args)
        ) as resp:
            print(resp.status)
            print(await resp.text())


async def send_video(*args):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            sendurl.format(token, type_send[1], chat_id, args)
        ) as resp:
            print(resp.status)
            print(await resp.text())
