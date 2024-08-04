import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from src.models.users import User


@pytest.mark.asyncio
async def test_success_login(
    fastapi_application: FastAPI, user1: User
) -> None:
    """
    Test endpoint with success login

    Args:
        fastapi_application (FastAPI)
        user1 (User): test user
    """
    async with AsyncClient(
        app=fastapi_application, base_url='http://test'
    ) as client:
        response = await client.post(
            url='/auth/authorization',
            params={'username': 'user1', 'password': 'password1'},
        )
    response_json = response.json()
    assert response.status_code == 200
    assert 'access_token' in response_json
    assert 'refresh_token' in response_json
