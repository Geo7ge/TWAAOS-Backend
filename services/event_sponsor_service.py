from supabase import create_client
import os
from dotenv import load_dotenv

from schemas.event_sponsor import EventSponsorCreate, EventSponsorUpdate

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


class EventSponsorService:

    @staticmethod
    def create_event_sponsor(data: EventSponsorCreate):
        supabase = get_supabase_client()

        result = supabase.table("event_sponsors").insert(data.model_dump()).execute()

        return result.data[0] if result.data else None

    @staticmethod
    def get_all():
        supabase = get_supabase_client()

        result = supabase.table("event_sponsors").select("*").execute()

        return result.data if result.data else []

    @staticmethod
    def get_by_id(es_id: int):
        supabase = get_supabase_client()

        result = (
            supabase
            .table("event_sponsors")
            .select("*")
            .eq("id", es_id)
            .execute()
        )

        return result.data[0] if result.data else None

    @staticmethod
    def get_by_event_id(event_id: int):
        supabase = get_supabase_client()

        result = (
            supabase
            .table("event_sponsors")
            .select("*")
            .eq("event_id", event_id)
            .execute()
        )

        return result.data if result.data else []

    @staticmethod
    def get_by_sponsor_id(sponsor_id: int):
        supabase = get_supabase_client()

        result = (
            supabase
            .table("event_sponsors")
            .select("*")
            .eq("sponsor_id", sponsor_id)
            .execute()
        )

        return result.data if result.data else []

    @staticmethod
    def update_event_sponsor(es_id: int, data: EventSponsorUpdate):
        supabase = get_supabase_client()

        update_data = {
            k: v for k, v in data.model_dump().items()
            if v is not None
        }

        result = (
            supabase
            .table("event_sponsors")
            .update(update_data)
            .eq("id", es_id)
            .execute()
        )

        return result.data[0] if result.data else None

    @staticmethod
    def delete_event_sponsor(es_id: int):
        supabase = get_supabase_client()

        result = (
            supabase
            .table("event_sponsors")
            .delete()
            .eq("id", es_id)
            .execute()
        )

        return True if result else False