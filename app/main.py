import uuid
import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.api.logs import router as logs_router
from app.core.errors import global_exception_handler

app = FastAPI(title=settings.app_name)
app.include_router(logs_router)
app.add_exception_handler(Exception, global_exception_handler)
setup_logging(settings.log_level)

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start_time = time.time()

        log = logger.bind(
            request_id=request_id,
            path=request.url.path,
            method=request.method,
            )

        try:
            response = await call_next(request)
        except Exception as exc:
            log.error(
                "request failed",
                error=str(exc),
                exc_info=True,
            )
            raise

        duration = time.time() - start_time

        log.info("request_end", status_code=response.status_code, duration_ms=int(duration * 1000))

        response.headers["X-Request-ID"] = request_id

        return response

app.add_middleware(RequestIDMiddleware)

@app.get("/health")
async def health_check():
    logger.info("health check")
    return {"status": "ok"}
