import pytest
from starlette import status

from app.roles.utils import create_default_roles
from app.scopes.models import Scope
from app.scopes.utils import create_scopes


@pytest.mark.asyncio
async def test_scopes_list(client, faker):
    await create_scopes()
    r = await client.get("/scopes")
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert "app_name" in data["items"][0]
    item_found = False
    for item in data["items"]:
        if item["app_name"] == "users" and item["value"] == "me":
            item_found = True
            break
    assert item_found is True
    scopes = await Scope.objects.all()
    assert len(scopes) == data["total"]


@pytest.mark.asyncio
@pytest.mark.parametrize("role_id", [1, 2])
async def test_scopes_list_with_role_id(role_id, client):
    await create_scopes()
    await create_default_roles()
    r = await client.get(f"/scopes?role_id={role_id}")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_scopes_list_with_invalid_role_id(client):
    await create_scopes()
    r = await client.get("/scopes?role_id=-1")
    assert r.status_code == 200
    assert r.json()["total"] == 0
