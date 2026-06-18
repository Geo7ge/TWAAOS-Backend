from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class FileBase(BaseModel):
    event_id: int
    file_url: str
    file_type: str  # pdf | image | presentation


class FileCreate(FileBase):
    pass


class FileUpdate(BaseModel):
    event_id: Optional[int] = None
    file_url: Optional[str] = None
    file_type: Optional[str] = None


class FileResponse(FileBase):
    id: int
    uploaded_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)