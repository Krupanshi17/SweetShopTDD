from fastapi import APIRouter
from app.schemas.user_schema import UserCreate, UserLogin, TokenResponse
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(user: UserCreate):
    return await register_user(user)

@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin):
    return await login_user(user)