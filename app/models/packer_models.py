from pydantic import BaseModel

from sqlalchemy import Column, Integer, Text, Boolean
from app.utils.base import Base


class DataPlace(BaseModel):
    id: int
    place: str
    camera: str


class DataAlarm(BaseModel):
    id: int
    message: str
    movie: bool


class Alarm(Base):
    __tablename__ = "alarms"
    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(Text)  # длина!
    movie = Column(Boolean, default=False)


class Place(Base):
    __tablename__ = "place"
    id = Column(Integer, primary_key=True)
    place = Column(Text)
    cameras = Column(Text)
