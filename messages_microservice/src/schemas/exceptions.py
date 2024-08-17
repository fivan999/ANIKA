from fastapi import HTTPException

HeadersNotFound = HTTPException(status_code=400, detail="Auth headers not found")

PermissionsError = HTTPException(
    status_code=403,
    detail="You do not have sufficient permissions to perform this operation."
)

TooManyNotifier= HTTPException(
    status_code=429,
    detail="Too many message for notify."
)

TimeOutException = HTTPException(
    status_code=504,
    detail="The request timed out. Please try again later."
)
