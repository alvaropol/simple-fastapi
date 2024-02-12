from datetime import datetime
from typing import List

from pydantic import BaseModel


class BookDto(BaseModel):
    title: str
    publication_date: datetime | None
    tags: List[str]
