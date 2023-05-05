from tests.conftest import get_client


async def test_user_request(get_client):
    response = await get_client.get(url="myself")
    assert response


async def test_users_request(get_client):
    response = await get_client.get(url="users")
    assert response
    assert len(response) > 50
