from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.controllers.controller_settings import Config, load_config

connect: Config = load_config("~\.env")

database = connect.db.database
user = connect.db.username
password = connect.db.password
host = connect.db.host
port = connect.db.port

DATABASE_URL = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session
