from pydantic import BaseModel, ConfigDict
from typing import Optional


class EventSponsorBase(BaseModel):
    event_id: int
    sponsor_id: int


class EventSponsorCreate(EventSponsorBase):
    pass


class EventSponsorUpdate(BaseModel):
    event_id: Optional[int] = None
    sponsor_id: Optional[int] = None


class EventSponsorResponse(EventSponsorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)