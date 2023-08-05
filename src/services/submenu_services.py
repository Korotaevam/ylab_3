from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.restaurant import models, schemas


async def get_submenus(menu_id: UUID, session: AsyncSession) -> list[schemas.Menu]:
    db_submenus = await session.execute(select(models.Submenu).filter(models.Submenu.menu_id == menu_id))
    return db_submenus.scalars().all()


async def create_submenu(menu_id: UUID, submenu: schemas.SubmenuBase, session: AsyncSession) -> models.Submenu:
    db_submenu = models.Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
    session.add(db_submenu)
    await session.commit()
    await session.refresh(db_submenu)
    return db_submenu


async def read_submenu(menu_id: UUID, submenu_id: UUID, session: AsyncSession) -> schemas.Submenu:
    db_submenu = await session.get(models.Submenu, submenu_id)
    if db_submenu is None or db_submenu.menu_id != menu_id:
        raise HTTPException(status_code=404, detail='submenu not found')
    dishes_count = await session.scalar(
        select(func.count(models.Dish.id)).join(models.Submenu).where(models.Submenu.id == submenu_id))
    return schemas.Submenu(
        id=str(db_submenu.id),
        title=db_submenu.title,
        description=db_submenu.description,
        menu_id=menu_id,
        dishes_count=dishes_count
    )


async def update_submenu(menu_id: UUID, submenu_id: UUID, submenu: schemas.SubmenuUpdate,
                         session: AsyncSession) -> schemas.Submenu:
    db_submenu = await session.get(models.Submenu, submenu_id)
    if db_submenu is None or db_submenu.menu_id != menu_id:
        raise HTTPException(status_code=404, detail='submenu not found')
    for field, value in submenu.dict(exclude_unset=True).items():
        setattr(db_submenu, field, value)
    await session.commit()
    await session.refresh(db_submenu)
    return schemas.Submenu(
        id=str(db_submenu.id),
        title=db_submenu.title,
        description=db_submenu.description,
        menu_id=menu_id
    )


async def delete_submenu(menu_id: UUID, submenu_id: UUID, session: AsyncSession) -> dict[str, str]:
    db_submenu = await session.get(models.Submenu, submenu_id)
    if db_submenu is None or db_submenu.menu_id != menu_id:
        raise HTTPException(status_code=404, detail='submenu not found')
    await session.delete(db_submenu)
    await session.commit()

    return {'message': 'Submenu and all associated dishes deleted successfully'}
