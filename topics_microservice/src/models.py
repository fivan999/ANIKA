from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    declarative_mixin,
    mapped_column,
    relationship,
)

from src.database import Base


@declarative_mixin
class BaseEntity:
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)


class Partner(Base, BaseEntity):
    __tablename__ = 'partners'

    topics: Mapped[List['Topic']] = relationship(
        'Topic',
        back_populates='partner',
        cascade='all, delete-orphan',
        lazy='selectin',
    )
    permissions: Mapped[List['Permission']] = relationship(
        'Permission',
        back_populates='partner',
        lazy='selectin',
    )
    subscriptions: Mapped[List['Subscription']] = relationship(
        'Subscription',
        back_populates='partner',
        lazy='selectin',
    )


class Topic(Base, BaseEntity):
    __tablename__ = 'topics'

    partner_id: Mapped[int] = mapped_column(ForeignKey('partners.id'))
    partner: Mapped['Partner'] = relationship(
        'Partner',
        back_populates='topics',
        lazy='selectin',
    )

    permissions: Mapped[List['Permission']] = relationship(
        'Permission',
        back_populates='topic',
        lazy='selectin',
    )
    subscriptions: Mapped[List['Subscription']] = relationship(
        'Subscription',
        back_populates='topic',
        lazy='selectin',
    )
    json_template: Mapped[str] = mapped_column()


class Permission(Base):
    __tablename__ = 'permissions'

    id: Mapped[int] = mapped_column(primary_key=True)

    topic_id: Mapped[int] = mapped_column(ForeignKey('topics.id'))
    topic: Mapped['Topic'] = relationship(
        'Topic',
        back_populates='permissions',
        lazy='selectin',
    )

    partner_id: Mapped[int] = mapped_column(ForeignKey('partners.id'))
    partner: Mapped['Partner'] = relationship(
        'Partner',
        back_populates='permissions',
        lazy='selectin',
    )


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]

    topic_id: Mapped[int] = mapped_column(ForeignKey('topics.id'))
    topic: Mapped['Topic'] = relationship(
        'Topic',
        back_populates='subscriptions',
        lazy='selectin',
    )

    partner_id: Mapped[int] = mapped_column(ForeignKey('partners.id'))
    partner: Mapped['Partner'] = relationship(
        'Partner',
        back_populates='subscriptions',
        lazy='selectin',
    )
