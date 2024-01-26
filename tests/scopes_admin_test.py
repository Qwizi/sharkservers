import pytest

from tests.conftest import TEST_SCOPE, create_fake_scopes

ADMIN_SCOPES_ENDPOINT = "/v1/admin/scopes"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "endpoint",
    [
        ADMIN_SCOPES_ENDPOINT,
        ADMIN_SCOPES_ENDPOINT + "/1",
    ],
)
async def test_unauthorized_admin_get_scopes(endpoint, client):
    r = await client.get(endpoint)
    assert r.status_code == 401


@pytest.mark.anyio
async def test_unauthorized_admin_create_scope(client):
    r = await client.post(ADMIN_SCOPES_ENDPOINT)
    assert r.status_code == 401


@pytest.mark.anyio
async def test_unauthorized_admin_delete_scope(client):
    r = await client.delete(ADMIN_SCOPES_ENDPOINT + "/1")
    assert r.status_code == 401


@pytest.mark.anyio
async def test_unauthorized_admin_update_scope(client):
    r = await client.put(ADMIN_SCOPES_ENDPOINT + "/1")
    assert r.status_code == 401


@pytest.mark.anyio
async def test_admin_get_all_scopes(admin_client):
    r = await admin_client.get(ADMIN_SCOPES_ENDPOINT)
    assert r.status_code == 200


@pytest.mark.anyio
async def test_admin_get_scope(admin_client):
    r = await admin_client.get(ADMIN_SCOPES_ENDPOINT + "/1")
    assert r.status_code == 200


@pytest.mark.anyio
@pytest.mark.parametrize("protected", [True, False])
async def test_admin_create_scope(protected, admin_client):
    r = await admin_client.post(
        ADMIN_SCOPES_ENDPOINT,
        json={
            "app_name": TEST_SCOPE.get("app_name"),
            "value": TEST_SCOPE.get("value"),
            "description": TEST_SCOPE.get("description"),
            "protected": protected,
        },
    )
    assert r.status_code == 200
    assert r.json()["app_name"] == TEST_SCOPE.get("app_name")
    assert r.json()["value"] == TEST_SCOPE.get("value")
    assert r.json()["description"] == TEST_SCOPE.get("description")
    if protected:
        assert r.json()["protected"] is True
    else:
        assert r.json()["protected"] is False


@pytest.mark.anyio
async def test_admin_delete_scope(admin_client):
    scopes = await create_fake_scopes(1)
    r = await admin_client.delete(ADMIN_SCOPES_ENDPOINT + f"/{scopes[0].id}")
    assert r.status_code == 200


@pytest.mark.anyio
async def test_admin_update_scope(admin_client):
    scopes = await create_fake_scopes(1)
    old_app_name = scopes[0].app_name
    new_app_name = "new_app_name"
    r = await admin_client.put(
        ADMIN_SCOPES_ENDPOINT + f"/{scopes[0].id}",
        json={
            "app_name": new_app_name,
        },
    )
    assert r.status_code == 200
    assert r.json()["app_name"] != old_app_name
