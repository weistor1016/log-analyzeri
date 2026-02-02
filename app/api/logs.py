from fastapi import APIRouter, HTTPException
from app.models.log_entry import LogEntry
from app.core.logging import logger

router = APIRouter(prefix="/logs", tags=["logs"])

@router.post("/")
async def ingest_log(log: LogEntry):
    log_ctx = logger.bind(
        service=log.service,
        event=log.event,
        user_id=log.user_id,
        request_id=log.request_id,
    )

    if log.level not in {"DEBUG", "INFO", "WARN", "ERROR"}:
        log_ctx.warning(
            "invalid_log_level",
            received_level=log.level,
        )
    
        raise HTTPException(
            status_code=400,
            detail="Invalid log level"
        )

    log_ctx.info(
        "log_ingested",
        message=log.message,
        level=log.level,
    )
    
    return {"status": "accepted"}