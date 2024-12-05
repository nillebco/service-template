from typing import Optional

from sqlmodel import JSON, Column, Field, SQLModel

from ..times import utc_now_float

class Recording(SQLModel, table=True):
    """
    A recording is a message exchanged on a conversation. Not necessarily between the assistant and the user.
    Will be used to keep track of the conversation and summarize it.

    It's not clear who is the owner of the recording.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    transport: str
    sender: str
    session_id: str
    subscribers: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    query: str
    conversation_id: Optional[str] = None
    mentions: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    is_mentioning_bot: bool
    timestamp: float = Field(default_factory=lambda: utc_now_float())
