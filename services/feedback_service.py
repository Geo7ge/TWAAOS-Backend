from supabase import create_client
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

from schemas.feedback import FeedbackCreate

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


class FeedbackService:
    @staticmethod
    def get_all_feedback():
        """Get all feedback"""
        supabase = get_supabase_client()

        result = supabase.table("feedback").select("*").execute()

        return result.data if result.data else []
    
    @staticmethod
    def get_feedback_by_id(feedback_id: int):
        """Get feedback by ID"""
        supabase = get_supabase_client()

        result = (
            supabase
            .table("feedback")
            .select("*")
            .eq("id", feedback_id)
            .execute()
        )

        if not result.data:
            return None

        return result.data[0]
    
    @staticmethod
    def get_feedback_by_user(user_id: int):
        """Get all feedback for a specific user"""
        supabase = get_supabase_client()

        result = (
            supabase
            .table("feedback")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        return result.data if result.data else []


    @staticmethod
    def create_feedback(user_id: int, feedback_data: FeedbackCreate):
        """Create feedback"""
        supabase = get_supabase_client()

        feedback_dict = feedback_data.model_dump()
        feedback_dict["user_id"] = user_id
        feedback_dict["created_at"] = datetime.now(timezone.utc).isoformat()

        result = supabase.table("feedback").insert(feedback_dict).execute()

        if not result.data:
            return None

        return result.data[0]




    @staticmethod
    def get_feedback_by_event(event_id: int):
        """Get all feedback for a specific event"""
        supabase = get_supabase_client()

        result = (
            supabase
            .table("feedback")
            .select("*")
            .eq("event_id", event_id)
            .execute()
        )

        return result.data if result.data else []

    @staticmethod
    def update_feedback(feedback_id: int, user_id: int, feedback_data: FeedbackCreate):
        """Update feedback (doar autorul îl poate modifica)"""
        supabase = get_supabase_client()

        # verificăm dacă feedback-ul există și aparține userului
        existing = (
            supabase
            .table("feedback")
            .select("*")
            .eq("id", feedback_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not existing.data:
            return None

        update_data = feedback_data.model_dump()

        result = (
            supabase
            .table("feedback")
            .update(update_data)
            .eq("id", feedback_id)
            .execute()
        )

        if not result.data:
            return None

        return result.data[0]

    @staticmethod
    def delete_feedback(feedback_id: int, user_id: int):
        """Delete feedback (doar autorul îl poate șterge)"""
        supabase = get_supabase_client()

        # verificare ownership
        existing = (
            supabase
            .table("feedback")
            .select("*")
            .eq("id", feedback_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not existing.data:
            return False

        supabase.table("feedback").delete().eq("id", feedback_id).execute()

        return True