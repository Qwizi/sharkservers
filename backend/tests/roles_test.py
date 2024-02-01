import pytest

from sharkservers.roles.enums import ProtectedDefaultRolesEnum
from sharkservers.scopes.dependencies import get_scopes_service
from sharkservers.scopes.services import ScopeService

ROLES_ENDPOINT = "/v1/roles"


@pytest.mark.anyio
async def test_get_roles(client):
    r = await client.get(ROLES_ENDPOINT)
    assert r.status_code == 200
    # 3 default roles [Admin, User, Banned, Vip]
    assert r.json()["total"] == 4


@pytest.mark.anyio
@pytest.mark.parametrize(
    "default_roles_id",
    [
        ProtectedDefaultRolesEnum.ADMIN.value,
        ProtectedDefaultRolesEnum.USER.value,
        ProtectedDefaultRolesEnum.BANNED.value,
    ],
)
async def test_get_default_role(default_roles_id, client):
    r = await client.get(f"{ROLES_ENDPOINT}/{default_roles_id}")
    assert r.status_code == 200
    assert r.json()["id"] == default_roles_id

    scopes_service: ScopeService = await get_scopes_service()
    if default_roles_id == ProtectedDefaultRolesEnum.ADMIN.value:
        admin_scopes = await scopes_service.get_default_scopes_for_role(
            ProtectedDefaultRolesEnum.ADMIN.value
        )
        assert r.json()["name"] == "Admin"
        assert r.json()["color"] == "#C53030"
        assert len(r.json()["scopes"]) == len(admin_scopes)
    elif default_roles_id == ProtectedDefaultRolesEnum.USER.value:
        user_roles = await scopes_service.get_default_scopes_for_role(
            ProtectedDefaultRolesEnum.USER.value
        )
        assert r.json()["name"] == "User"
        assert r.json()["color"] == "#99999"
        assert len(r.json()["scopes"]) == len(user_roles)
    elif default_roles_id == ProtectedDefaultRolesEnum.BANNED.value:
        assert r.json()["name"] == "Banned"
        assert r.json()["color"] == "#000000"
        assert len(r.json()["scopes"]) == 0


@pytest.mark.anyio
async def test_get_invalid_role(client):
    r = await client.get(f"{ROLES_ENDPOINT}/9999")
    assert r.status_code == 404
