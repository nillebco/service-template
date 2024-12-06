from typing import Optional

from sqlmodel import JSON, Column, Field, SQLModel

from ..times import utc_now_float


class DynamicMedia(SQLModel, table=True):
    """
    Associates an ID to a media.
    """

    uid: Optional[int] = Field(default=None, primary_key=True)
    kind: str
    entity_id: str
    created_at: Optional[float] = Field(default_factory=lambda: utc_now_float())
    info: dict = Field(default_factory=list, sa_column=Column(JSON))
