from fastapi import APIRouter, HTTPException, status
from schemas.user import UserCreate, UserResponse, UserLogin, Token
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user_data: UserCreate):
    """Register a new user"""
    user = UserService.create_user(user_data)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )
    return UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        role=user.get("role"),
        created_at=user["created_at"],
    )


@router.post("/login", response_model=Token)
def login(user_data: UserLogin):
    """Login user and return access token"""
    token = UserService.authenticate_user(user_data)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token


@router.get("/", response_model=list[UserResponse])
def get_all_users():
    """Get all users"""
    users = UserService.get_all_users()
    return [
        UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            role=user.get("role"),
            created_at=user["created_at"],
        )
        for user in users
    ]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Get user by ID"""
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        role=user.get("role"),
        created_at=user["created_at"],
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Delete user by ID"""
    deleted = UserService.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None
