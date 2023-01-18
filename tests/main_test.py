import os

import pytest

from src.roles.models import Role
from src.users.models import User
from tests.auth_test import TEST_REGISTER_USER
from src.main import installed_file_path


@pytest.mark.asyncio
async def test_install(client):
    install_file_exists = False
    if os.path.exists(installed_file_path):
        install_file_exists = True
        os.remove(installed_file_path)
    r = await client.post("/install", json=TEST_REGISTER_USER)
    assert r.status_code == 200

    admin_user = await User.objects.select_related(["display_role", "roles"]).get(id=1)
    admin_role = await Role.objects.get(id=1)
    assert admin_user.id == 1
    assert admin_role.id == 1
    assert admin_user.display_role == admin_role
    assert admin_role in admin_user.roles

    if install_file_exists:
        install_finish_file = open(installed_file_path, "w+")


@pytest.mark.asyncio
async def test_install_when_is_already_installed(client):
    install_file_exists = True if os.path.exists(installed_file_path) else False
    install_finish_file = open(installed_file_path, "w+")
    r = await client.post("/install", json=TEST_REGISTER_USER)
    assert r.status_code == 400
    if not install_file_exists:
        os.remove(installed_file_path)
