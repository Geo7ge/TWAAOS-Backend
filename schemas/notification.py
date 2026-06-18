from pydantic import BaseModel, ConfigDict
from datetime import datetime


class NotificationBase(BaseModel):
    event_id: int
    message: str
    is_read: bool = False


class NotificationCreate(NotificationBase):
    pass  # user_id vine din token


class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)