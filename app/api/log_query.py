from fastapi import APIRouter, Query, status
from typing import List, Optional
import json
import os

router = APIRouter(prefix="/logs", tags=["logs"])

LOG_FILE_PATH = "logs/app.log.jsonl"

@router.get("/")
async def query_logs(
    level: Optional[str] = Query(None, description="log level filter (e.g. INFO, EEOR)"),
    service: Optional[str] = Query(None, description="Service name filter"),
    event: Optional[str] = Query(None, description="Event name filter"),
    limit: int = Query(50, ge=1, le=500, description="Max number of logs to return"),
    offset: int = Query(0, ge=0, description="Number of logs to skip"),
):
    if not os.path.exists(LOG_FILE_PATH):
        return {"data": [], "limit": limit, "offset": offset, "total": 0}
    
    matched_logs = []

    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for line in reversed(lines):
        try:
            log = json.loads(line)
        except json.JSONDecodeError:
            continue

        if level and log.get("level", "").lower() != level.lower():
            continue
        if service and log.get("service", "").lower() != service.lower():
            continue
        if event and log.get("event", "").lower() != event.lower():
            continue

        matched_logs.append(log)
    
    total = len(matched_logs)

    paged_logs = matched_logs[offset:offset + limit]
    return {"data": paged_logs, "limit": limit, "offset": offset, "total": total}

@router.get("/levels")
async def get_log_levels():
    level = set()

    if not os.path.exists(LOG_FILE_PATH):
        return {"levels": []}

    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                log = json.loads(line)
                level.add(log.get("level", "").upper())
            except json.JSONDecodeError:
                continue
    
    return {"levels": sorted(level)}

@router.get("/services")
async def get_log_services():
    services = set()

    if not os.path.exists(LOG_FILE_PATH):
        return {"services": []}

    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                log = json.loads(line)
                service = log.get("service")
                if service:
                    services.add(service)
            except json.JSONDecodeError:
                continue
        
    return {"services": sorted(services)}

@router.get("/events")
async def get_log_events():
    events = set()

    if not os.path.exists(LOG_FILE_PATH):
        return {"events": []}

    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                log = json.loads(line)
                event = log.get("event")
                if event:
                    events.add(event)
            except json.JSONDecodeError:
                continue
        
    return {"events": sorted(events)}

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_logs():
    if os.path.exists(LOG_FILE_PATH):
        os.remove(LOG_FILE_PATH)