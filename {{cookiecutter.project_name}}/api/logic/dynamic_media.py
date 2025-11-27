from typing import Callable, Optional

from ..database.sql import get_or_create_media
from ..database.types import DynamicMedia

ENTRY_RESOLVERS = {}

URI_GETTERS = {}


def register_entry_resolver(kind: str, resolver: Callable):
    ENTRY_RESOLVERS[kind] = resolver


def register_uri_getter(kind: str, getter: Callable):
    URI_GETTERS[kind] = getter


async def get_dynamic_media(media_id) -> DynamicMedia:
    return await get_or_create_media(media_id)


def resolve_entry(media: DynamicMedia):
    resolver = ENTRY_RESOLVERS.get(media.kind)
    if resolver:
        return resolver(media.entity_id)
    return None


def _get_media_url(media: DynamicMedia) -> Optional[str]:
    method = URI_GETTERS.get(media.kind)
    if not method or not media:
        return None

    entry = resolve_entry(media)
    if not entry:
        return None

    url = method(entry)
    return url


async def get_media_url(media_id: str) -> Optional[str]:
    media = await get_dynamic_media(media_id)

    if not media:
        return None

    return _get_media_url(media)
