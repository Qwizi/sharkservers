import pytest

from tests.conftest import create_fake_categories

CATEGORIES_ENDPOINT = "/v1/forum/categories"


@pytest.mark.asyncio
async def test_get_empty_categories(client):
    r = await client.get(CATEGORIES_ENDPOINT)
    assert r.status_code == 200
    assert r.json()["total"] == 0


@pytest.mark.asyncio
async def test_get_categories(client):
    await create_fake_categories()
    r = await client.get(CATEGORIES_ENDPOINT)
    assert r.status_code == 200
    assert r.json()["total"] == 50


@pytest.mark.asyncio
async def test_get_category(client):
    category = await create_fake_categories(1)
    r = await client.get(f"{CATEGORIES_ENDPOINT}/{category[0].id}")
    assert r.status_code == 200
    assert "id" in r.json()
    assert "name" in r.json()
    assert "description" in r.json()
    assert r.json()["name"] == category[0].name


@pytest.mark.asyncio
async def test_get_invalid_category(client):
    r = await client.get(CATEGORIES_ENDPOINT + "/1")
    assert r.status_code == 404
