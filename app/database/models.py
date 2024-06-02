import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Income(Base):
    __tablename__ = 'income'

    id: Mapped[int] = mapped_column(primary_key=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    date: Mapped[datetime.date] = mapped_column()
    time: Mapped[datetime.time] = mapped_column()
    concentration: Mapped[str] = mapped_column()


class Outcome(Base):
    __tablename__ = 'outcome'

    id: Mapped[int] = mapped_column(primary_key=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    date: Mapped[datetime.date] = mapped_column()
    time: Mapped[datetime.time] = mapped_column()
    concentration: Mapped[str] = mapped_column()


class TankVolume(Base):
    __tablename__ = 'volume'

    id: Mapped[int] = mapped_column(primary_key=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    volume: Mapped[int] = mapped_column()
    tank_name: Mapped[str] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
