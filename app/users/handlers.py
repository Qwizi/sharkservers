from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event
from app.handlers import log_debug_event
from app.users.enums import UsersEventsEnum, UsersAdminEventsEnum

"""
Users events handlers
"""


@local_handler.register(event_name=UsersEventsEnum.GET_ALL_PRE)
async def handle_users_event_get_all_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersEventsEnum.GET_ALL_POST)
async def handle_users_event_get_all_post(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersEventsEnum.GET_ONE_PRE)
async def handle_users_event_get_one_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersEventsEnum.GET_ONE_POST)
async def handle_users_event_get_one_post(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersEventsEnum.ME_PRE)
async def handle_users_event_me_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersEventsEnum.ME_POST)
async def handle_users_event_me_post(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersEventsEnum.CHANGE_USERNAME_PRE)
async def handle_users_event_change_username_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersEventsEnum.CHANGE_USERNAME_POST)
async def handle_users_event_change_username_post(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersEventsEnum.CHANGE_PASSWORD_PRE)
async def handle_users_event_change_password_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersEventsEnum.CHANGE_PASSWORD_POST)
async def handle_users_event_change_password_post(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersEventsEnum.GET_ONLINE_PRE)
async def handle_users_event_get_online_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersEventsEnum.GET_ONLINE_POST)
async def handle_users_event_get_online_post(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersEventsEnum.GET_LAST_LOGGED_PRE)
async def handle_users_event_get_last_logged_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersEventsEnum.GET_LAST_LOGGED_POST)
async def handle_users_event_get_last_logged_post(event: Event):
    log_debug_event(event)


"""
Users admin events handlers
"""


@local_handler.register(event_name=UsersAdminEventsEnum.GET_ALL_PRE)
async def handle_users_admin_event_get_all_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersAdminEventsEnum.GET_ALL_POST)
async def handle_users_admin_event_get_all_post(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersAdminEventsEnum.GET_ONE_PRE)
async def handle_users_admin_event_get_one_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersAdminEventsEnum.GET_ONE_POST)
async def handle_users_admin_event_get_one_post(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersAdminEventsEnum.CREATE_PRE)
async def handle_users_admin_event_create_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersAdminEventsEnum.CREATE_POST)
async def handle_users_admin_event_create_post(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersAdminEventsEnum.DELETE_PRE)
async def handle_users_admin_event_delete_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=UsersAdminEventsEnum.DELETE_POST)
async def handle_users_admin_event_delete_post(event: Event):
    log_debug_event(event)
