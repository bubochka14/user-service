from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper, crud as user_crud

router = APIRouter(
    tags=["User"],
)


class Status(str, Enum):
    is_registered = "is_registered"
    is_changed_nickname = "is_changed_nickname"


@router.post("/{telegram_id}")
async def create_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        telegram_id: int,
        username: str | None = None,
):
    await user_crud.create_user(session=session, telegram_id=telegram_id, username=username)


@router.get("/{telegram_id}")
async def get_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        telegram_id: int,
):
    return await user_crud.get_user(session=session, telegram_id=telegram_id)


@router.get("/{telegram_id}/status/{status}")
async def get_user_status(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        telegram_id: int,
        status: Status,
):
    return await user_crud.get_user_status(session=session, telegram_id=telegram_id, field=status.value)


@router.put("/{telegram_id}/status/{status}")
async def update_user_status(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        telegram_id: int,
        status: Status,
        value: bool = True
):
    return await user_crud.update_user_status(session=session, telegram_id=telegram_id, field=status.value, value=value)
