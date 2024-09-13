from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, func

from core import Base


class User(Base):
    """Таблица users"""
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, unique=True)
    username: Mapped[str | None] = mapped_column(nullable=True)
    nickname: Mapped[str | None] = mapped_column(String(15), nullable=True, unique=True)
    registration_date: Mapped[datetime] = mapped_column(server_default=func.now())
    match_points: Mapped[int] = mapped_column(default=0)


class StatusesUser(Base):
    """Таблица statuses_users"""
    __tablename__ = "statuses_users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, unique=True)
    is_registered: Mapped[bool] = mapped_column(default=False)
    is_changed_nickname: Mapped[bool] = mapped_column(default=False)
