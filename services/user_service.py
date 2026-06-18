from passlib.context import CryptContext
from schemas.user import UserCreate, UserLogin, Token
from supabase import create_client, Client
import os
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_supabase_client():
    """Get Supabase client, create if not exists"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_user(user_data: UserCreate):
        """Create new user"""
        supabase = get_supabase_client()
        # Check if email already exists
        existing = supabase.table("users").select("*").eq("email", user_data.email).execute()
        if existing.data:
            return None
        
        hashed_password = UserService.hash_password(user_data.password)
        user_dict = user_data.model_dump()
        user_dict["password"] = hashed_password
        user_dict["created_at"] = datetime.now(timezone.utc).isoformat()
        user_dict["updated_at"] = datetime.now(timezone.utc).isoformat()
        result = supabase.table("users").insert(user_dict).execute()
        if not result.data:
            return None
        return result.data[0]

    @staticmethod
    def authenticate_user(user_data: UserLogin) -> Token:
        """Authenticate user and return token"""
        supabase = get_supabase_client()
        result = supabase.table("users").select("*").eq("email", user_data.email).execute()
        if not result.data:
            return None
        user = result.data[0]
        if not UserService.verify_password(user_data.password, user["password"]):
            return None
        access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
        expire = datetime.now(timezone.utc) + access_token_expires
        to_encode = {"sub": str(user["id"]), "exp": expire}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return Token(
            access_token=encoded_jwt,
            token_type="bearer",
            user_id=user["id"],
            email=user["email"],
            role=user.get("role"),
            name=user["name"]
        )

    @staticmethod
    def generate_token_for_user(user: dict) -> Token:
        """Generate JWT token and Token response for an existing user dict"""
        access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
        expire = datetime.now(timezone.utc) + access_token_expires
        to_encode = {"sub": str(user["id"]), "exp": expire}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return Token(
            access_token=encoded_jwt,
            token_type="bearer",
            user_id=user["id"],
            email=user.get("email"),
            role=user.get("role"),
            name=user.get("name")
        )

    @staticmethod
    def get_user_by_email(email: str):
        """Get user by email"""
        supabase = get_supabase_client()
        result = supabase.table("users").select("*").eq("email", email).execute()
        if not result.data:
            return None
        return result.data[0]

    @staticmethod
    def get_user_by_id(user_id: int):
        """Get user by ID"""
        supabase = get_supabase_client()
        result = supabase.table("users").select("*").eq("id", user_id).execute()
        if not result.data:
            return None
        return result.data[0]

    @staticmethod
    def get_all_users():
        """Get all users without passwords"""
        supabase = get_supabase_client()
        result = supabase.table("users").select("id, email, name, role, created_at").execute()
        if not result.data:
            return []
        return result.data

    @staticmethod
    def delete_user(user_id: int):
        """Delete user by ID"""
        supabase = get_supabase_client()
        # Check if user exists
        user = supabase.table("users").select("id").eq("id", user_id).execute()
        if not user.data:
            return False
        # Delete the user
        result = supabase.table("users").delete().eq("id", user_id).execute()
        return True
