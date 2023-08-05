from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.restaurant import models, schemas


async def get_dishes(submenu_id: UUID, session: AsyncSession, skip: int = 0, limit: int = 100) -> list[schemas.Dish]:
    db_dishes = await session.execute(
        select(models.Dish).filter(models.Dish.submenu_id == submenu_id).offset(skip).limit(limit))
    return db_dishes.scalars().all()


async def create_dish(submenu_id: UUID, dish: schemas.DishCreate, session: AsyncSession) -> schemas.Dish:
    db_dish = models.Dish(title=dish.title, description=dish.description, price=str(dish.price), submenu_id=submenu_id)
    session.add(db_dish)
    await session.commit()
    await session.refresh(db_dish)
    return schemas.Dish(id=db_dish.id, title=db_dish.title, description=db_dish.description,
                        price=str(float(round(float(db_dish.price), 2))), submenu_id=db_dish.submenu_id)


async def read_dish(dish_id: UUID, session: AsyncSession) -> schemas.Dish:
    db_dish = await session.execute(select(models.Dish).where(models.Dish.id == dish_id))
    db_dish_row = db_dish.fetchone()
    if db_dish_row is None:
        raise HTTPException(status_code=404, detail='dish not found')
    else:
        db_dish = db_dish_row[0]
    return schemas.Dish(id=db_dish.id, title=db_dish.title, description=db_dish.description,
                        price=str(float(round(float(db_dish.price), 2))), submenu_id=db_dish.submenu_id)


async def update_dish(dish_id: UUID, dish: schemas.DishUpdate, session: AsyncSession) -> schemas.Dish:
    db_dish = await session.get(models.Dish, dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    update_data = dish.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_dish, field, value)
    await session.commit()
    await session.refresh(db_dish)
    return schemas.Dish(id=db_dish.id, title=db_dish.title, description=db_dish.description,
                        price=str(float(round(float(db_dish.price), 2))), submenu_id=db_dish.submenu_id)


async def delete_dish(dish_id: UUID, session: AsyncSession) -> dict[str, str]:
    db_dish = await session.get(models.Dish, dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    await session.delete(db_dish)
    await session.commit()
    return {'message': 'Dish deleted successfully'}
