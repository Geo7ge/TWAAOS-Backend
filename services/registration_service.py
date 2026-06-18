from supabase import create_client
import os
import logging
from datetime import datetime, timezone
from schemas.registration import RegistrationCreate
from dotenv import load_dotenv
from services.user_service import UserService
from services.events_service import EventService
from services.locations_service import LocationService
from services.email_service import EmailService


def format_event_datetime(value):
    if not value:
        return "Neconfigurat"
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M")
    try:
        parsed = datetime.fromisoformat(str(value))
        return parsed.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(value)

logger = logging.getLogger(__name__)

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

class RegistrationService:
    @staticmethod
    def create_registration(registration_data: RegistrationCreate):
        """Înscrie un utilizator la un eveniment"""
        supabase = get_supabase_client()
        
        # 1. Verificăm dacă utilizatorul este deja înscris la acest eveniment
        # pentru a evita duplicatele
        existing = supabase.table("registrations") \
            .select("*") \
            .eq("user_id", registration_data.user_id) \
            .eq("event_id", registration_data.event_id) \
            .execute()
        
        if existing.data:
            # Utilizatorul este deja înscris
            return {"error": "User already registered for this event", "data": existing.data[0]}
        
        # 2. Pregătim datele pentru inserare
        registration_dict = registration_data.model_dump()
        registration_dict["status"] = registration_dict.get("status", "pending")
        registration_dict["created_at"] = datetime.now(timezone.utc).isoformat()
        
        # 3. Inserăm în baza de date
        result = supabase.table("registrations").insert(registration_dict).execute()
        
        if not result.data:
            return None
            
        return result.data[0]

    @staticmethod
    def send_registration_confirmation(user_id: int, event_id: int):
        try:
            user = UserService.get_user_by_id(user_id)
            event = EventService.get_event_by_id(event_id)

            if not user or not event:
                logger.warning(f"Could not find user {user_id} or event {event_id}")
                return False

            recipient = user.get("email")
            if not recipient:
                logger.warning(f"User {user_id} has no email address")
                return False

            subject = f"Confirmare înscriere la {event.get('title', event.get('name', 'eveniment'))}"

            location = "Neconfigurată"
            if event.get('location_id'):
                try:
                    location_data = LocationService.get_location_by_id(event['location_id'])
                    if location_data and isinstance(location_data, dict):
                        name = location_data.get('name', "Neconfigurată")
                        address = location_data.get('address')
                        city = location_data.get('city')
                        address_parts = [part for part in [address, city] if part]
                        if address_parts:
                            location = f"{name}, {' '.join(address_parts)}"
                        else:
                            location = name
                except Exception as loc_err:
                    logger.warning(f"Could not fetch location {event.get('location_id')}: {loc_err}")

            body_lines = [
                f"Bună {user.get('name', 'participant')},",
                "",
                "Iată confirmarea înscrierii tale:",
                "",
                f"Nume eveniment: {event.get('title', event.get('name', 'N/A'))}",
                f"Descriere: {event.get('description', 'Nu este disponibilă')}",
                f"Data si ora evenimentului: {format_event_datetime(event.get('start_time'))}",
                f"Finalul evenimetului: {format_event_datetime(event.get('end_time'))}",
                f"Locație: {location}",
                "",
                "Dacă ai nevoie de informații suplimentare, contactează organizatorul.",
                "Mulțumim pentru înscriere!",
            ]

            body = "\n".join(body_lines)

            EmailService.send_email(subject, body, recipient)
            logger.info(f"Registration confirmation email sent to {recipient}")
            return True
        except Exception as e:
            logger.error(f"Error sending registration confirmation email: {str(e)}")
            return False

    @staticmethod
    def get_user_registrations(user_id: int):
        """Obține toate evenimentele la care este înscris un utilizator"""
        supabase = get_supabase_client()
        # Putem folosi select cu join dacă baza de date e configurată corect (foreign keys)
        # Ex: .select("*, events(*)") pentru a aduce și detaliile evenimentului
        result = supabase.table("registrations") \
            .select("*, events(*)") \
            .eq("user_id", user_id) \
            .execute()
        return result.data

    @staticmethod
    def get_event_registrations(event_id: int):
        """Obține toți participanții la un anumit eveniment"""
        supabase = get_supabase_client()
        result = supabase.table("registrations") \
            .select("*, users(id, name, email)") \
            .eq("event_id", event_id) \
            .execute()
        return result.data

    @staticmethod
    def update_registration_status(registration_id: int, status: str | None):
        supabase = get_supabase_client()

        if status is None:
            return None

        result = supabase.table("registrations") \
            .update({"status": status, "updated_at": datetime.now(timezone.utc).isoformat()}) \
            .eq("id", registration_id) \
            .execute()

        return result.data[0] if result.data else None

    @staticmethod
    def delete_registration(registration_id: int):
        """Anulează o înscriere (delete)"""
        supabase = get_supabase_client()
        result = supabase.table("registrations") \
            .delete() \
            .eq("id", registration_id) \
            .execute()
        return result.data