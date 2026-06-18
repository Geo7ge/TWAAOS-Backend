from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class FeedbackBase(BaseModel):
    event_id: int
    rating: int = Field(ge=1, le=5)  # rating între 1 și 5
    comment: str | None = None


class FeedbackCreate(FeedbackBase):
    pass  # user_id îl iei din token (nu din request body)


class FeedbackResponse(FeedbackBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)