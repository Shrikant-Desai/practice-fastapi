from fastapi import HTTPException
from schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from core.security import hash_password, verify_password, create_access_token, create_refresh_token
import repositories.auth as auth_repo

async def register_user(data: RegisterRequest) -> dict:
    if auth_repo.get_user_by_email(data.email):
        raise HTTPException(status_code=409, detail="Email already registered")

    auth_repo.create_user(data, hash_password(data.password))
    return {"msg": "User created"}

async def login_user(data: LoginRequest) -> TokenResponse:
    user = auth_repo.get_user_by_email(data.email)

    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": data.email, "role": user["role"]}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )
