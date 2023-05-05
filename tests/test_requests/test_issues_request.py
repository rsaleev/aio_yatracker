from tests.conftest import get_client
import pytest

@pytest.mark.parametrize("issue_id", ("SSTGARBAGE-441",))
async def test_user_request(get_client, issue_id):
    response = await get_client.get(url=f"issues/{issue_id}")
    assert response
