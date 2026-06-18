from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os

from schemas.notification import NotificationCreate, NotificationResponse
from services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


# ✅ CREATE
@router.post("/", response_model=NotificationResponse, status_code=201)
def create_notification(
    data: NotificationCreate,
    user_id: int = Depends(get_current_user_id)
):
    notif = NotificationService.create_notification(user_id, data)

    if not notif:
        raise HTTPException(status_code=400, detail="Could not create notification")

    return notif


# ✅ GET ALL
@router.get("/", response_model=list[NotificationResponse])
def get_all_notifications():
    return NotificationService.get_all_notifications()


# ✅ GET BY ID
@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(notification_id: int):
    notif = NotificationService.get_notification_by_id(notification_id)

    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    return notif


# ✅ GET BY USER
@router.get("/user/{user_id}", response_model=list[NotificationResponse])
def get_notifications_by_user(user_id: int):
    return NotificationService.get_notifications_by_user(user_id)


# ✅ GET BY EVENT
@router.get("/event/{event_id}", response_model=list[NotificationResponse])
def get_notifications_by_event(event_id: int):
    return NotificationService.get_notifications_by_event(event_id)


# ✅ UPDATE
@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(notification_id: int, data: NotificationCreate):
    notif = NotificationService.update_notification(notification_id, data)

    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    return notif


# ✅ DELETE
@router.delete("/{notification_id}", status_code=204)
def delete_notification(notification_id: int):
    success = NotificationService.delete_notification(notification_id)

    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")

    return