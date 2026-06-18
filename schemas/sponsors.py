from pydantic import BaseModel, ConfigDict
from typing import Optional


class SponsorBase(BaseModel):
    name: str
    logo_url: str


# CREATE
class SponsorCreate(SponsorBase):
    pass


# UPDATE (partial update)
class SponsorUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None


# RESPONSE (ce returnezi din API)
class SponsorResponse(SponsorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)