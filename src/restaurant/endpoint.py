from uuid import UUID

import aioredis
from fastapi import APIRouter, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session
from src.restaurant import schemas
from src.services.dish_services import DishRepository
from src.services.menu_services import MenuRepository
from src.services.submenu_services import SubMenuRepository

router = APIRouter()

CACHE_TIME = 30


@router.on_event('startup')
async def startup_event():
    """ redis """
    redis = aioredis.from_url('redis://localhost', encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


# Определяем CRUD операции для модели Menu
@router.get('/api/v1/menus', response_model=list[schemas.Menu])
@cache(expire=CACHE_TIME)
async def read_menus_handler(skip: int = 0, limit: int = 100, menu: MenuRepository = Depends(),
                             session: AsyncSession = Depends(get_async_session)):
    """ получить меню """
    return await menu.get_menus(skip, limit, session)


@router.post('/api/v1/menus', response_model=schemas.Menu, status_code=status.HTTP_201_CREATED)
async def create_menu_handler(menu_data: schemas.MenuCreate, menu: MenuRepository = Depends(),
                              session: AsyncSession = Depends(get_async_session)):
    """ создать меню """
    return await menu.create_menu(menu_data, session)


@router.get('/api/v1/menus/{menu_id}', response_model=schemas.Menu)
@cache(expire=CACHE_TIME)
async def read_menu_handler(menu_id: UUID, menu: MenuRepository = Depends(),
                            session: AsyncSession = Depends(get_async_session)):
    """ получить меню по id """
    return await menu.read_menu(menu_id, session)


@router.patch('/api/v1/menus/{menu_id}', response_model=schemas.Menu)
async def update_menu_handler(menu_id: UUID, menu_data: schemas.MenuUpdate, menu: MenuRepository = Depends(),
                              session: AsyncSession = Depends(get_async_session)):
    """ изменить меню """
    return await menu.update_menu(menu_id, menu_data, session)


@router.delete('/api/v1/menus/{menu_id}')
async def delete_menu_handler(menu_id: UUID, menu: MenuRepository = Depends(),
                              session: AsyncSession = Depends(get_async_session)):
    """ удалить меню """
    return await menu.delete_menu(menu_id, session)


# Определяем CRUD операции для модели Submenu

@router.get('/api/v1/menus/{menu_id}/submenus', response_model=list[schemas.Menu])
@cache(expire=CACHE_TIME)
async def get_submenus_handler(menu_id: UUID, submenu: SubMenuRepository = Depends(),
                               session: AsyncSession = Depends(get_async_session)):
    """ получить субменю """
    return await submenu.get_submenus(menu_id, session)


@router.post('/api/v1/menus/{menu_id}/submenus', status_code=status.HTTP_201_CREATED)
async def create_submenu_handler(menu_id: UUID, submenu_data: schemas.SubmenuBase,
                                 submenu: SubMenuRepository = Depends(),
                                 session: AsyncSession = Depends(get_async_session)):
    """ создать субменю """
    return await submenu.create_submenu(menu_id, submenu_data, session)


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.Submenu)
@cache(expire=CACHE_TIME)
async def read_submenu_handler(menu_id: UUID, submenu_id: UUID, submenu: SubMenuRepository = Depends(),
                               session: AsyncSession = Depends(get_async_session)):
    """ прочитать субменю по id"""
    return await submenu.read_submenu(menu_id, submenu_id, session)


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.Submenu)
async def update_submenu_handler(menu_id: UUID, submenu_id: UUID, submenu_data: schemas.SubmenuUpdate,
                                 submenu: SubMenuRepository = Depends(),
                                 session: AsyncSession = Depends(get_async_session)):
    """ изменить субменю """
    return await submenu.update_submenu(menu_id, submenu_id, submenu_data, session)


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu_handler(menu_id: UUID, submenu_id: UUID, submenu: SubMenuRepository = Depends(),
                                 session: AsyncSession = Depends(get_async_session)):
    """ удалить субменю """
    return await submenu.delete_submenu(menu_id, submenu_id, session)


# # Определяем CRUD операции для модели Dish
@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=list[schemas.Dish])
@cache(expire=CACHE_TIME)
async def get_dishes_handler(submenu_id: UUID, skip: int = 0, limit: int = 100,
                             dish: DishRepository = Depends(),
                             session: AsyncSession = Depends(get_async_session)):
    """ получить блюдо """
    return await dish.get_dishes(submenu_id, session, skip, limit)


@router.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=schemas.Dish,
             status_code=status.HTTP_201_CREATED)
async def create_dish_handler(submenu_id: UUID, dish_data: schemas.DishCreate,
                              dish: DishRepository = Depends(),
                              session: AsyncSession = Depends(get_async_session)):
    """ создать блюдо """
    return await dish.create_dish(submenu_id, dish_data, session)


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.Dish)
@cache(expire=CACHE_TIME)
async def read_dish_handler(dish_id: UUID, dish: DishRepository = Depends(),
                            session: AsyncSession = Depends(get_async_session)):
    """ получить блюдо по id """
    return await dish.read_dish(dish_id, session)


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.Dish)
async def update_dish_handler(dish_id: UUID, dish_data: schemas.DishUpdate,
                              dish: DishRepository = Depends(),
                              session: AsyncSession = Depends(get_async_session)):
    """ изменить блюдо """
    return await dish.update_dish(dish_id, dish_data, session)


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def delete_dish_handler(dish_id: UUID, dish: DishRepository = Depends(),
                              session: AsyncSession = Depends(get_async_session)):
    """ удалить блюдо """
    return await dish.delete_dish(dish_id, session)
