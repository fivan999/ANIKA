import pytest
from httpx import AsyncClient

from src.models.users import User


@pytest.mark.asyncio
async def test_success_login(
    fastapi_test_client: AsyncClient, user1: User
) -> None:
    response = await fastapi_test_client.post(
        url='/auth/token',
        json={'username': 'user1', 'password': 'password1'},
    )
    response_json = response.json()
    assert response.status_code == 200
    assert 'access_token' in response_json
    assert 'refresh_token' in response_json


@pytest.mark.asyncio
async def test_login_incorrect_user(
    fastapi_test_client: AsyncClient, user1: User
) -> None:
    response = await fastapi_test_client.post(
        url='/auth/token',
        json={'username': 'user2', 'password': 'password1'},
    )
    response_json = response.json()
    assert response.status_code == 403
    assert 'access_token' not in response_json
    assert 'refresh_token' not in response_json
