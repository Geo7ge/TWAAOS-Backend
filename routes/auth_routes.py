from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import os
import httpx
from services.user_service import UserService
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

router = APIRouter(prefix="/auth", tags=["auth"])


class SupabaseTokenIn(BaseModel):
    token: str


@router.post("/supabase-google")
def supabase_google_login(data: SupabaseTokenIn):
    """Validate Supabase token, map to internal user and return internal Token response."""
    if not data.token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing token")

    # Validate token with Supabase: GET /auth/v1/user
    url = f"{SUPABASE_URL}/auth/v1/user"
    headers = {"Authorization": f"Bearer {data.token}", "apikey": SUPABASE_KEY}

    try:
        with httpx.Client(timeout=10) as client:
            resp = client.get(url, headers=headers)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error contacting Supabase: {e}")

    if resp.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Supabase token")

    supa_user = resp.json()
    email = supa_user.get("email")
    supa_id = supa_user.get("id")

    if not email:
        raise HTTPException(status_code=400, detail="Supabase user has no email")

    # Map to internal user by email
    internal_user = UserService.get_user_by_email(email)
    if not internal_user:
        raise HTTPException(status_code=404, detail="No internal user mapping for this account")

    # Generate internal token and return same shape as normal login
    token = UserService.generate_token_for_user(internal_user)
    return token
