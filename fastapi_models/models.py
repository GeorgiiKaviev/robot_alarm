from pydantic import BaseModel


class DataPlace(BaseModel):
    id: int
    camera: str


class DataAlarm(BaseModel):
    message: str
    movie: bool
