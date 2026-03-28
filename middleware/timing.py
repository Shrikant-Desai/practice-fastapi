import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Before the route handler
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        # Attach request_id to request state — accessible anywhere downstream
        request.state.request_id = request_id

        # call_next hands off to the next middleware or route handler
        response = await call_next(request)

        # After the route handler
        duration_ms = (time.perf_counter() - start_time) * 1000
        response.headers["X-Request-ID"]    = request_id
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"

        # This is where you'd log to your observability stack (Module 8)
        print(
            f"[{request_id}] "
            f"{request.method} {request.url.path} "
            f"→ {response.status_code} "
            f"({duration_ms:.2f}ms)"
        )
        return response