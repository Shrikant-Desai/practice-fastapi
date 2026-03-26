# routers/protected.py
from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user, require_admin, require_roles

router = APIRouter(tags=["protected"])


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    # Any authenticated user can reach this
    return {"email": current_user["sub"], "role": current_user["role"]}


@router.get("/admin/dashboard")
async def admin_dashboard(current_user: dict = Depends(require_admin)):
    # Only admins reach this — 403 returned automatically otherwise
    return {"msg": "Welcome, admin", "user": current_user["sub"]}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int, current_user: dict = Depends(require_roles("admin", "superadmin"))
):
    return {"deleted": user_id}


@router.get("/reports")
async def get_reports(current_user: dict = Depends(require_roles("admin", "analyst"))):
    return {"data": [...]}
