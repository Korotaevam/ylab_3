from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.restaurant import models, schemas
from src.restaurant.models import Menu


class MenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session: AsyncSession = session
        self.model = Menu

    async def get_menus(self, skip: int, limit: int, session: AsyncSession) -> list[schemas.Menu]:
        menus = await session.execute(select(models.Menu).offset(skip).limit(limit))
        return menus.scalars().all()  # type: ignore

    async def create_menu(self, menu: schemas.MenuCreate, session: AsyncSession) -> schemas.Menu:
        db_menu = models.Menu(title=menu.title, description=menu.description)
        session.add(db_menu)
        await session.commit()
        await session.refresh(db_menu)
        return db_menu

    async def read_menu(self, menu_id: UUID, session: AsyncSession) -> schemas.Menu:
        db_menu = await session.get(models.Menu, menu_id)
        if db_menu is None:
            raise HTTPException(status_code=404, detail='menu not found')

        submenus_count = await session.scalar(
            select(func.count(models.Submenu.id)).join(models.Menu).where(models.Menu.id == menu_id))

        dishes_count = await session.scalar(
            select(func.count(models.Dish.id)).join(models.Submenu).join(models.Menu).where(models.Menu.id == menu_id))

        return schemas.Menu(
            id=str(db_menu.id),  # type: ignore
            title=db_menu.title,  # type: ignore
            description=db_menu.description,  # type: ignore
            submenus_count=submenus_count,  # type: ignore
            dishes_count=dishes_count  # type: ignore
        )

    async def update_menu(self, menu_id: UUID, menu: schemas.MenuUpdate, session: AsyncSession) -> schemas.Menu:
        db_menu = await session.get(models.Menu, menu_id)
        if db_menu is None:
            raise HTTPException(status_code=404, detail='menu not found')
        for field, value in menu.dict(exclude_unset=True).items():
            setattr(db_menu, field, value)
        await session.commit()
        await session.refresh(db_menu)
        return schemas.Menu(
            id=str(db_menu.id),  # type: ignore
            title=db_menu.title,  # type: ignore
            description=db_menu.description  # type: ignore
        )

    async def delete_menu(self, menu_id: UUID, session: AsyncSession) -> dict[str, str]:
        db_menu = await session.get(models.Menu, menu_id)
        if db_menu is None:
            raise HTTPException(status_code=404, detail='menu not found')
        await session.delete(db_menu)
        await session.commit()
        return {'message': 'menu deleted successfully'}
