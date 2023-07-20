import pytest

ADMIN_SCOPES_ENDPOINT = "/v1/admin/scopes"


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint", [
    ADMIN_SCOPES_ENDPOINT,
    ADMIN_SCOPES_ENDPOINT + "/1",
])
async def test_unauthorized_admin_get_scopes(endpoint, client):
    r = await client.get(endpoint)
    assert r.status_code == 401
