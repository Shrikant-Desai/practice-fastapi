from celery.result import AsyncResult
from tasks.celery_app import celery_app
from fastapi import APIRouter


router = APIRouter(tags=["tasks"])


@router.get("/tasks")
async def get_all_tasks():
    inspect = celery_app.control.inspect()

    return {
        "active": inspect.active() or {},
        "reserved": inspect.reserved() or {},
        "scheduled": inspect.scheduled() or {},
    }


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,  # PENDING, STARTED, SUCCESS, FAILURE
        "result": result.result if result.ready() else None,
    }
