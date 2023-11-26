# apps dependencies
from fastapi import Depends
from fastapi_pagination.ext import ormar

from src.apps.services import AppService


async def get_app_service() -> AppService:
    """
    Get app service
    :return AppService:
    """
    return AppService()


async def get_valid_apps(
    apps_id: int, apps_service: AppService = Depends(get_app_service)
) -> ormar.Model:
    """
    Get valid apps
    :param app_service:
    :param apps_id:
    :return Apps:
    """
    return await apps_service.get_one(id=apps_id)
