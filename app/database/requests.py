from sqlalchemy import select

from app.database.models import (Income, Outcome, TankVolume, User,
                                 async_session)


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_income(date, time, concentration):
    async with async_session() as session:
        session.add(Income(date=date, time=time, concentration=concentration))
        await session.commit()


async def set_outcome(date, time, concentration):
    async with async_session() as session:
        session.add(Outcome(date=date, time=time, concentration=concentration))
        await session.commit()


async def get_income(item_id):
    async with async_session() as session:
        return await session.scalar(select(Income).where(Income.id == item_id))


async def get_outcome(item_id):
    async with async_session() as session:
        return await session.scalar(select(Outcome).where(Outcome.id == item_id))


async def get_tank_volume(item_id):
    async with async_session() as session:
        return await session.scalar(select(TankVolume).where(TankVolume.id == item_id))
