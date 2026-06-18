from supabase import create_client
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

from schemas.notification import NotificationCreate

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


class NotificationService:

    @staticmethod
    def create_notification(user_id: int, notification_data: NotificationCreate):
        supabase = get_supabase_client()

        data = notification_data.model_dump()
        data["user_id"] = user_id
        data["created_at"] = datetime.now(timezone.utc).isoformat()

        result = supabase.table("notifications").insert(data).execute()

        return result.data[0] if result.data else None

    @staticmethod
    def get_all_notifications():
        supabase = get_supabase_client()

        result = supabase.table("notifications").select("*").execute()
        return result.data if result.data else []

    @staticmethod
    def get_notification_by_id(notification_id: int):
        supabase = get_supabase_client()

        result = (
            supabase
            .table("notifications")
            .select("*")
            .eq("id", notification_id)
            .execute()
        )

        return result.data[0] if result.data else None

    @staticmethod
    def get_notifications_by_user(user_id: int):
        supabase = get_supabase_client()

        result = (
            supabase
            .table("notifications")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        return result.data if result.data else []

    @staticmethod
    def get_notifications_by_event(event_id: int):
        supabase = get_supabase_client()

        result = (
            supabase
            .table("notifications")
            .select("*")
            .eq("event_id", event_id)
            .execute()
        )

        return result.data if result.data else []

    @staticmethod
    def update_notification(notification_id: int, data: NotificationCreate):
        supabase = get_supabase_client()

        result = (
            supabase
            .table("notifications")
            .update(data.model_dump())
            .eq("id", notification_id)
            .execute()
        )

        return result.data[0] if result.data else None

    @staticmethod
    def delete_notification(notification_id: int):
        supabase = get_supabase_client()

        result = (
            supabase
            .table("notifications")
            .delete()
            .eq("id", notification_id)
            .execute()
        )

        return True if result else False