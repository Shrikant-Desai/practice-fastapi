# routers/auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])

# Fake DB — we'll replace with a real one in Module 6
fake_users_db: dict[str, dict] = {}


class RegisterRequest(BaseModel):
    email: str
    password: str
    role: str = "user"


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/register", status_code=201)
async def register(data: RegisterRequest):
    if data.email in fake_users_db:
        raise HTTPException(status_code=409, detail="Email already registered")

    fake_users_db[data.email] = {
        "email": data.email,
        "hashed_password": hash_password(data.password),
        "role": data.role,
    }
    return {"msg": "User created"}


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    user = fake_users_db.get(data.email)

    if not user or not verify_password(data.password, user["hashed_password"]):
        # IMPORTANT: same error for both "user not found" and "wrong password"
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": data.email, "role": user["role"]}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )
