from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session
from src.restaurant import schemas
from src.services.dish_services import (
    create_dish,
    delete_dish,
    get_dishes,
    read_dish,
    update_dish,
)
from src.services.menu_services import (
    create_menu,
    delete_menu,
    get_menus,
    read_menu,
    update_menu,
)
from src.services.submenu_services import (
    create_submenu,
    delete_submenu,
    get_submenus,
    read_submenu,
    update_submenu,
)

router = APIRouter()


# Определяем CRUD операции для модели Menu
@router.on_event('startup')
async def startup_event():
    redis = aioredis.from_url('redis://localhost', encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


@router.get('/api/v1/menus', response_model=list[schemas.Menu])
@cache(expire=30)
async def read_menus_handler(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    return await get_menus(skip, limit, session)


@router.post('/api/v1/menus', response_model=schemas.Menu, status_code=status.HTTP_201_CREATED)
async def create_menu_handler(menu: schemas.MenuCreate, session: AsyncSession = Depends(get_async_session)):
    return await create_menu(menu, session)


@router.get('/api/v1/menus/{menu_id}', response_model=schemas.Menu)
@cache(expire=30)
async def read_menu_handler(menu_id: UUID, session: AsyncSession = Depends(get_async_session)):
    return await read_menu(menu_id, session)


@router.patch('/api/v1/menus/{menu_id}', response_model=schemas.Menu)
async def update_menu_handler(menu_id: UUID, menu: schemas.MenuUpdate,
                              session: AsyncSession = Depends(get_async_session)):
    return await update_menu(menu_id, menu, session)


@router.delete('/api/v1/menus/{menu_id}')
async def delete_menu_handler(menu_id: UUID, session: AsyncSession = Depends(get_async_session)):
    return await delete_menu(menu_id, session)


# Определяем CRUD операции для модели Submenu
@router.get('/api/v1/menus/{menu_id}/submenus', response_model=list[schemas.Menu])
@cache(expire=30)
async def get_submenus_handler(menu_id: UUID, session: AsyncSession = Depends(get_async_session)):
    return await get_submenus(menu_id, session)


@router.post('/api/v1/menus/{menu_id}/submenus', status_code=status.HTTP_201_CREATED)
async def create_submenu_handler(menu_id: UUID, submenu: schemas.SubmenuBase,
                                 session: AsyncSession = Depends(get_async_session)):
    return await create_submenu(menu_id, submenu, session)


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.Submenu)
@cache(expire=30)
async def read_submenu_handler(menu_id: UUID, submenu_id: UUID, session: AsyncSession = Depends(get_async_session)):
    return await read_submenu(menu_id, submenu_id, session)


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.Submenu)
async def update_submenu_handler(menu_id: UUID, submenu_id: UUID, submenu: schemas.SubmenuUpdate,
                                 session: AsyncSession = Depends(get_async_session)):
    return await update_submenu(menu_id, submenu_id, submenu, session)


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu_handler(menu_id: UUID, submenu_id: UUID, session: AsyncSession = Depends(get_async_session)):
    return await delete_submenu(menu_id, submenu_id, session)


# # Определяем CRUD операции для модели Dish
@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=list[schemas.Dish])
@cache(expire=30)
async def get_dishes_handler(submenu_id: UUID, skip: int = 0, limit: int = 100,
                             session: AsyncSession = Depends(get_async_session)):
    return await get_dishes(submenu_id, session, skip, limit)


@router.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=schemas.Dish,
             status_code=status.HTTP_201_CREATED)
async def create_dish_handler(submenu_id: UUID, dish: schemas.DishCreate,
                              session: AsyncSession = Depends(get_async_session)):
    return await create_dish(submenu_id, dish, session)


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.Dish)
@cache(expire=30)
async def read_dish_handler(dish_id: UUID, session: AsyncSession = Depends(get_async_session)):
    return await read_dish(dish_id, session)


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.Dish)
async def update_dish_handler(dish_id: UUID, dish: schemas.DishUpdate,
                              session: AsyncSession = Depends(get_async_session)):
    return await update_dish(dish_id, dish, session)


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def delete_dish_handler(dish_id: UUID, session: AsyncSession = Depends(get_async_session)):
    return await delete_dish(dish_id, session)
