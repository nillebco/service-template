from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, Response

from ..constants import MEDIA_DYNAMIC_API
from ..logic.dynamic_media import get_media_url

router = APIRouter(prefix=MEDIA_DYNAMIC_API)

SECONDS_IN_A_DAY = 86400


@router.get("/{media_id}")
async def media_get(request: Request, media_id: str):
    uri = await get_media_url(media_id)
    if not uri:
        return Response(status_code=404)
    return RedirectResponse(uri)


@router.head("/{media_id}")
async def media_head(request: Request, media_id: str):
    uri = await get_media_url(media_id)
    if not uri:
        return Response(status_code=404)
    return RedirectResponse(uri)
