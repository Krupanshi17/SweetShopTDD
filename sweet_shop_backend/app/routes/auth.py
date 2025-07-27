# app/routes/auth.py
from fastapi import APIRouter, status, Form
from fastapi.responses import JSONResponse
from app.services.auth_service import register_user, login_user
from app.schemas.user_schema import UserCreate, UserLogin

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register")
async def register(user: UserCreate):
    """
    Endpoint to register a new user.
    Accepts UserCreate schema, calls the register_user service,
    and returns the created user's info with HTTP 201 status.
    """
    result = await register_user(user)
    return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)

@router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...)
):
    """
    Endpoint to login a user.
    Receives username and password as form data,
    creates UserLogin schema, calls login_user service,
    and returns the authentication token with HTTP 200 status.
    """
    credentials = UserLogin(email=username, password=password)
    result = await login_user(credentials)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
