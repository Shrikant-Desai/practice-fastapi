# services/user_service.py
from fastapi import HTTPException
from repositories.user_repository import UserRepository
from schemas.auth import UserCreate, UserUpdate
from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, data: UserCreate) -> dict:
        if await self.repo.find_by_email(data.email):
            raise HTTPException(status_code=409, detail="Email already registered")

        user = await self.repo.create(
            {
                "email": data.email,
                "username": data.username,
                "password": hash_password(data.password),
                "role": "user",
            }
        )
        return user

    async def login(self, email: str, password: str) -> dict:
        user = await self.repo.find_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not user.is_active:
            raise HTTPException(status_code=403, detail="Account is inactive")

        token_data = {"sub": str(user.id), "role": user.role}
        return {
            "access_token": create_access_token(token_data),
            "refresh_token": create_refresh_token(token_data),
            "token_type": "bearer",
        }

    async def get_user(self, user_id: int) -> dict:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def update_user(
        self, user_id: int, data: UserUpdate, current_user: dict
    ) -> dict:
        user = await self.get_user(user_id)
        if str(user.id) != current_user["sub"] and current_user["role"] != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        updates = data.model_dump(exclude_unset=True)
        return await self.repo.update(user, updates)
