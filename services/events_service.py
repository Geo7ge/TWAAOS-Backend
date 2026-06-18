from supabase import create_client
from schemas.events import EventCreate, EventUpdate
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client():
    """Get Supabase client"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


class EventService:
    @staticmethod
    def create_event(event_data: EventCreate):
        """Create new event"""
        supabase = get_supabase_client()

        event_dict = event_data.model_dump(mode="json")
        event_dict["created_at"] = datetime.now(timezone.utc).isoformat()

        result = supabase.table("events").insert(event_dict).execute()

        if not result.data:
            return None

        return result.data[0]

    @staticmethod
    def get_all_events():
        """Get all events"""
        supabase = get_supabase_client()

        result = supabase.table("events").select("*").execute()

        if not result.data:
            return []

        return result.data

    @staticmethod
    def get_event_by_id(event_id: int):
        """Get event by ID"""
        supabase = get_supabase_client()

        result = (
            supabase.table("events")
            .select("*")
            .eq("id", event_id)
            .execute()
        )

        if not result.data:
            return None

        return result.data[0]

    @staticmethod
    def update_event(event_id: int, event_data: EventUpdate):
        """Update event"""
        supabase = get_supabase_client()

        existing_event = (
            supabase.table("events")
            .select("*")
            .eq("id", event_id)
            .execute()
        )

        if not existing_event.data:
            return None

        update_data = event_data.model_dump(mode="json", exclude_unset=True)

        if not update_data:
            return existing_event.data[0]

        result = (
            supabase.table("events")
            .update(update_data)
            .eq("id", event_id)
            .execute()
        )

        if not result.data:
            return None

        return result.data[0]

    @staticmethod
    def delete_event(event_id: int):
        """Delete event"""
        supabase = get_supabase_client()

        existing_event = (
            supabase.table("events")
            .select("*")
            .eq("id", event_id)
            .execute()
        )

        if not existing_event.data:
            return None

        result = (
            supabase.table("events")
            .delete()
            .eq("id", event_id)
            .execute()
        )

        if not result.data:
            return None

        return {
            "message": "Event deleted successfully",
            "deleted_event": result.data[0]
        }