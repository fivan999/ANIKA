from typing import Annotated

from fastapi import Depends

from src.utils.tokens import get_jwt_bearer_token


JWTTokenDep = Annotated[str, Depends(get_jwt_bearer_token)]
