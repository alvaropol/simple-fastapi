from typing import Optional

from datetime import datetime
from pydantic import BaseModel, Field


class BookDto(BaseModel):
    title: str = Field(...)
    author: Optional[str] = Field(None)
    publication_date: datetime | None = Field(...)

    class Config:
        from_attributes = True
