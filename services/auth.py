from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from repositories.auth import AuthRepository
from tasks.email_tasks import send_welcome_email


async def register_user(data: RegisterRequest, db: AsyncSession) -> dict:
    repo = AuthRepository(db)
    if await repo.find_by_email(data.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    if await repo.find_by_username(data.username):
        raise HTTPException(status_code=409, detail="Username already registered")

    user_data = data.model_dump()
    user_data["password"] = hash_password(user_data.pop("password"))
    await repo.create(user_data)
    send_welcome_email.delay(user_data["email"], user_data["username"])
    return {"msg": "user created", "data": user_data}


async def login_user(data: LoginRequest, db: AsyncSession) -> TokenResponse:
    repo = AuthRepository(db)
    user = await repo.find_by_email(data.email)

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": user.email, "role": user.role, "id": user.id}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )
