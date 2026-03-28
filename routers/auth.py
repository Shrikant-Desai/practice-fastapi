from fastapi import APIRouter
from schemas.auth import RegisterRequest, LoginRequest, TokenResponse
import services.auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201)
async def register(data: RegisterRequest):
    return await auth_service.register_user(data)

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    return await auth_service.login_user(data)
