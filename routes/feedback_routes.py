from fastapi import APIRouter, HTTPException, status, Depends
import jwt
import os

from schemas.feedback import FeedbackCreate, FeedbackResponse
from services.feedback_service import FeedbackService

router = APIRouter(prefix="/feedback", tags=["feedback"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


# 🔐 helper pentru extragerea user_id din token
def get_current_user_id(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# ✅ GET all feedback
@router.get("/", response_model=list[FeedbackResponse])
def get_all_feedback():
    return FeedbackService.get_all_feedback()

# ✅ GET feedback by ID
@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(feedback_id: int):
    feedback = FeedbackService.get_feedback_by_id(feedback_id)

    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    return feedback

@router.get("/user/{user_id}", response_model=list[FeedbackResponse])
def get_feedback_by_user(user_id: int):
    """Get all feedback created by a user"""
    return FeedbackService.get_feedback_by_user(user_id)
# ✅ CREATE feedback
@router.post(
    "/",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_feedback(feedback_data: FeedbackCreate, token: str):
    user_id = get_current_user_id(token)

    feedback = FeedbackService.create_feedback(user_id, feedback_data)

    if not feedback:
        raise HTTPException(status_code=400, detail="Could not create feedback")

    return feedback

# ✅ GET feedback by EVENT ID
@router.get("/event/{event_id}", response_model=list[FeedbackResponse])
def get_feedback_by_event(event_id: int):
    return FeedbackService.get_feedback_by_event(event_id)


# ✅ UPDATE feedback
@router.put("/{feedback_id}", response_model=FeedbackResponse)
def update_feedback(feedback_id: int, feedback_data: FeedbackCreate, token: str):
    user_id = get_current_user_id(token)

    feedback = FeedbackService.update_feedback(
        feedback_id, user_id, feedback_data
    )

    if not feedback:
        raise HTTPException(
            status_code=404,
            detail="Feedback not found or not authorized",
        )

    return feedback


# ✅ DELETE feedback
@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_feedback(feedback_id: int, token: str):
    user_id = get_current_user_id(token)

    success = FeedbackService.delete_feedback(feedback_id, user_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Feedback not found or not authorized",
        )

    return