from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    partner_id: Mapped[int] = mapped_column()
