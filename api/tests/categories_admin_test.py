import pytest

from src.forum.enums import CategoryTypeEnum
from tests.conftest import create_fake_categories, TEST_CATEGORY

ADMIN_CATEGORIES_ENDPOINT = "/v1/admin/forum/categories"


@pytest.mark.asyncio
async def test_unauthorized_admin_create_category(client):
    r = await client.post(ADMIN_CATEGORIES_ENDPOINT, json={
        "name": TEST_CATEGORY.get("name"),
        "description": TEST_CATEGORY.get("description"),
        "type": TEST_CATEGORY.get("type")
    })
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_admin_delete_category(client):
    categories = await create_fake_categories(1)
    r = await client.delete(ADMIN_CATEGORIES_ENDPOINT + f"/{categories[0].id}")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_admin_delete_category(admin_client):
    categories = await create_fake_categories(1)
    r = await admin_client.delete(ADMIN_CATEGORIES_ENDPOINT + f"/{categories[0].id}")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_admin_delete_invalid_category(admin_client):
    r = await admin_client.delete(ADMIN_CATEGORIES_ENDPOINT + "/1")
    assert r.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize("category_type", [CategoryTypeEnum.PUBLIC.value, CategoryTypeEnum.APPLICATION.value])
async def test_admin_create_category(admin_client, category_type):
    r = await admin_client.post(ADMIN_CATEGORIES_ENDPOINT, json={
        "name": TEST_CATEGORY.get("name"),
        "description": TEST_CATEGORY.get("description"),
        "type": category_type
    })
    assert r.status_code == 200
    assert "id" in r.json()
    assert "name" in r.json()
    assert "description" in r.json()
    assert r.json()["name"] == TEST_CATEGORY.get("name")
    assert r.json()["description"] == TEST_CATEGORY.get("description")
    assert r.json()["type"] == category_type
