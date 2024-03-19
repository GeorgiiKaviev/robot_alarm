from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.base_models.models import Places, Alarms


# хэндлеры для получения значений из базы данных
async def get_place(session: AsyncSession, place_id: int) -> list[Places]:
    result = await session.execute(
        select(Places.id, Places.cameras).filter(Places.id == place_id)
    )
    return result.scalars().all()


async def get_alarm(session: AsyncSession, alarm_id: int) -> list[Alarms]:
    result = await session.execute(
        select(Alarms.message, Alarms.movie).filter(Alarms.id == alarm_id)
    )
    return result.scalars().all()
