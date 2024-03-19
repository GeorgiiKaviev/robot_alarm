from sqlalchemy import Column, Integer, Text, Boolean
from base_models.base import Base


class Alarms(Base):
    __tablename__ = "alarms"
    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(Text)  # длина!
    movie = Column(Boolean, default=False)


class Places(Base):
    __tablename__ = "place"
    id = Column(Integer, primary_key=True)
    place = Column(Text)
    cameras = Column(Text)
