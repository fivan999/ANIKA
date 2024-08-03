from fastapi import HTTPException

HeadersNotFound = HTTPException(status_code=400, detail="Auth headers not found")

PermissionsError = HTTPException(
    status_code=403,
    detail="You do not have sufficient permissions to perform this operation."
)
