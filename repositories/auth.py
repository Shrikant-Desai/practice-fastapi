from schemas.auth import RegisterRequest

fake_users_db: dict[str, dict] = {}

def get_user_by_email(email: str) -> dict | None:
    return fake_users_db.get(email)

def create_user(data: RegisterRequest, hashed_password: str) -> dict:
    user = {
        "email": data.email,
        "hashed_password": hashed_password,
        "role": data.role,
    }
    fake_users_db[data.email] = user
    return user
