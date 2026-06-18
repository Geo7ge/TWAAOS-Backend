from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    location_id: Optional[int] = None
    category_name: Optional[str] = None
    organizer_id: Optional[int] = None

    participation_type: Optional[str] = None
    registration_link: Optional[str] = None
    qr_code: Optional[str] = None

    max_participants: Optional[int] = None
    deadline: Optional[datetime] = None


# CREATE
class EventCreate(EventBase):
    pass


# UPDATE (partial update pentru CRUD real)
class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    location_id: Optional[int] = None
    category_name: Optional[str] = None
    organizer_id: Optional[int] = None

    participation_type: Optional[str] = None
    registration_link: Optional[str] = None
    qr_code: Optional[str] = None

    max_participants: Optional[int] = None
    deadline: Optional[datetime] = None


# RESPONSE (ce trimiți către frontend)
class EventResponse(EventBase):
    id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)