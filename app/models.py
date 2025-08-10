# 模型
from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from datetime import datetime, timezone

class Question(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    content: str = Field(max_length=500)
    ip: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
