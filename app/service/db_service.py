from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.packer_models import DataPlace, DataAlarm, Place, Alarm


# хэндлеры для получения значений из базы данных
async def get_place(session: AsyncSession, place_id: int) -> DataPlace:
    result = await session.execute(
        select(Place.id, Place.place, Place.cameras).filter(Place.id == place_id)
    )
    return result.fetchone()


async def get_alarm(session: AsyncSession, alarm_id: int) -> DataAlarm:
    result = await session.execute(
        select(Alarm.id, Alarm.message, Alarm.movie).filter(Alarm.id == alarm_id)
    )
    return result.fetchone()
