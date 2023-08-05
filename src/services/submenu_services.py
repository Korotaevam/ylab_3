from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.restaurant import models, schemas
from src.restaurant.models import Submenu


class SubMenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session: AsyncSession = session
        self.model = Submenu

    async def get_submenus(self, menu_id: UUID, session: AsyncSession) -> list[schemas.Menu]:
        db_submenus = await session.execute(select(models.Submenu).filter(models.Submenu.menu_id == menu_id))
        return db_submenus.scalars().all()  # type: ignore

    async def create_submenu(self, menu_id: UUID, submenu: schemas.SubmenuBase,
                             session: AsyncSession) -> models.Submenu:
        db_submenu = models.Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
        session.add(db_submenu)
        await session.commit()
        await session.refresh(db_submenu)
        return db_submenu

    async def read_submenu(self, menu_id: UUID, submenu_id: UUID, session: AsyncSession) -> schemas.Submenu:
        db_submenu = await session.get(models.Submenu, submenu_id)
        if db_submenu is None or db_submenu.menu_id != menu_id:
            raise HTTPException(status_code=404, detail='submenu not found')
        dishes_count = await session.scalar(
            select(func.count(models.Dish.id)).join(models.Submenu).where(models.Submenu.id == submenu_id))
        return schemas.Submenu(
            id=str(db_submenu.id),  # type: ignore
            title=db_submenu.title,  # type: ignore
            description=db_submenu.description,  # type: ignore
            menu_id=menu_id,
            dishes_count=dishes_count
        )

    async def update_submenu(self, menu_id: UUID, submenu_id: UUID, submenu: schemas.SubmenuUpdate,
                             session: AsyncSession) -> schemas.Submenu:
        db_submenu = await session.get(models.Submenu, submenu_id)
        if db_submenu is None or db_submenu.menu_id != menu_id:
            raise HTTPException(status_code=404, detail='submenu not found')
        for field, value in submenu.dict(exclude_unset=True).items():
            setattr(db_submenu, field, value)
        await session.commit()
        await session.refresh(db_submenu)
        return schemas.Submenu(
            id=str(db_submenu.id),  # type: ignore
            title=db_submenu.title,  # type: ignore
            description=db_submenu.description,  # type: ignore
            menu_id=menu_id
        )

    async def delete_submenu(self, menu_id: UUID, submenu_id: UUID, session: AsyncSession) -> dict[str, str]:
        db_submenu = await session.get(models.Submenu, submenu_id)
        if db_submenu is None or db_submenu.menu_id != menu_id:
            raise HTTPException(status_code=404, detail='submenu not found')
        await session.delete(db_submenu)
        await session.commit()

        return {'message': 'Submenu and all associated dishes deleted successfully'}
