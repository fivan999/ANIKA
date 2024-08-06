import datetime

import freezegun
import pytest
from httpx import AsyncClient

from src.dependencies.config import jwt_config
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
async def test_login_incorrect_username(
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


@pytest.mark.asyncio
async def test_login_incorrect_password(
    fastapi_test_client: AsyncClient, user1: User
) -> None:
    response = await fastapi_test_client.post(
        url='/auth/token',
        json={'username': 'user1', 'password': 'password2'},
    )
    response_json = response.json()
    assert response.status_code == 403
    assert 'access_token' not in response_json
    assert 'refresh_token' not in response_json


@pytest.mark.asyncio
async def test_get_authorization_data_by_access_token(
    fastapi_test_client: AsyncClient, access_and_refresh_token1: dict[str, str]
) -> None:
    access_token = access_and_refresh_token1.get('access_token', 'fake')
    response = await fastapi_test_client.get(
        url='/auth/authorization',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json.get('user_id', 0) == 1
    assert response_json.get('partner_id', 0) == 1


@pytest.mark.asyncio
async def test_get_access_token_by_refresh_token(
    fastapi_test_client: AsyncClient, access_and_refresh_token1: dict[str, str]
) -> None:
    refresh_token = access_and_refresh_token1.get('refresh_token', 'fake')
    response = await fastapi_test_client.post(
        url='/auth/refresh', json={'refresh_token': refresh_token}
    )
    response_json = response.json()
    assert response.status_code == 200
    assert 'access_token' in response_json


@pytest.mark.asyncio
async def test_get_authorization_by_invalid_access_token(
    fastapi_test_client: AsyncClient, user1: User
) -> None:
    response = await fastapi_test_client.get(
        url='/auth/authorization', headers={'Authorization': 'Bearer aboba'}
    )
    response_json = response.json()
    assert response.status_code == 401
    assert 'user_id' not in response_json
    assert 'partner_id' not in response_json


@pytest.mark.asyncio
async def test_get_authorization_by_expired_access_token(
    fastapi_test_client: AsyncClient, access_and_refresh_token1: User
) -> None:
    access_token = access_and_refresh_token1.get('access_token', 'fake')
    mock_datetime = datetime.datetime.now(
        datetime.timezone.utc
    ) + datetime.timedelta(minutes=jwt_config.access_token_expire_minutes + 1)
    with freezegun.freeze_time(mock_datetime):
        response = await fastapi_test_client.get(
            url='/auth/authorization',
            headers={'Authorization': f'Bearer {access_token}'},
        )
    response_json = response.json()
    assert response.status_code == 401
    assert 'user_id' not in response_json
    assert 'partner_id' not in response_json


@pytest.mark.asyncio
async def test_get_access_token_by_expired_refresh_token(
    fastapi_test_client: AsyncClient, access_and_refresh_token1: User
) -> None:
    refresh_token = access_and_refresh_token1.get('refresh_token', 'fake')
    mock_datetime = datetime.datetime.now(
        datetime.timezone.utc
    ) + datetime.timedelta(minutes=jwt_config.refresh_token_expire_minutes + 1)
    with freezegun.freeze_time(mock_datetime):
        response = await fastapi_test_client.post(
            url='/auth/refresh',
            json={'refresh_token': refresh_token},
        )
    response_json = response.json()
    assert response.status_code == 403
    assert 'access_token' not in response_json
