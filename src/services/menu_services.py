from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.restaurant import models, schemas


# Определяем CRUD операции для модели Menu
async def get_menus(skip: int, limit: int, session: AsyncSession) -> list[schemas.Menu]:
    menus = await session.execute(select(models.Menu).offset(skip).limit(limit))
    return menus.scalars().all()


async def create_menu(menu: schemas.MenuCreate, session: AsyncSession) -> schemas.Menu:
    db_menu = models.Menu(title=menu.title, description=menu.description)
    session.add(db_menu)
    await session.commit()
    await session.refresh(db_menu)
    return db_menu


async def read_menu(menu_id: UUID, session: AsyncSession) -> schemas.Menu:
    db_menu = await session.get(models.Menu, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    submenus_count = await session.scalar(
        select(func.count(models.Submenu.id)).join(models.Menu).where(models.Menu.id == menu_id))

    dishes_count = await session.scalar(
        select(func.count(models.Dish.id)).join(models.Submenu).join(models.Menu).where(models.Menu.id == menu_id))

    return schemas.Menu(
        id=str(db_menu.id),
        title=db_menu.title,
        description=db_menu.description,
        submenus_count=submenus_count,
        dishes_count=dishes_count
    )


async def update_menu(menu_id: UUID, menu: schemas.MenuUpdate, session: AsyncSession) -> schemas.Menu:
    db_menu = await session.get(models.Menu, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    for field, value in menu.dict(exclude_unset=True).items():
        setattr(db_menu, field, value)
    await session.commit()
    await session.refresh(db_menu)
    return schemas.Menu(
        id=str(db_menu.id),
        title=db_menu.title,
        description=db_menu.description
    )


async def delete_menu(menu_id: UUID, session: AsyncSession) -> dict[str, str]:
    db_menu = await session.get(models.Menu, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    await session.delete(db_menu)
    await session.commit()
    return {'message': 'menu deleted successfully'}
