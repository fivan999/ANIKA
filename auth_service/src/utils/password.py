from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Comparing password and hashed password

    Args:
        password (str)
        hashed_password (str)

    Returns:
        bool: are passwords equal
    """
    return pwd_context.verify(password, hashed_password)


def get_hashed_password(password: str) -> str:
    """
    Getting hashed value of a password

    Args:
        password (str)

    Returns:
        str: hashed passsword
    """
    return pwd_context.hash(password)
