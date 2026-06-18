from supabase import create_client
from schemas.sponsors import SponsorCreate, SponsorUpdate
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client():
    """Get Supabase client"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


class SponsorService:
    @staticmethod
    def create_sponsor(sponsor_data: SponsorCreate):
        """Create new sponsor"""
        supabase = get_supabase_client()

        sponsor_dict = sponsor_data.model_dump()
        sponsor_dict["created_at"] = datetime.now(timezone.utc).isoformat()

        result = supabase.table("sponsors").insert(sponsor_dict).execute()

        if not result.data:
            return None

        return result.data[0]

    @staticmethod
    def get_all_sponsors():
        """Get all sponsors"""
        supabase = get_supabase_client()

        result = supabase.table("sponsors").select("*").execute()

        if not result.data:
            return []

        return result.data

    @staticmethod
    def get_sponsor_by_id(sponsor_id: int):
        """Get sponsor by ID"""
        supabase = get_supabase_client()

        result = (
            supabase.table("sponsors")
            .select("*")
            .eq("id", sponsor_id)
            .execute()
        )

        if not result.data:
            return None

        return result.data[0]

    @staticmethod
    def update_sponsor(sponsor_id: int, sponsor_data: SponsorUpdate):
        """Update sponsor"""
        supabase = get_supabase_client()

        existing_sponsor = (
            supabase.table("sponsors")
            .select("*")
            .eq("id", sponsor_id)
            .execute()
        )

        if not existing_sponsor.data:
            return None

        update_data = sponsor_data.model_dump(exclude_unset=True)

        if not update_data:
            return existing_sponsor.data[0]

        result = (
            supabase.table("sponsors")
            .update(update_data)
            .eq("id", sponsor_id)
            .execute()
        )

        if not result.data:
            return None

        return result.data[0]

    @staticmethod
    def delete_sponsor(sponsor_id: int):
        """Delete sponsor"""
        supabase = get_supabase_client()

        existing_sponsor = (
            supabase.table("sponsors")
            .select("*")
            .eq("id", sponsor_id)
            .execute()
        )

        if not existing_sponsor.data:
            return None

        result = (
            supabase.table("sponsors")
            .delete()
            .eq("id", sponsor_id)
            .execute()
        )

        if not result.data:
            return None

        return {
            "message": "Sponsor deleted successfully",
            "deleted_sponsor": result.data[0]
        }