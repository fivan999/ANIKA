from typing import Annotated

from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


def get_jwt_bearer_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(HTTPBearer()),
    ],
) -> str:
    return credentials.credentials


JWTTokenDep = Annotated[str, Depends(get_jwt_bearer_token)]


async def get_current_partner_id(
    token: JWTTokenDep,  # noqa: ARG001
    x_partner_id: int = Header(None),
) -> int:
    if x_partner_id is None:
        raise HTTPException(
            status_code=401,
            detail='Partner ID must be provided',
        )

    return int(x_partner_id)
