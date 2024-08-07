from pydantic import BaseModel


class SubscriptionBase(BaseModel):
    topic_id: int
    url: str


class SubscriptionCreate(SubscriptionBase):
    pass


class Subscription(SubscriptionBase):
    id: int
    partner_id: int

    class Config:
        from_attributes = True


class PermissionBase(BaseModel):
    pass


class PermissionCreate(PermissionBase):
    topic_id: int
    partner_id: int


class Permission(PermissionBase):
    id: int
    topic_id: int
    partner_id: int

    class Config:
        from_attributes = True


class TopicBase(BaseModel):
    name: str
    description: str | None = None


class TopicCreate(TopicBase):
    pass


class TopicUpdate(TopicBase):
    name: str | None = None
    description: str | None = None


class Topic(TopicBase):
    id: int
    partner_id: int
    subscriptions: list[Subscription] = []
    permissions: list[Permission] = []

    class Config:
        from_attributes = True
