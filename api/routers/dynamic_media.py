from fastapi.responses import RedirectResponse

from ..constants import MEDIA_DYNAMIC_API
from fastapi import APIRouter, Request

router = APIRouter(prefix=MEDIA_DYNAMIC_API)

SECONDS_IN_A_DAY = 86400


@router.get("/{media_id}")
async def media_get(request: Request, media_id: str):
    uri = "/test"
    return RedirectResponse(uri)


@router.head("/{media_id}")
async def media_head(request: Request, media_id: str):
    uri = "/test"
    return RedirectResponse(uri)

