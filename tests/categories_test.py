import pytest


@pytest.mark.asyncio
async def test_get_categories(client, mocker):
    mocker.patch("shark_api.forum.utils._get_categories", return_value=[])
    response = await client.get("/categories")
    assert response.status_code == 200
    assert response.json() == {"items": [], "page": 1, "pages": 1, "total": 0}
