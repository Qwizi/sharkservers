import pytest

from src.roles.enums import ProtectedDefaultRolesEnum

SCOPES_ENDPOINT = "/v1/scopes"


@pytest.mark.asyncio
async def test_get_all_scopes(client):
    r = await client.get(SCOPES_ENDPOINT)
    assert r.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("role_id", [
    ProtectedDefaultRolesEnum.ADMIN.value,
    ProtectedDefaultRolesEnum.USER.value,
    ProtectedDefaultRolesEnum.BANNED.value,
])
async def test_get_scopes_by_role_id(role_id, client):
    r = await client.get(SCOPES_ENDPOINT + f"?role_id={role_id}")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_scopes_by_role_id_not_found(client):
    r = await client.get(SCOPES_ENDPOINT + f"?role_id=999999")
    assert r.status_code == 200
    assert r.json()["total"] == 0
