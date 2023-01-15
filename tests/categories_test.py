import pytest

from tests.conftest import create_fake_categories


@pytest.mark.asyncio
async def test_get_empty_categories(client):
    r = await client.get("/forum/categories")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_categories(client):
    categories = await create_fake_categories()
    r = await client.get("/forum/categories")
    assert r.status_code == 200
    assert r.json()["total"] == 50


@pytest.mark.asyncio
async def test_get_category(client):
    category = await create_fake_categories(1)
    r = await client.get(f"/forum/categories/{category[0].id}")
    assert r.status_code == 200
    assert r.json()["name"] == category[0].name


@pytest.mark.asyncio
async def test_get_invalid_category(client):
    r = await client.get("/forum/categories/1")
    assert r.status_code == 404
