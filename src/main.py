from email import message
import json
import os
from typing import Annotated
import anyio
from fastapi.encoders import jsonable_encoder

from fastapi import (
    FastAPI,
    Depends,
    Security,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    )
from fastapi.routing import APIRoute
from fastapi_events.dispatcher import dispatch
from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_pagination import Params, add_pagination
from jose import JWTError
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from src.chat.enums import WebsocketEventEnum
from src.chat.schemas import ChatEventSchema
from src.chat.dependencies import get_chat_service
from src.chat.services import ChatService
from src.chat.dependencies import ws_get_current_user
from src.servers.dependencies import get_servers_service
from src.servers.services import ServerService

from src.__version import VERSION
from src.auth.dependencies import (
    get_auth_service,
    get_application,
    get_access_token_service,
)
from src.auth.schemas import RegisterUserSchema
from src.auth.services.auth import AuthService
from src.forum.dependencies import (
    get_threads_service,
    get_posts_service,
)

# Events
from src.auth.views import router as auth_router_v1
from src.db import REDIS_URL, database, create_redis_pool, settings
from src.forum.views import (
    router_v1 as forum_router,
    admin_router_v1 as admin_forum_router,
)
from src.players.views import router as steamprofile_router
from src.players.views_admin import router as admin_steamprofiles_router
from src.roles.dependencies import get_roles_service
from src.roles.services import RoleService
from src.roles.views import router as roles_router
from src.roles.views_admin import router as admin_roles_router
from src.scopes.dependencies import get_scopes_service
from src.scopes.services import ScopeService
from src.scopes.views import router as scopes_router
from src.scopes.views_admin import router as admin_scopes_router
from src.servers.views import router as servers_router
from src.servers.views_admin import router as admin_servers_router
from src.services import MainService
from src.chat.views import router as chat_router
from src.subscryptions.views import router as subscryptions_router
from aiocron import crontab

# Routes
from src.users.views import router as users_router_v1

# Admin Routes
from src.users.views_admin import (
    router as admin_users_router,
)
from src.users.models import User
from .apps.models import App
from .auth.utils import now_datetime
from .forum.dependencies import (
    get_categories_service,
    get_threads_service,
    get_posts_service,
)
from .forum.services import CategoryService, ThreadService, PostService

# import admin posts router
from broadcaster import Broadcast
from .auth.handlers import create_activate_code_after_register
from .logger import logger
from .users.dependencies import get_users_service

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "../static/")
installed_file_path = os.path.join(script_dir, "installed")


broadcast = Broadcast(REDIS_URL)


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


async def connect_db(_app: FastAPI):
    database_ = _app.state.database
    if not database_.is_connected:
        await database.connect()
    _app.state.redis = await create_redis_pool()
    await FastAPILimiter.init(_app.state.redis)
    return _app


async def disconnect_db(_app: FastAPI):
    database_ = _app.state.database
    if database_.is_connected:
        await database_.disconnect()
    await app.state.redis.close()


async def connect_broadcast(_app: FastAPI):
    _app.state.broadcast = broadcast
    await broadcast.connect()
    return _app


async def disconnect_broadcast(_app: FastAPI):
    broadcast_ = _app.state.broadcast
    await broadcast_.disconnect()


async def chatroom_ws_receiver(
    websocket, chat_service: ChatService, author: User | None = None
):
    async for message in websocket.iter_json():
        message_event = message.get("event", None)
        message_data = message.get("data", None)
        if message_event == WebsocketEventEnum.SEND_MESSAGE:
            if message_data is None:
                return

            new_message = await chat_service.create(author=author, message=message_data)
            logger.info(new_message)
            new_message_schema = ChatEventSchema(
                event=WebsocketEventEnum.GET_MESSAGE, data=new_message
            )
            messages = await chat_service.get_all(
                params=Params(size=10),
                related=[
                    "author",
                    "author__display_role",
                    "author__player",
                    "author__player__steamrep_profile",
                ],
                order_by="-id",
            )
            messages_schema = ChatEventSchema(
                event=WebsocketEventEnum.GET_MESSAGES, data=messages
            )
            # await websocket.send_json(jsonable_encoder(messages_schema))
            await broadcast.publish(
                channel="chat", message=json.dumps(jsonable_encoder(messages_schema))
            )

        await broadcast.publish(channel="chat", message=json.dumps(message))


async def chatroom_ws_sender(
    websocket: WebSocket, chat_service: ChatService, author: User = None
):
    async with broadcast.subscribe(channel="chat") as subscriber:
        async for event in subscriber:
            message = json.loads(event.message)
            message_event = message.get("event", None)
            message_data = message.get("data", None)
            logger.info(message_event)
            if message_event == WebsocketEventEnum.GET_MESSAGES:
                messages = await chat_service.get_all(
                    params=Params(size=10),
                    related=[
                        "author",
                        "author__display_role",
                        "author__player",
                        "author__player__steamrep_profile",
                    ],
                    order_by="-id",
                )
                messages_schema = ChatEventSchema(
                    event=WebsocketEventEnum.GET_MESSAGES, data=messages
                )
                await websocket.send_json(jsonable_encoder(messages_schema))
            # elif message_event == WebsocketEventEnum.SEND_MESSAGE:
            #     if message_data is None:
            #         return
            #     new_message = await chat_service.create(
            #         author=author, message=message_data
            #     )
            #     logger.info(new_message)
            #     new_message_schema = ChatEventSchema(
            #         event=WebsocketEventEnum.GET_MESSAGE, data=new_message
            #     )
            #     messages = await chat_service.get_all(
            #             params=Params(size=10),
            #             related=["author", "author__display_role"],
            #             order_by="-id",
            #     )
            #     messages_schema = ChatEventSchema(
            #             event=WebsocketEventEnum.GET_MESSAGES, data=messages
            #     )
            #     await websocket.send_json(jsonable_encoder(messages_schema))


def init_routes(_app: FastAPI):
    # V1 routes
    _app.include_router(auth_router_v1, prefix="/v1/auth", tags=["auth"])
    _app.include_router(users_router_v1, prefix="/v1/users", tags=["users"])
    _app.include_router(scopes_router, prefix="/v1/scopes", tags=["scopes"])
    _app.include_router(roles_router, prefix="/v1/roles", tags=["roles"])
    _app.include_router(steamprofile_router, prefix="/v1/players", tags=["players"])
    _app.include_router(forum_router)
    _app.include_router(servers_router, prefix="/v1/servers", tags=["servers"])
    _app.include_router(chat_router, prefix="/v1/chat", tags=["chat"])
    _app.include_router(
        subscryptions_router, prefix="/v1/subscryption", tags=["subscryption"]
    )

    # Admin routes
    _app.include_router(
        admin_users_router, prefix="/v1/admin/users", tags=["admin-users"]
    )
    _app.include_router(
        admin_roles_router, prefix="/v1/admin/roles", tags=["admin-roles"]
    )
    _app.include_router(
        admin_scopes_router, prefix="/v1/admin/scopes", tags=["admin-scopes"]
    )
    _app.include_router(
        admin_steamprofiles_router, prefix="/v1/admin/players", tags=["admin-players"]
    )
    _app.include_router(admin_forum_router)
    _app.include_router(
        admin_servers_router, prefix="/v1/admin/servers", tags=["admin-servers"]
    )
    return _app


@crontab("* * * * *")
async def update_tables_counters():
    try:
        logger.info("Updating tables counters")
        categories_service = await get_categories_service()
        threads_service = await get_threads_service()
        posts_service = await get_posts_service()
        users_service = await get_users_service()
        await categories_service.sync_counters()
        await threads_service.sync_counters()
        await posts_service.sync_counters()
        await users_service.sync_counters(
            threads_service=threads_service, posts_service=posts_service
        )
        logger.info("Finished updating tables counters")
    except Exception as e:
        logger.error(e)


def create_app():
    _app = FastAPI(
        name="Shark API",
        version=VERSION,
        debug=True,
        generate_unique_id_function=custom_generate_unique_id,
    )
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:3001"
            "https://api-sharkservers.qwizi.dev",
            "https://beta.sharkservers.pl",
            "https://api.sharkservers.pl",
            "https://api-beta.sharkservers.pl",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    event_handler_id: int = id(_app)
    _app.add_middleware(
        EventHandlerASGIMiddleware,
        handlers=[local_handler],
        middleware_id=event_handler_id,
    )
    _app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")
    _app.state.database = database
    init_routes(_app)
    add_pagination(_app)

    @_app.on_event("startup")
    async def startup():
        await connect_db(_app)
        await connect_broadcast(_app)

    @_app.on_event("shutdown")
    async def shutdown():
        await disconnect_db(_app)
        await FastAPILimiter.close()
        await disconnect_broadcast(_app)

    @_app.middleware("http")
    async def update_user_last_online_time(request: Request, call_next):
        response = await call_next(request)
        if "Authorization" not in request.headers:
            return response
        try:
            access_token_service = await get_access_token_service(settings=settings)
            jwt_token = await AuthService.oauth2_scheme(request=request)
            token_data = access_token_service.decode_token(jwt_token)
            users_service = await get_users_service()
            user = await users_service.get_one(id=token_data.user_id)
            await user.update(last_online=now_datetime())
            return response
        except (JWTError, HTTPException):
            return response

    @_app.post("/install", tags=["root"])
    async def install(
        user_data: RegisterUserSchema,
        scopes_service: ScopeService = Depends(get_scopes_service),
        roles_service: RoleService = Depends(get_roles_service),
        auth_service: AuthService = Depends(get_auth_service),
    ):
        await MainService.install(
            file_path=installed_file_path,
            admin_user_data=user_data,
            scopes_service=scopes_service,
            roles_service=roles_service,
            auth_service=auth_service,
        )
        return {"msg": "Successfully installed"}

    @_app.get("/generate-openapi", tags=["root"])
    async def generate_openapi():
        await MainService.generate_openapi_file()
        return {"msg": "Done"}

    @_app.get("/generate-random-data", tags=["root"])
    async def generate_random_data(
        auth_service: AuthService = Depends(get_auth_service),
        roles_service: RoleService = Depends(get_roles_service),
        categories_service: CategoryService = Depends(get_categories_service),
        threads_service: ThreadService = Depends(get_threads_service),
        posts_service: PostService = Depends(get_posts_service),
        servers_service: ServerService = Depends(get_servers_service),
    ):
        dispatch(
            event_name="GENERATE_RANDOM_DATA",
            payload={
                "auth_service": auth_service,
                "roles_service": roles_service,
                "categories_service": categories_service,
                "threads_service": threads_service,
                "posts_service": posts_service,
                "servers_service": servers_service,
            },
        )
        return {"msg": "Done"}

    @_app.get("/protected", tags=["root"])
    async def protected_route(
        app: App = Security(get_application, scopes=["users:create"]),
    ):
        return {"msg": "You are authenticated!"}

    @_app.get("/test", tags=["root"])
    async def test(
        request: Request,
    ):
        client_host = request.client.host
        user_agent = request.headers.get("User-Agent", None)
        x_forwarded_for = request.headers.get("X-Forwarded-For", None)
        x_real_ip = request.headers.get("X-Real-Ip", None)
        return {"user_ip": client_host, "user_agent": user_agent, "X-Forwarded-For": x_forwarded_for, "X-Real-Ip": x_real_ip}

    @_app.websocket("/ws")
    async def websocket_endpoint(
        websocket: WebSocket,
        chat_service: ChatService = Depends(get_chat_service),
        author: User = Depends(ws_get_current_user),
    ):
        try:
            logger.info(_app.state.broadcast)
            await websocket.accept()

            async with anyio.create_task_group() as task_group:
                # run until first is complete
                async def run_chatroom_ws_receiver() -> None:
                    await chatroom_ws_receiver(
                        websocket=websocket, chat_service=chat_service, author=author
                    )
                    task_group.cancel_scope.cancel()

                task_group.start_soon(run_chatroom_ws_receiver)
                await chatroom_ws_sender(
                    websocket, chat_service=chat_service, author=author
                )
        except WebSocketDisconnect:
            pass

    return _app


app = create_app()
