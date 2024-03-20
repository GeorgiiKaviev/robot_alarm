import os

import dotenv

dotenv.load_dotenv()

DATABASE = os.getenv("DATABASE")
USERNAME = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
