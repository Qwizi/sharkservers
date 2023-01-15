import pytest
from fastapi import Security

from shark_api.auth.utils import get_admin_user
from shark_api.forum.exceptions import thread_not_found_exception
from shark_api.forum.models import Thread
from shark_api.forum.views.admin.threads import admin_delete_thread


@pytest.mark.asyncio
@pytest.mark.skip
async def test_admin_delete_thread():
    thread = await Thread.objects.get_or_create(id=1, title="test", category=1, author=1, content="test")
    user = Security(get_admin_user, scopes=["threads:delete"])
    response = await admin_delete_thread(1, user)
    assert response == {"message": "Thread deleted successfully"}
    with pytest.raises(thread_not_found_exception):
        await admin_delete_thread(2, user)
