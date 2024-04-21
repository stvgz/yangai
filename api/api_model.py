"""Pydantic models for API requests and responses."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Conversation
class ConversationBase(BaseModel):
    user_name: str
    conversation: Optional[str] = None
    notes: Optional[str] = None

class ConversationCreate(ConversationBase):
    pass

class ConversationDisplay(ConversationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted: int

    class Config:
        orm_mode = True


# Sentence
class SentenceBase(BaseModel):
    from_user: Optional[str] = None
    to_user: Optional[str] = None
    text: str
    type: Optional[str] = None
    model: Optional[str] = None
    notes: Optional[str] = None

class SentenceCreate(SentenceBase):
    pass

class SentenceDisplay(SentenceBase):
    id: int
    created: datetime
    conversation_id: Optional[int] = None

    class Config:
        orm_mode = True
