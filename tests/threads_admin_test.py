import pytest
from fastapi import Security

from src.auth.dependencies import get_admin_user
from src.forum.exceptions import thread_not_found_exception
from src.forum.models import Thread
from src.forum.views.admin.threads import admin_delete_thread


@pytest.mark.asyncio
@pytest.mark.skip
async def test_admin_delete_thread():
    thread = await Thread.objects.get_or_create(
        id=1, title="test", category=1, author=1, content="test"
    )
    user = Security(get_admin_user, scopes=["threads:delete"])
    response = await admin_delete_thread(1, user)
    assert response == {"message": "Thread deleted successfully"}
    with pytest.raises(thread_not_found_exception):
        await admin_delete_thread(2, user)
