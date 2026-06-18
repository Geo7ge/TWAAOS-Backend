from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class RegistrationBase(BaseModel):
    user_id: int
    event_id: int
    status: str = "pending"   # ex: pending / approved / rejected


# CREATE
class RegistrationCreate(RegistrationBase):
    pass


# UPDATE (partial)
class RegistrationUpdate(BaseModel):
    status: Optional[str] = None


# RESPONSE
class RegistrationResponse(RegistrationBase):
    id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)