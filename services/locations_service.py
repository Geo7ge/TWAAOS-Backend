from supabase import create_client, Client
from schemas.locations import (
    LocationCreate,
    LocationUpdate,
)
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client():
    """Get Supabase client, create if not exists"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


class LocationService:
    @staticmethod
    def create_location(location_data: LocationCreate):
        """Create new location"""
        supabase = get_supabase_client()

        location_dict = location_data.model_dump()
        location_dict["created_at"] = datetime.now(timezone.utc).isoformat()

        result = supabase.table("locations").insert(location_dict).execute()

        if not result.data:
            return None

        return result.data[0]

    @staticmethod
    def get_all_locations():
        """Get all locations"""
        supabase = get_supabase_client()

        result = supabase.table("locations").select("*").execute()

        if not result.data:
            return []

        return result.data

    @staticmethod
    def get_location_by_id(location_id: int):
        """Get location by ID"""
        supabase = get_supabase_client()

        result = (
            supabase.table("locations")
            .select("*")
            .eq("id", location_id)
            .execute()
        )

        if not result.data:
            return None

        return result.data[0]

    @staticmethod
    def update_location(location_id: int, location_data: LocationUpdate):
        """Update location"""
        supabase = get_supabase_client()

        existing_location = (
            supabase.table("locations")
            .select("*")
            .eq("id", location_id)
            .execute()
        )

        if not existing_location.data:
            return None

        update_data = location_data.model_dump(exclude_unset=True)

        if not update_data:
            return existing_location.data[0]

        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

        result = (
            supabase.table("locations")
            .update(update_data)
            .eq("id", location_id)
            .execute()
        )

        if not result.data:
            return None

        return result.data[0]

    @staticmethod
    def delete_location(location_id: int):
        """Delete location"""
        supabase = get_supabase_client()

        existing_location = (
            supabase.table("locations")
            .select("*")
            .eq("id", location_id)
            .execute()
        )

        if not existing_location.data:
            return None

        result = (
            supabase.table("locations")
            .delete()
            .eq("id", location_id)
            .execute()
        )

        if not result.data:
            return None

        return {
            "message": "Location deleted successfully",
            "deleted_location": result.data[0]
        }