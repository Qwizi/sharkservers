from datetime import datetime, timedelta
from unittest import mock

import pytest
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import get_access_token_service, get_refresh_token_service
from src.roles.dependencies import get_roles_service
from src.roles.enums import ProtectedDefaultRolesEnum
from src.users.dependencies import get_users_service
from tests.conftest import create_fake_users, TEST_USER, TEST_ADMIN_USER, create_fake_posts, create_fake_threads, \
    _get_auth_service, settings, create_fake_image, create_fake_invalid_image, create_fake_categories

USERS_ENDPOINT = "/v1/users"


@pytest.mark.asyncio
async def test_get_users(client):
    response = await client.get(USERS_ENDPOINT)
    assert response.status_code == 200
    # 1 because of the admin user
    assert response.json()["total"] == 1


@pytest.mark.asyncio
async def test_get_user(client):
    users = await create_fake_users(1)
    response = await client.get(f"{USERS_ENDPOINT}/{users[0].id}")
    assert response.status_code == 200
    assert response.json()["id"] == users[0].id
    assert response.json()["username"] == users[0].username
    assert "password" not in response.json()
    assert "email" not in response.json()
    assert "secret_salt" not in response.json()


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get(f"{USERS_ENDPOINT}/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_staff_users(client):
    response = await client.get(f"{USERS_ENDPOINT}/staff")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["id"] == ProtectedDefaultRolesEnum.ADMIN.value
    assert response.json()["items"][0]["user_display_role"][0]["username"] == TEST_ADMIN_USER.get("username")


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint", [
    f"{USERS_ENDPOINT}/me",
    f"{USERS_ENDPOINT}/me/posts",
    f"{USERS_ENDPOINT}/me/threads",
    f"{USERS_ENDPOINT}/me/apps",

])
async def test_unauthorized_get_logged_user(endpoint, client):
    response = await client.get(endpoint)
    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint", [
    f"{USERS_ENDPOINT}/me/username",
    f"{USERS_ENDPOINT}/me/password",
    f"{USERS_ENDPOINT}/me/display-role",
    f"{USERS_ENDPOINT}/me/email",
    f"{USERS_ENDPOINT}/me/email/confirm",
])
async def test_unauthorized_change_user_data(endpoint, client):
    response = await client.post(endpoint)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_upload_logged_user_avatar(client):
    response = await client.post(f"{USERS_ENDPOINT}/me/avatar")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_logged_user(logged_client):
    response = await logged_client.get(f"{USERS_ENDPOINT}/me")
    assert response.status_code == 200
    assert response.json()["username"] == TEST_USER.get("username")
    assert "password" not in response.json()


@pytest.mark.asyncio
async def test_get_logged_user_posts(logged_client):
    users_service = await get_users_service()
    author = await users_service.get_one(username=TEST_USER.get("username"),
                                         related=["display_role", "display_role__scopes"])
    posts = await create_fake_posts(1, author)
    response = await logged_client.get(f"{USERS_ENDPOINT}/me/posts")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["id"] == posts[0].id


@pytest.mark.asyncio
async def test_get_logged_user_threads(logged_client):
    users_service = await get_users_service()
    categories = await create_fake_categories(1)
    author = await users_service.get_one(username=TEST_USER.get("username"),
                                         related=["display_role", "display_role__scopes"])
    threads = await create_fake_threads(1, author, categories[0])
    response = await logged_client.get(f"{USERS_ENDPOINT}/me/threads")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["id"] == threads[0].id


@pytest.mark.asyncio
async def test_logged_user_change_username(logged_client):
    new_username = "NewUsername"
    response = await logged_client.post(f"{USERS_ENDPOINT}/me/username", json={
        "username": new_username
    })
    assert response.status_code == 200
    assert response.json()["new_username"] != TEST_USER.get("username")


@pytest.mark.asyncio
@pytest.mark.parametrize("username", [
    # 3 because of min length
    "a" * 2,
    # 20 because of max length
    "a" * 33,
    # Invalid characters
    "a@#$%^&*()_+",
])
async def test_logged_user_change_username_with_invalid_data(username, logged_client):
    response = await logged_client.post(f"{USERS_ENDPOINT}/me/username", json={
        "username": username
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_logged_user_change_username_with_already_taken_username(logged_client):
    response = await logged_client.post(f"{USERS_ENDPOINT}/me/username", json={
        "username": TEST_ADMIN_USER.get("username")
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_logged_user_change_password(logged_client):
    new_password = "newpassword123"
    response = await logged_client.post(f"{USERS_ENDPOINT}/me/password", json={
        "current_password": TEST_USER.get("password"),
        "new_password": new_password,
        "new_password2": new_password,
    })
    assert response.status_code == 200

    # Now try to login with new password
    auth_service = await _get_auth_service()
    token, user = await auth_service.login(
        form_data=OAuth2PasswordRequestForm(
            username=TEST_USER.get("username"),
            password=new_password,
            scope="",
        ),
        jwt_access_token_service=await get_access_token_service(settings),
        jwt_refresh_token_service=await get_refresh_token_service(settings),
    )

    assert token is not None


@pytest.mark.asyncio
async def test_logged_user_change_password_with_invalid_current_password(logged_client):
    password = "newpassword123"
    response = await logged_client.post(f"{USERS_ENDPOINT}/me/password", json={
        "current_password": "invalidpassword",
        "new_password": password,
        "new_password2": password,
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_logged_user_change_password_with_no_equal_password_and_password2(logged_client):
    pass1 = "newpassword123"
    pass2 = "newpassword1234"
    response = await logged_client.post(f"{USERS_ENDPOINT}/me/password", json={
        "current_password": TEST_USER.get("password"),
        "new_password": pass1,
        "new_password2": pass2,
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_logged_user_change_display_role(logged_client):
    users_service = await get_users_service()
    roles_service = await get_roles_service()
    user = await users_service.get_one(username=TEST_USER.get("username"), related=["roles", "display_role"])
    old_display_role_id = user.display_role.id
    role = await roles_service.get_one(id=ProtectedDefaultRolesEnum.ADMIN.value)
    await user.roles.add(role)
    response = await logged_client.post(f"{USERS_ENDPOINT}/me/display-role", json={
        "role_id": role.id
    })
    assert response.status_code == 200
    assert response.json()["display_role"]["id"] != old_display_role_id


@pytest.mark.asyncio
async def test_logged_user_change_display_role_with_invalid_role_id(logged_client):
    response = await logged_client.post(f"{USERS_ENDPOINT}/me/display-role", json={
        "role_id": 9999
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_logged_user_change_display_role_when_role_not_exists_in_user_roles(logged_client):
    response = await logged_client.post(f"{USERS_ENDPOINT}/me/display-role", json={
        "role_id": ProtectedDefaultRolesEnum.ADMIN.value
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_last_logged_users(client):
    response = await client.get(f"{USERS_ENDPOINT}/online")
    assert response.status_code == 200
    # 0 because nobody is logged in
    assert response.json()["total"] == 0
    # Now login user
    auth_service = await _get_auth_service()
    token, user = await auth_service.login(
        form_data=OAuth2PasswordRequestForm(
            username=TEST_ADMIN_USER.get("username"),
            password=TEST_ADMIN_USER.get("password"),
            scope="",
        ),
        jwt_access_token_service=await get_access_token_service(settings),
        jwt_refresh_token_service=await get_refresh_token_service(settings),
    )
    response = await client.get(f"{USERS_ENDPOINT}/online")
    assert response.status_code == 200
    # 1 because now user is logged in
    assert response.json()["total"] == 1
    # Mock datetime to 16 minutes later, because this
    with mock.patch('src.users.services.now_datetime',
                    return_value=datetime.now() + timedelta(
                        minutes=16)):
        response = await client.get(f"{USERS_ENDPOINT}/online")
        assert response.status_code == 200
        # 0 because now user don't make any actions
        assert response.json()["total"] == 0


@pytest.mark.asyncio
async def test_not_found_user(client):
    response = await client.get(f"{USERS_ENDPOINT}/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_user_threads(logged_client):
    users_service = await get_users_service()
    categories = await create_fake_categories(1)
    author = await users_service.get_one(username=TEST_USER.get("username"))
    threads = await create_fake_threads(1, author, categories[0])
    response = await logged_client.get(f"{USERS_ENDPOINT}/{author.id}/threads")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["id"] == threads[0].id


@pytest.mark.asyncio
async def test_get_user_posts(logged_client):
    users_service = await get_users_service()
    author = await users_service.get_one(username=TEST_USER.get("username"))
    posts = await create_fake_posts(1, author)
    response = await logged_client.get(f"{USERS_ENDPOINT}/{author.id}/posts")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["id"] == posts[0].id


@pytest.mark.asyncio
@pytest.mark.parametrize("filename", ["default_avatar.png", "default_avatar.jpg", "default_avatar.jpeg"])
async def test_logged_user_upload_avatar(filename, logged_client):
    # get path to static/images/default_avatar.png
    image_file, image_bytes = create_fake_image()
    response = await logged_client.get(f"{USERS_ENDPOINT}/me")
    assert response.status_code == 200

    old_avatar_url = response.json()["avatar"]

    response = await logged_client.post(f"{USERS_ENDPOINT}/me/avatar",
                                        files={"avatar": (filename, image_bytes, "image/png")})
    assert response.status_code == 200

    response = await logged_client.get(f"{USERS_ENDPOINT}/me")
    assert response.status_code == 200
    assert response.json()["avatar"] != old_avatar_url


@pytest.mark.asyncio
@pytest.mark.parametrize("content_type", [
    # Invalid: Missing "image/"
    "gif",
    "jpeg",
    "png",

    # Invalid: Incorrect content type for images
    "application/octet-stream",

    # Invalid: Invalid characters
    "image/gif; charset=utf-8",
    "image/jpeg; boundary=something",
    "image/png; encoding=base64",

    # Invalid: Content type with extra spaces
    "  image/gif  ",
    "image/png  ",

    # Invalid: Unsupported content types
    "image/bmp",
    "image/tiff",
    "image/svg+xml",

    # Invalid: Empty content type
    "",

    # Invalid: Content type with invalid characters
    "image/gif<",
    "image/jpeg;",
    "image/png?",
])
async def test_logged_user_upload_avatar_with_invalid_content_type(content_type, logged_client):
    image_file, image_bytes = create_fake_image()

    response = await logged_client.post(f"{USERS_ENDPOINT}/me/avatar",
                                        files={"avatar": ("default_avatar", image_bytes, content_type)})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_logged_user_upload_avatar_with_invalid_file_with_valid_content_type(logged_client):
    image_bytes = create_fake_invalid_image()

    response = await logged_client.post(f"{USERS_ENDPOINT}/me/avatar",
                                        files={"avatar": ("default_avatar.png", image_bytes, "image/png")})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_logged_user_upload_avatar_with_invalid_file_size(logged_client):
    image_bytes = create_fake_invalid_image(additional_bytes=1000)
    response = await logged_client.post(f"{USERS_ENDPOINT}/me/avatar",
                                            files={"avatar": ("default_avatar.png", image_bytes, "image/png")})
    assert response.status_code == 422
