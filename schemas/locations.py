from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class LocationBase(BaseModel):
    name: str
    address: str
    city: str


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None


class LocationResponse(LocationBase):
    id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)