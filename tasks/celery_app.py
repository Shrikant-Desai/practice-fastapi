from celery import Celery
from core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "myapp",
    broker=settings.redis_url,  # Redis as the message broker
    backend=settings.redis_url,  # Redis to store task results
)

celery_app.conf.update(
    task_serializer="json",
    result_expires=3600,
    timezone="UTC",
)
