import pytest
from starlette import status

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
