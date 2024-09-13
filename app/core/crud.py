from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, StatusesUser


async def create_user(session: AsyncSession, telegram_id: int, username: str | None) -> None:
    user = User(telegram_id=telegram_id, username=username)
    statuses_user = StatusesUser(telegram_id=telegram_id)
    try:
        session.add_all([user, statuses_user])
        await session.commit()
    except IntegrityError:
        await session.rollback()


async def get_user(session: AsyncSession, telegram_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def update_user(session: AsyncSession, telegram_id: int, **fields) -> None:
    stmt = update(User).where(User.telegram_id == telegram_id).values(**fields)
    await session.execute(stmt)
    await session.commit()


async def get_user_status(session: AsyncSession, telegram_id: int, field: str) -> bool | None:
    stmt = select(getattr(StatusesUser, field)).where(StatusesUser.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalar()


async def update_user_status(session: AsyncSession, telegram_id: int, field: str, value: bool = True) -> None:
    stmt = update(StatusesUser).where(StatusesUser.telegram_id == telegram_id).values({field: value})
    await session.execute(stmt)
    await session.commit()
