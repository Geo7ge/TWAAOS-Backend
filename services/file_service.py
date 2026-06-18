from supabase import create_client
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

from schemas.file import FileCreate, FileUpdate

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


class FileService:

    @staticmethod
    def create_file(file_data: FileCreate):
        supabase = get_supabase_client()

        data = file_data.model_dump()
        data["uploaded_at"] = datetime.now(timezone.utc).isoformat()

        result = supabase.table("files").insert(data).execute()

        return result.data[0] if result.data else None

    @staticmethod
    def get_all_files():
        supabase = get_supabase_client()

        result = supabase.table("files").select("*").execute()

        return result.data if result.data else []

    @staticmethod
    def get_file_by_id(file_id: int):
        supabase = get_supabase_client()

        result = (
            supabase
            .table("files")
            .select("*")
            .eq("id", file_id)
            .execute()
        )

        return result.data[0] if result.data else None

    @staticmethod
    def get_files_by_event(event_id: int):
        supabase = get_supabase_client()

        result = (
            supabase
            .table("files")
            .select("*")
            .eq("event_id", event_id)
            .execute()
        )

        return result.data if result.data else []

    @staticmethod
    def update_file(file_id: int, file_data: FileUpdate):
        supabase = get_supabase_client()

        # eliminăm câmpurile None
        update_data = {
            k: v for k, v in file_data.model_dump().items()
            if v is not None
        }

        result = (
            supabase
            .table("files")
            .update(update_data)
            .eq("id", file_id)
            .execute()
        )

        return result.data[0] if result.data else None

    @staticmethod
    def delete_file(file_id: int):
        supabase = get_supabase_client()

        result = (
            supabase
            .table("files")
            .delete()
            .eq("id", file_id)
            .execute()
        )

        return True if result else False